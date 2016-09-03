#!/usr/bin/env python
# -*- coding: utf8 -*-
#~#######################################################################
#~ Copyright (c) 2008 Burdakov Daniel <kreved@kreved.org>               #
#~                                                                      #
#~ This file is part of FreQ-bot.                                       #
#~                                                                      #
#~ FreQ-bot is free software: you can redistribute it and/or modify     #
#~ it under the terms of the GNU General Public License as published by #
#~ the Free Software Foundation, either version 3 of the License, or    #
#~ (at your option) any later version.                                  #
#~                                                                      #
#~ FreQ-bot is distributed in the hope that it will be useful,          #
#~ but WITHOUT ANY WARRANTY; without even the implied warranty of       #
#~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
#~ GNU General Public License for more details.                         #
#~                                                                      #
#~ You should have received a copy of the GNU General Public License    #
#~ along with FreQ-bot.  If not, see <http://www.gnu.org/licenses/>.    #
#~#######################################################################

import twisted
from twisted.words.protocols.jabber import client, jid, xmlstream
from twisted.words.protocols.jabber.client import XMPPAuthenticator
from twisted.internet import reactor, threads, defer
from twisted.words.xish import domish
from twisted.words.xish.domish import Element, ParserError
from twisted.web.html import escape
import traceback
import re
import log
import sys
import config
import time

class NonStrictExpatElementStream:
    """
    Based on twisted.words.xish.domish.ExpatElementStream, but parses
    namespaces manually, without help of pyexpat, so it doesn't crash
    because of unbound prefixes.
    """
    def __init__(self):
        import pyexpat
        self.strict = False
        self.DocumentStartEvent = None
        self.ElementEvent = None
        self.DocumentEndEvent = None
        self.error = pyexpat.error
        self.parser = pyexpat.ParserCreate("UTF-8")
        self.parser.StartElementHandler = self._onStartElement
        self.parser.EndElementHandler = self._onEndElement
        self.parser.CharacterDataHandler = self._onCdata
        self.currElem = None
        self.defaultNsStack = ['']
        self.documentStarted = 0
        self.reserverPrefixes = {'xml': 'http://www.w3.org/XML/1998/namespace',\
        'xmlns': 'http://www.w3.org/2000/xmlns/'}
        self.localPrefixesStack = [{}]

    def parse(self, buffer):
        try:
            self.parser.Parse(buffer)
        except self.error, e:
            raise ParserError, str(e)
    
    def getUriByPrefix(self, q):
      prefix = q[0]
      nname = q[1]
      uri = None
      i = len(self.localPrefixesStack) - 1
      while ((i>=0) and (uri is None)):
        uri = self.localPrefixesStack[i].get(prefix, None)
        i -= 1
      if uri is None:
        if prefix.lower().startswith('xml'):
          uri = self.reserverPrefixes.get(prefix, self.defaultNsStack[-1])
        elif self.strict: raise ParserError, 'Unbound prefix: ' + prefix
        else: uri = self.defaultNsStack[-1]
      return (uri, nname)

    def _onStartElement(self, name, attrs):
        # Push default uri into stack
        defaultNs = attrs.pop('xmlns', None)
        if defaultNs is None: self.defaultNsStack.append(self.defaultNsStack[-1])
        else: self.defaultNsStack.append(defaultNs)
        
        self.localPrefixesStack.append({})
        
        # Check for local prefixes
        for k, v in attrs.items():
            if k.startswith('xmlns:'):
                 prefix = k[6:]
                 self.localPrefixesStack[-1][prefix] = v
                 del attrs[k]
        
        # Generate a qname tuple from the provided name
        qname = name.split(":")
        if len(qname) == 1: qname = (self.defaultNsStack[-1], name)
        else: qname = self.getUriByPrefix(qname)

        # Process attributes
        for k, v in attrs.items():
            if k.find(":") != -1:
                aqname = k.split(":")
                attrs[self.getUriByPrefix(aqname)] = v
                del attrs[k]

        # Construct the new element
        e = Element(qname, self.defaultNsStack[-1], attrs, self.localPrefixesStack[-1])

        # Document already started
        if self.documentStarted == 1:
            if self.currElem != None:
                self.currElem.children.append(e)
                e.parent = self.currElem
            self.currElem = e

        # New document
        else:
            self.documentStarted = 1
            self.DocumentStartEvent(e)

    def _onEndElement(self, _):
        # Check for null current elem; end of doc
        if self.currElem is None:
            self.DocumentEndEvent()

        # Check for parent that is None; that's
        # the top of the stack
        elif self.currElem.parent is None:
            self.ElementEvent(self.currElem)
            self.currElem = None

        # Anything else is just some element in the current
        # packet wrapping up
        else:
            self.currElem = self.currElem.parent
        
        self.defaultNsStack.pop()
        self.localPrefixesStack.pop()

    def _onCdata(self, data):
        if self.currElem != None:
            self.currElem.addContent(data)

