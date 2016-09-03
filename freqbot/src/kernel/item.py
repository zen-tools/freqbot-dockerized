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
import lang
import time

class item:

 def __init__(self, bot, room=None):
  self.bot = bot
  self.handled = None
  self.room = room
  self.jid = None
  self.realjid = None
  self.nick = None
  self.role = None
  self.affiliation = None
  self.joined = time.time()
  self.status = None
  self.show = None
  self.ACC = None

 def msg(self, typ, body):
  if (typ=='groupchat') and self.room and (len(body)>self.room.get_msglimit()):
   self.bot.muc.msg(typ, self.jid, self.get_msg('see_private'))
   typ = 'chat'
  if typ in ['chat', 'groupchat', 'normal']: self.bot.muc.msg(typ, self.jid, body)
  elif typ == 'null': pass
  elif typ.startswith('redirect:'):
   nick = typ[9:]
   if self.room and (nick in self.room.keys()):
    self.room[nick].msg('chat', body)
   else: raise ValueError('can\'t send redirect:* msg')
  else: raise ValueError('invalid typ: '+typ)

 def get_lang(self):
  return lang.getLang(self.jid)

 def get_msg(self, template, params=()):
  return lang.msg(template, params, self.get_lang())

 def lmsg(self, typ, template, *params):
  self.msg(typ, self.get_msg(template, params))

 def syntax(self, typ, text):
  self.bot.muc.invalid_syntax(typ, self, text)

 def access(self):
  if self.ACC == None: return self.bot.muc.get_access(self)
  else: return self.ACC

 def allowed(self, required_access):
  return self.access() >= required_access

 def can_kick(self, item):
  return (self.access()>4) and (item.access()<5)

 def can_visitor(self, item):
  return self.can_kick(item) or ((self.access()>8) and (item.access()<8))

 def can_participant(self, item):
  return self.can_visitor(item)

 def can_moderator(self, item):
  return self.access() > 8

 def can_ban(self, item):
  return ((self.access()>8) and (item.access()<8)) or ((self.access()>10) and (item.access()<12))

 def can_none(self, item):
  return self.can_ban(item)

 def can_member(self, item):
  return self.can_ban(item)

 def can_admin(self, item):
  return self.access()>10

 def can_owner(self, item):
  return self.access()>10

 def config_jid(self):
  if self.room: return self.room.jid
  else: return self.jid.split('/')[0] # bare jid

def item_x(i, access):
 # IMHO this function is not pure, but i don't know how to do it better //kreved
 r = item(i.bot, i.room)
 #print 'item_x(i=..'
 #print i
 #print access
 r.jid = i.jid
 r.realjid = i.realjid
 r.nick = i.nick
 r.role = i.role
 r.affiliation = i.affiliation
 r.joined = i.joined
 r.status = i.status
 r.show = i.show
 r.ACC = access
 #print 'r.ACC'
 #print r
 #print r.ACC
 return r
