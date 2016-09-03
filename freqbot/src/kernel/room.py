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
import config
import options
import lang
from twisted.internet.defer import Deferred
from twisted.words.protocols.jabber.client import IQ
from twisted.internet.reactor import callFromThread
from item import item as titem

class room:

 def __init__(self, bot, jid):
  self.bot = None
  self.globalbot = bot
  self.items = {}
  self.joiner = ()
  self.__getitem__ = self.items.__getitem__
  self.__setitem__ = self.items.__setitem__
  self.get = self.items.get
  self.has_key = self.items.has_key
  self.keys = self.items.keys
  self.jid = jid
  self.setdefault = self.items.setdefault
  self.pop = self.items.pop

 def get_option(self, k, d=None):
  return options.get_option(self.jid, k, d)

 def set_option(self, k, v):
  options.set_option(self.jid, k, v)

 def get_msglimit(self):
  return int(self.get_option('msglimit', config.MSGLIMIT))

 def set_msglimit(self, value):
  return self.set_option('msglimit', str(value))

 def rejoin(self):
  self.globalbot.muc.join(self.jid)

 def moderate(self, jn, jid_nick, ra, set_to, reason=None):
  if not reason:
   try: reason = self.bot.nick
   except: reason = 'freQ'
  packet = IQ(self.globalbot.wrapper.x, 'set')
  query = packet.addElement('query', 'http://jabber.org/protocol/muc#admin')
  i = query.addElement('item')
  i[jn] = jid_nick
  i[ra] = set_to
  i.addElement('reason').addContent(reason)
  d = Deferred()
  packet.addCallback(d.callback)
  #print packet.toXml()
  callFromThread(packet.send, self.jid)
  return d

 def server(self):
  jid = self.jid
  if jid.count('@'): return jid[jid.find('@')+1:]
  else: return jid

 def msg(self, body):
  self.globalbot.muc.msg('groupchat', self.jid, body)

 def get_lang(self):
  return lang.getLang(self.jid)

 def get_msg(self, template, params=()):
  return lang.msg(template, params, self.get_lang())

 def lmsg(self, template, *params):
  self.msg(lang.msg(template, params, lang.getLang(self.jid)))

 def count(self):
  return len(self.items)

 def set_subject(self, subject):
  self.globalbot.wrapper.msg('groupchat', self.jid, None, subject)
