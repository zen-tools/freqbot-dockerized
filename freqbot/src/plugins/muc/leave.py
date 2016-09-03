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

def leave_handler(t, s, p):
 p = p.strip()
 if p.count(' '):
  n = p.find(' ')
  room, reason = p[:n], p[n+1:]
 else: room, reason = p, ''
 if room:
  room = room.lower()
  if s.allowed(50):
   if room in bot.g.keys():
    if not reason: reason = '".leave" command from bot owner'
    bot.muc.leave(room, reason)
    s.lmsg(t, 'leaved', room)
   else: s.lmsg(t, 'i_am_not_there')
  else: s.lmsg(t, 'not_allowed')
 else:
  if s.room: bot.muc.leave(s.room.jid, '".leave" command from bot owner')
  else: s.lmsg(t, 'muc_only')

bot.register_cmd_handler(leave_handler, '.leave', 50)
