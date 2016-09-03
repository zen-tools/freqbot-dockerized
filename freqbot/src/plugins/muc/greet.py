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

def set_greet(t, s, p):
 p = p.strip()[:500]
 if p:
  if s.room.get_option('greeting'):
   s.room.set_option('greeting', p)
   s.lmsg(t, 'updated')
  else:
   s.room.set_option('greeting', p)
   s.lmsg(t, 'saved')
 else:
  if s.room.get_option('greeting'):
   s.room.set_option('greeting', '')
   s.lmsg(t, 'deleted')
  else: s.lmsg(t, 'nothing_to_delete')

def say_greet(item):
 if (item.access()<3) and item.room.get_option('greeting'):
  item.msg('chat', context_replace(item.room.get_option('greeting'), 'chat', item))

bot.register_cmd_handler(set_greet, '.set_greeting', 9, True)
bot.register_join_handler(say_greet)