class MyXmlStream(xmlstream.XmlStream):
 
 def __init__(self, *args, **kwargs):
        xmlstream.XmlStream.__init__(self, *args, **kwargs)
        self.logger = log.logger()
 
 def _initializeStream(self):
        """ Sets up XML Parser. """
        self.stream = NonStrictExpatElementStream()
        self.stream.DocumentStartEvent = self.onDocumentStart
        self.stream.ElementEvent = self.onElement
        self.stream.DocumentEndEvent = self.onDocumentEnd

 def dataReceived(self, data):
        """ Called whenever data is received.

        Passes the data to the XML parser. This can result in calls to the
        DOM handlers. If a parse error occurs, the L{STREAM_ERROR_EVENT} event
        is called to allow for cleanup actions, followed by dropping the
        connection.
        """
        try:
         if self.rawDataInFn:
          self.rawDataInFn(data)
         self.stream.parse(data)
        except domish.ParserError:
         if type(data) == type(''): data = data.decode('utf8')
         self.logger.err_e('*** CRASH BECAUSE OF BAD STANZA: ' + data)
         self.dispatch(self, twisted.words.xish.xmlstream.STREAM_ERROR_EVENT)
         self.transport.loseConnection()

class ClientFactory(xmlstream.XmlStreamFactory):
    
    protocol = MyXmlStream
    
    def __init__(self, a, host):
        self.host = host
        xmlstream.XmlStreamFactory.__init__(self, a)

    def clientConnectionFailed(self, connector, reason):
        m = 'Connection failed! ' + repr(reason.getTraceback())
        self.host.log.err_e(m)
        self.host.log.log_e(m)
        try: reactor.stop()
        except twisted.internet.error.ReactorNotRunning: pass

    def clientConnectionLost(self, connector, reason):
        if self.host.stopped: return
        m = 'Connection lost! ' + repr(reason.getTraceback())
        self.host.log.err_e(m)
        self.host.log.log_e(m)
        try: reactor.stop()
        except twisted.internet.error.ReactorNotRunning: pass

