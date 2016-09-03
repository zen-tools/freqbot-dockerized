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

BL = optstringlist('blacklist')

def blacklist_parse(s):
 """
 input: '/3m room@server reason'
 output: ('room@server', (1202281728, 'reason'))
 """
 tm, s = fetch_time(s)
 if s.count(' '):
  n = s.find(' ')
  return (s[:n], (tm, s[n+1:]))
 else: return (s, (tm, ''))

def blacklist_load():
 q = BL['global']
 p = [True for i in q if blacklist_parse(i)[1][0]<time.time()]
 if p:
  q = [i for i in q if blacklist_parse(i)[1][0]>time.time()]
  BL['global'] = q
 m = dict([blacklist_parse(i) for i in q])
 return m

def blacklist_dump(q):
 BL['global'] = [dump_time(q[room][0], u'%s %s' % (room, q[room][1])) for room in q.keys()]

def blacklist_add(t, s, p):
 p = p.strip().lower()
 if not p:
  s.syntax(t, 'blacklist_add')
  return
 q = blacklist_load()
 room, tmp = blacklist_parse(p)
 tm, reason = tmp
 q[room] = (tm, reason)
 blacklist_dump(q)
 if room in bot.g.keys(): bot.muc.leave(room, reason)
 s.lmsg(t, 'ok')

def blacklist_del(t, s, p):
 room = p.strip().lower()
 if not p:
  s.syntax(t, 'blacklist_del')
  return
 q = blacklist_load()
 if room in q.keys():
  q.pop(room)
  blacklist_dump(q)
  s.lmsg(t, 'blacklist_deleted')
 else: s.lmsg(t, 'blacklist_not_found')

def blacklist_clear(t, s, p):
 blacklist_dump({})
 s.lmsg(t, 'list_cleared')

def blacklist_show(t, s, p):
 q = blacklist_load()
 q = [dump_time(q[room][0], '%s %s' % (room, q[room][1]), True, s) for room in q.keys()]
 if q: s.msg(t, show_list(q, p, s.get_msg('not_found')))
 else: s.lmsg(t, 'list_empty')

bot.register_cmd_handler(blacklist_add, '.blacklist_add', 50)
bot.register_cmd_handler(blacklist_del, '.blacklist_del', 50)
bot.register_cmd_handler(blacklist_clear, '.blacklist_clear', 50)
bot.register_cmd_handler(blacklist_show, '.blacklist_show', 50)
