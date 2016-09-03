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
def info_handler(t, s, p):
 ut = time2str(time.time() - BOOTUP_TIMESTAMP, True, lang.getLang(s.jid))
 mc = float(INFO[0][0]+INFO[1][0]+INFO[2][0]+INFO[3][0])/240
 sc = float(INFO[0][1]+INFO[1][1]+INFO[2][1]+INFO[3][1])/240
 if not mc: mc = 0.001
 s.lmsg(t, 'info', bot.version_name, bot.version_version, ut, '%0.2f' % (mc, ), int(sc/mc))

bot.register_cmd_handler(info_handler, '.info')