class wrapper:

 def __init__(self, version):
  self.version = version
  self.stopped = False
  self.tc = 0
  self.th = {}
  self.sjid = u'%s@%s/%s' % (config.USER, config.SERVER, config.RESOURCE)
  self.jid = jid.JID(self.sjid)
  self.onauthd = None
  self.a = XMPPAuthenticator(self.jid, config.PASSWD)
  self.c = ClientFactory(self.a, self)
  self.c.maxRetries = 0
  self.c.addBootstrap(xmlstream.STREAM_AUTHD_EVENT, self.authd)
  self.c.addBootstrap(xmlstream.INIT_FAILED_EVENT, self.initfailed)
  self.c.addBootstrap(xmlstream.STREAM_CONNECTED_EVENT, self.onConnected)
  self.c.addBootstrap(xmlstream.STREAM_END_EVENT, self.onDisconnected)
  self.x = None
  self.log = log.logger()
  self.msghandlers = []
  port = config.PORT
  if config.CONNECT_SERVER: server = config.CONNECT_SERVER
  else: server = config.SERVER
  if config.USE_SSL:
   from twisted.internet import ssl
   reactor.connectSSL(server, port, self.c, ssl.ClientContextFactory())
  else: reactor.connectTCP(server, port, self.c)

 def onConnected(self, xs):
  self.x = xs
  self.log.log('Connected! (STREAM_CONNECTED_EVENT)')

 def presence(self, status=None):
  if not self.x: return
  if not status: status = config.STATUS.replace(r'%VERSION%', self.version)
  p = domish.Element(('jabber:client', 'presence'))
  p.addElement('status').addContent(status)
  p.addElement('show').addContent('chat')
  self.x.send(p)

 def getChild(self, x, n):
  return [i for i in x.children if (i.__class__==domish.Element) and (i.name==n)][0]

 def authd(self, x):
  self.log.log('Authenticated! (STREAM_AUTHD_EVENT)')
  self.x.addObserver('/message', self.cbmessage)
  self.onauthd()

 def initfailed(self, x):
  self.log.err('Init failed! (INIT_FAILED_EVENT)')
  reactor.stop()

 def onDisconnected(self, x):
  if self.stopped: return
  self.log.err('Disconnected! (STREAM_END_EVENT)')
  reactor.stop()

 def register_msg_handler(self, func):
  self.msghandlers.append(func)

 def cbmessage(self, x):
  delayed = [i for i in x.children if (i.__class__==domish.Element) and ((i.name=='delay') or ((i.name=='x') and (i.uri=='jabber:x:delay')))]
  try: body = self.getChild(x, 'body').children[0]
  except: body = ''
  try: subject = self.getChild(x, 'subject').children[0]
  except: subject = None
  try: f = x['from']
  except: f = config.SERVER
  try: typ = x['type']
  except: typ = 'chat'
  if subject or not delayed:
   for i in self.msghandlers:
    self.call(i, typ, f, body, subject, x)

 def send(self, x):
  try: target = x['to']
  except: target = '(server)'
  self.log.log(u'try to send stanza to %s..' % (target, ), 0)
  reactor.callFromThread(self._send, x)

 def _send(self, x):
  try: self.x.send(x)
  except:
   try: xml = x.toXml()
   except: xml = '[can\'t x.toXml()]'
   m = '; '.join(traceback.format_exception(sys.exc_type, sys.exc_value, sys.exc_traceback))
   m = m.decode('utf8', 'replace')
   self.log.err_e('Can\'t send stanza! (xml: %s). Error: %s' % (xml, m))

 def msg(self, typ, j, body, subject=None):
  m = domish.Element(('jabber:client', 'message'))
  m['type'] = typ
  m['to'] = j
  if body: m.addElement('body').addContent(body)
  if subject: m.addElement('subject').addContent(subject)
  self.send(m)

 def call(self, f, *args, **kwargs):
  tc, self.tc = self.tc + 1, self.tc + 1
  self.th[tc] = (f, args, kwargs)
  if config.USE_THREADS: reactor.callInThread(self._call, f, tc, *args, **kwargs)
  else: self._call(f, tc, *args, **kwargs)
  try: self.th.pop(tc)
  except: self.log.err('Something wrong with threads management: can\'t self.th.pop(%s)' % (tc, ))

 def _call(self, f, tc, *args, **kwargs):
  try:
   self.log.log(escape('=== started thread #%s' % (tc, )), 1)
   try: f(*args, **kwargs)
   except:
    m = '; '.join(traceback.format_exception(sys.exc_type, sys.exc_value, sys.exc_traceback))
    m = m.decode('utf8', 'replace')
    m = u'<font color=red><b>UNCATCHED ERROR:</b></font> %s\n<br/>\n(f, *args, *kwargs, thread) was <font color=grey>(%s)</font>' \
         % (escape(m), escape(repr((f, args, kwargs, tc))))
    self.log.err(m)
   self.log.log(escape('=== finished thread #%s' % (tc, )), 1)
  except:
   m = ''.join(traceback.format_exception(sys.exc_type, sys.exc_value, sys.exc_traceback))
   print 'STOP: ', m
   self.log.err(escape(m))
   self.log.err('=== failed thread #%s' % (self.tc, ))
