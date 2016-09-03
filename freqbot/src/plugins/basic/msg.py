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

def echo_handler(t, s, p):
 if p: s.msg(t, context_replace(p, t, s))
 else: s.syntax(t, 'echo')

def say_handler(t, s, p):
 if p: s.room.msg(context_replace(p, t, s))
 else: s.msg(t, '?')

def globmsg_handler(t, s, p):
 if p:
  for i in bot.g.values():
   if i.bot: i.msg(context_replace(p, 'groupchat', i.bot))
   else: i.msg(p)
  s.lmsg(t, 'globmsg_sent', len([i for i in bot.g.keys() if i]))
 else: s.msg(t, '?')

def msg_handler(t, s, p):
 p = p.strip()
 if p.count(' '):
  jid, p, text = p.partition(' ')
  if jid in bot.g.keys(): typ = 'groupchat'
  else: typ = 'chat'
  bot.wrapper.msg(typ, jid, text)
  s.lmsg(t, 'sent')
 else: s.syntax(t, 'msg')

bot.register_cmd_handler(echo_handler, '.echo')
bot.register_cmd_handler(say_handler, '.say', 9, True)
bot.register_cmd_handler(globmsg_handler, '.globmsg', 99)
bot.register_cmd_handler(msg_handler, '.msg', 50)
