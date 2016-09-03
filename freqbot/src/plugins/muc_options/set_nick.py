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
def set_nick_handler(t, s, p):
 p = p.strip().replace('/', '(slash)')[:30].replace('\n', '')
 if p in s.room.keys(): s.lmsg(t, 'nick_in_use')
 elif p:
  s.room.set_option('nick', p)
  s.room.rejoin()
  s.lmsg(t, 'nick_updated')
 else: s.syntax(t, 'set_nick')

bot.register_cmd_handler(set_nick_handler, '.set_nick', 8, 1)
