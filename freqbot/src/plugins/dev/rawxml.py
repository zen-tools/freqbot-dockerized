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
def rawxml(x):
 if not os.access(config.RAWXML, os.F_OK):
  fp = open(config.RAWXML, 'w')
  fp.write('<rawxml>\n\n')
  fp.close()
 try:
  f = config.RAWXML
  f = open(f, 'a')
  f.write('<receive time=\'%s\'>\n%s\n</receive>\n\n' % (time.strftime('%d:%m:%y %H:%M:%S'), x.toXml().encode('utf8')))
  f.close()
 except: pass

if config.RAWXML:
 bot.wrapper.c.addBootstrap(xmlstream.STREAM_AUTHD_EVENT, lambda x: bot.wrapper.x.addObserver('/*', rawxml))
