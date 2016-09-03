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

def get_nick(jid):
 p = jid.find('/')
 return jid[p+1:]

def get_jid(source, p):
 if p:
  if source.room:
   if p in source.room.items.keys():
    return source.room[p].jid
   else: return p
  else: return p
 else: return source.jid

def get_type(s, p):
 jid = get_jid(s, p)
 if p == jid: return 0
 if s.room:
  if s.room.bot and (s.room.bot.jid==jid): return 3
  if s.jid == jid: return 2
  return 1
 else:
  if p: return 0
  else: return 2

def version_handler(t, s, p):
 packet = IQ(bot.wrapper.x, 'get')
 q = packet.addElement('query', 'jabber:iq:version')
 packet.addCallback(version_result_handler, t, s, p, get_type(s, p))
 reactor.callFromThread(packet.send, get_jid(s, p))

def version_result_handler(t, s, p, typ, x):
 if x['type'] == 'error':
  describe_error(t, s, x, typ)
 else:
  query = element2dict(x)['query']
  r = element2dict(query)
  if typ == 0:
   s.lmsg(t, 'version_result_jid', x['from'], r.get('name'), r.get('version'), r.get('os'))
  else:
   if typ == 1:
    s.lmsg(t, 'version_result_nick', get_nick(x['from']), r.get('name'), r.get('version'), r.get('os'))
   else:
    if typ == 2:
     s.lmsg(t, 'version_result_your', r.get('name'), r.get('version'), r.get('os'))
    else:
     s.lmsg(t, 'version_result_self', bot.version_name, bot.version_version, bot.version_os)

bot.register_cmd_handler(version_handler, '.version')

