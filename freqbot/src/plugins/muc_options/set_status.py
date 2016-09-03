#!/usr/bin/env python
# -*- coding: utf8 -*-
#~#######################################################################
#~ Copyright (c) 2008 Burdakov Daniel <kreved@kreved.org>               #
#~ Modifications: 2010 Timur Timirkhanov <timur@timirkhanov.kz>         #
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
def set_status_handler(t, s, p):
 allowed_shows = ('online', 'away', 'xa', 'dnd', 'chat')
 if p:
  pt = p.partition(' ')
  if (pt[1] == ''):
   if pt[0] in allowed_shows:
    show = pt[0]
    if show == 'online': show = ''
    s.room.set_option('show', show)
    s.room.set_option('status', '')
   else:
    s.room.set_option('status', p)
  else:
   if pt[0] in allowed_shows:
    show = pt[0]
    if show == 'online': show = ''
    s.room.set_option('show', show)
    s.room.set_option('status', pt[2])
   else:
    s.room.set_option('status', p)
  s.room.rejoin()
  s.lmsg(t, 'status_updated')
 else: s.syntax(t, 'set_status')

bot.register_cmd_handler(set_status_handler, '.set_status', 8, 1)
