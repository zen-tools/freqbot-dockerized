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

def stop_handler(t, s, p):
 p = p.strip()
 s.lmsg(t, 'stopping')
 if p: bot.stop('.stop command from bot owner (%s)' % (p, ))
 else: bot.stop('.stop command from bot owner')

bot.register_cmd_handler(stop_handler, '.stop', 50)


def restart_handler(t, s, p):
 p = p.strip()
 s.lmsg(t, 'restarting')
 if p: bot.stop('.restart command from bot owner (%s)' % (p, ), True)
 else: bot.stop('.restart command from bot owner', True)

bot.register_cmd_handler(restart_handler, '.restart', 50)
