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
def enable_noisy(t, s, p):
 if s.room.get_option('noisy', 'off') == 'on': s.lmsg(t, 'noisy_already_on')
 else:
  s.room.set_option('noisy', 'on')
  s.lmsg(t, 'ok')

def disable_noisy(t, s, p):
 if s.room.get_option('noisy', 'off') == 'off': s.lmsg(t, 'noisy_already_off')
 else:
  s.room.set_option('noisy', 'off')
  s.lmsg(t, 'ok')

bot.register_cmd_handler(enable_noisy, '.enable_noisy', 9, 1)
bot.register_cmd_handler(disable_noisy, '.disable_noisy', 9, 1)

# leave_type: 0: leave
#             1: kick
#             2: ban
#             3: rename

def noisy_join_handler(item):
 if (item.room.get_option('noisy', 'off') == 'on') and item.room.bot and (item.nick <> item.room.bot.nick):
  item.room.lmsg('noisy_join', item.nick)

def noisy_leave_handler(item, leave_type, reason):
 if item.room.get_option('noisy', 'off') == 'on':
  pattern = ('noisy_leave', 'noisy_kick', 'noisy_ban', 'noisy_rename')[leave_type]
  if leave_type<3: item.room.lmsg(pattern, item.nick, reason)
  else: item.room.lmsg(pattern, item.nick)

bot.register_leave_handler(noisy_leave_handler)
bot.register_join_handler(noisy_join_handler)
