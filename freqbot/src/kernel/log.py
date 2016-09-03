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
import os
import time
import config
import lang
from twisted.web.html import escape

class logger:

 def __init__(self):
  self.pid = str(os.getpid())
  self.version = '?'

 def _log(self, fn, m, h):
  if not os.access(fn, 0):
   fp = file(fn, 'w')
   fp.write(h.encode('utf8', 'replace'))
   fp.close()
  fp = file(fn, 'a')
  fp.write(m.replace(r'$PID$', self.pid).replace('$VERSION$', \
  self.version).encode('utf8', 'replace'))
  fp.close()

 def log(self, m, level=9):
  if level >= config.LOGLEVEL: self._log(config.LOGFILE, time.strftime(lang.get('log.record')) % (m, ), lang.get('log.header'))

 def err(self, m):
  self._log(config.ERRLOGFILE, time.strftime(lang.get('log.record')) % (m, ), lang.get('log.header'))

 def err_e(self, m):
  self.err(escape(m))

 def log_e(self, m, level=9):
  self.log(escape(m), level)
