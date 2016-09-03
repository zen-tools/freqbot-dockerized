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

def join_handler(t, s, p):
 p = p.strip()
 p = p.replace('\n', '')
 if not p: s.syntax(t, 'join')
 else:
   if p.count('#'):
    p_part = p.partition('#')
    password = p_part[2].strip()
    p = p_part[0]
   else:
    password = None
   if p.count('/'):
    p_part = p.partition('/')
    groupchat = p_part[0]
    nick = p_part[2].strip()
   else:
    groupchat = p
    nick = config.NICK
   groupchat = groupchat.lower()
   if groupchat in bot.g.keys(): s.lmsg(t, 'join_already_there')
   else:
    q = blacklist_load()
    gserver = groupchat.split('@')[-1]
    if q.has_key(groupchat) or q.has_key(gserver):
     if q.has_key(groupchat): tm, reason = q[groupchat]
     else: tm, reason = q[gserver]
     if reason: m = s.get_msg('join_not_permitted_reason', (groupchat, reason))
     else: m = s.get_msg('join_not_permitted', (groupchat, ))
     m = dump_time(tm, m, True, s)
     s.msg(t, m)
    else:
     g = bot.muc.join(groupchat, nick, password)
     g.joiner = (s, t)
     bot.log.log_e(u'joining %s (asked by %s)' % (p, s.jid), 5)

bot.register_cmd_handler(join_handler, '.join', config.JOIN_ACCESS)
