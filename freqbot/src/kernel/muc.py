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

# todo: def fetch_error_code(presence): int
# use it to handle different error codes differently in presence_handler

from twisted.words.xish import domish
from twisted.web.html import escape
from item import item as new_item
from room import room as new_room
import config
import lang
import sys
import options
from random import randint

msglimit = 8000

class muc:

 def __init__(self, bot):
  self.g_file = '%s/text/groupchats.txt' % (config.DATADIR, )
  self.bot = bot
  self.bot.wrapper.x.addObserver('/presence', self.presence_handler)
  self.bot.g = {}

 def msg(self, t, s, b):
  b = self.bot.clear_text(b)
  # clear_text(unicode) is from plugins/shared/utils.py
  if len(b) > msglimit: b = b[:msglimit] + '... (truncated)'
  b = b.strip()
  self.bot.log.log(escape(u'attempt to send message to %s (type "%s", body: %s)' % (s, t, b)), 3)
  if (s in self.bot.g.keys()) or (t <> 'groupchat'):
   if b == '': b = '[empty message]'
   self.bot.wrapper.msg(t, s, b)
  else:
   s = s.split('/')
   groupchat = s[0]
   nick = '/'.join(s[1:])
   self.bot.log.log(escape(u'send message to %s (type "%s", body: %s)' % (groupchat, t, b)), 3)
   self.bot.wrapper.msg(t, groupchat, '%s: %s' % (nick, b))

 def is_admin(self, jid):
  return jid and (jid.split('/')[0].lower() in config.ADMINS)

 def get_access(self, item):
  self.bot.log.log(u'checking access for %s (%s)...' % (item.jid, item.realjid), 1)
  access = 0
  if item.role == 'participant': access += 1
  if item.role == 'moderator': access += 4
  if item.affiliation == 'none': access += 1
  if item.affiliation == 'member': access += 3
  if item.affiliation == 'admin': access += 5
  if item.affiliation == 'owner': access += 7
  if self.is_admin(item.realjid):
   access += 50
   if item.room and (item.room.server() in config.TRUSTED_SERVERS):
    access += 50
  if self.is_admin(item.jid): access += 100
  for m in self.bot.access_modificators: access = self.bot.call(m, item, access)
  return access

 def allowed(self, s, required_access):
  return self.get_access(s) >= required_access

 def invalid_syntax(self, t, s, text):
  try:
   s.lmsg(t, 'invalid_syntax', self.bot.read_file('doc/syntax/%s.txt' % (text, )).strip())
  except: s.lmsg(t, 'invalid_syntax_default')

 def presence_handler(self, x):
  if self.bot.stopped: return
  self.bot.log.log(u'presence_handler..', 1)
  try: typ = x['type']
  except: typ = 'available'
  jid = x['from'].split('/')
  groupchat = jid[0]
  nick = x['from'][len(groupchat)+1:]
  groupchat = self.bot.g.get(groupchat)
  if groupchat:
   if typ == 'available':
    item = groupchat.setdefault(nick, new_item(self.bot, groupchat))
    item.jid = x['from']
    try: item.status = [i for i in x.children if i.name=='status'][0].children[0]
    except: item.status = ''
    try: item.show = [i for i in x.children if i.name=='show'][0].children[0]
    except: item.show = 'online'
    item.nick = nick
    try:
     _x = [i for i in x.children if (i.name=='x') and (i.uri=='http://jabber.org/protocol/muc#user')][0]
     _item = [i for i in _x.children if i.name=='item'][0]
     item.affiliation = _item['affiliation']
     item.role = _item['role']
     try: item.realjid = _item['jid'].split('/')[0]
     except: item.realjid = item.jid
    except:
     self.bot.log.err(u"Got invalid presence from '%s'?\n%s: %s<br/><font color=grey>%s</font>" % (x['from'], escape(repr(sys.exc_info()[0])), escape(repr(sys.exc_info()[1])), escape(x.toXml())))
    if not item.handled:
     if item.nick == self.get_nick(groupchat.jid): # if item is bot...
      groupchat.bot = item
      gj = groupchat.joiner
      if gj:
       gj[0].lmsg(gj[1], 'join_success', groupchat.jid, nick)
       self.bot.log.log(u'reporting to %s about successful joining..' % (gj[0].jid, ), 6)
       groupchat.joiner = None
     item.handled = True
     self.bot.call_join_handlers(item)
    if not(item.nick == self.get_nick(groupchat.jid)): #if item isn't bot...
     self.bot.check_text(item, item.nick)
     self.bot.check_text(item, item.status)
   else:
    item = groupchat.pop(nick, None)
    if item:
     # parse leave_type, reason
     # leave_type: 0: leave
     #             1: kick
     #             2: ban
     #             3: rename
     if typ == 'unavailable':
      #unavailable
      try:
       _x = [i for i in x.children if (i.name=='x') and (i.uri == 'http://jabber.org/protocol/muc#user')][0]
       _item = [i for i in _x.children if i.name=='item'][0]
       _status = [i['code'] for i in _x.children if i.name=='status']
       try: new_nick = _item['nick']
       except: new_nick = '[unknown nick]'
       if '303' in _status: leave_type = 3
       elif '301' in _status: leave_type = 2
       elif '307' in _status: leave_type = 1
       else: leave_type = 0
       if leave_type == 0:
        try: reason = [i for i in x.children if i.name=='status'][0].children[0]
        except: reason = ''
       else:
        try: reason = [i for i in _item.children if i.name=='reason'][0].children[0]
        except: reason = ''
      except:
       self.bot.log.err(u"Got invalid presence from '%s'?\n%s: %s<br/><font color=grey>%s</font>" % (x['from'], escape(repr(sys.exc_info()[0])), escape(repr(sys.exc_info()[1])), escape(x.toXml())))
       leave_type = 0
       reason = ''
      if leave_type == 3: #if item changes nickname
       reason = item.nick
       item.jid = u'%s/%s' % (groupchat.jid, new_nick)
       item.nick = new_nick
       groupchat[new_nick] = item
      self.bot.call_leave_handlers(item, leave_type, reason)
      if config.ROOM_LIMIT:
       if (item.nick == self.get_nick(groupchat.jid)) and (leave_type <> 3): self.leave(groupchat.jid)
     else:
      #error
      self.bot.log.err(u'unknown error presence: ' + escape(x.toXml()))
    else:
     if typ == 'error':
      # check error code
      error = [q for q in x.elements() if q.name=='error']
      if error: code = error[0]['code']
      else: code = None
      if '409' in code: self.join(groupchat.jid, '%s-%s' % (nick, randint(1,100)))
      if '503' in code: pass
      if not code is None:
       if code == '': pass
       else: pass
       gj = groupchat.joiner
       if gj:
        self.bot.log.log(u'reporting to %s about failed joining..' % \
        (escape(gj[0].jid), ), 6)
        gj[0].lmsg(gj[1], 'join_failed', groupchat.jid, nick)
        groupchat.joiner = None
       if x['from'].endswith(self.get_nick(groupchat.jid)) and config.ROOM_LIMIT:
        self.bot.log.log_e(u'leave because of error presence from %s\nstanza:\n%s' % \
        (x['from'], x.toXml()), 7)
        self.leave(groupchat.jid, 'error presence...', True)
      else: self.bot.log.err(u'unexpected error presence from %s\nstanza:\n%s' % \
            (escape(x['from']), escape(x.toXml())))
     else: self.bot.log.err(u'unexpected unavailable presence from %s\nstanza:\n%s' % \
           (escape(x['from']), escape(x.toXml())))
  else:
   if typ in ('subscribe', 'subscribed', 'unsubscribe', 'unsubscribed'):
    p = domish.Element(('jabber:client', 'presence'))
    p['type'] = typ
    p['to'] = x['from']
    self.bot.wrapper.send(p)
    self.bot.log.log('ROSTER: %s - %s' % (typ, p['to']), 5)

 def get_nick(self, groupchat):
  return options.get_option(groupchat, 'nick', config.NICK)

 def set_nick(self, groupchat, nick):
  options.set_option(groupchat, 'nick', nick)

 def join(self, groupchat, nick=None):
  if nick == None: nick = self.get_nick(groupchat)
  else: self.set_nick(groupchat, nick)
  groupchat = groupchat.replace('\n', '')
  groupchat = self.bot.g.setdefault(groupchat, new_room(self.bot, groupchat))
  p = domish.Element(('jabber:client', 'presence'))
  p['to'] = u'%s/%s' % (groupchat.jid, nick)
  p.addElement('status').addContent(options.get_option(groupchat.jid, 'status', \
  config.STATUS).replace('%VERSION%', self.bot.version_version))
  p.addElement('x', 'http://jabber.org/protocol/muc').addElement('history').__setitem__('maxchars', '0')
  self.bot.wrapper.send(p)
  q = self.load_groupchats()
  if not (groupchat.jid in q): self.dump_groupchats(q+[groupchat.jid])
  return groupchat

 def leave(self, groupchat, reason = 'leave', config_only = False):
  if not config_only:
   p = domish.Element(('jabber:client', 'presence'))
   p['to'] = u'%s/%s' % (groupchat, self.get_nick(groupchat))
   p['type'] = 'unavailable'
   p.addElement('status').addContent(reason)
   self.bot.wrapper.send(p)
  q = self.load_groupchats()
  if groupchat in q:
   q.remove(groupchat)
   self.dump_groupchats(q)
  self.bot.g.pop(groupchat, None)

 def offline(self, reason):
  p = domish.Element(('jabber:client', 'presence'))
  p['type'] = 'unavailable'
  p.addElement('status').addContent(reason)
  self.bot.wrapper.send(p)

 def load_groupchats(self):
  try:
   f = file(self.g_file, 'r')
   g = f.read().decode('utf8').split(u'\n')
   f.close()
  except: g = []
  return [i.strip() for i in g if i]

 def dump_groupchats(self, groupchats):
  f = file(self.g_file, 'w')
  f.write(u'\n'.join(groupchats).encode('utf8'))
  f.close()
