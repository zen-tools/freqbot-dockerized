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

def passive():
 r = 'null'
 q = 999
 for i in bot.g.keys():
  p = len(bot.g[i].items)
  if p < q:
   r = i
   q = p
 return r

from twisted.internet import task

def cleanup_handler():
 if bot.authd == 0: return
 bot.log.log('muc cleanup...', 2)
 q = len(bot.g) - config.ROOM_LIMIT
 while q > 0:
  bot.muc.leave(passive(), 'MUC cleanup plugin')
  q -= 1

if config.ROOM_LIMIT:
 l = task.LoopingCall(cleanup_handler)
 l.start(60)

def passive_handler(t, s, p):
 p = passive()
 s.msg(t, '%s (%s)' % (p, len(bot.g.get(p, {}).items)))

bot.register_cmd_handler(passive_handler, '.passive')
