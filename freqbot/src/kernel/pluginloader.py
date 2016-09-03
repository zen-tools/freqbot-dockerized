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
import sys
import config

PLUGINS_DIR = config.PLUGINS_DIR

class pluginloader:
 def __init__(self, bot):
  self.bot = bot
  self.env = bot.env
  self.pluginlist = os.listdir(PLUGINS_DIR)
 
 def load_all(self):
  sys.stdout.write('Loading plugins: ')
  for i in self.pluginlist:
   self.load(i)
  print ' done.'
 
 def load(self, p):
  tl = os.listdir(PLUGINS_DIR+'/'+p)
  tl = [i for i in tl if i.endswith('.py')]
  for i in tl:
   fn = '%s/%s/%s' % (PLUGINS_DIR, p, i);
   fp = file(fn, 'r')
   pc = fp.read()
   fp.close()
   if config.ENABLE_SQLITE or not pc.count('__NEED_DB__'):
    try:
     exec pc in self.env
    except:
     sys.stderr.write('\nCan\'t load plugin %s:\n' % (fn, ))
     raise
    sys.stdout.write('+')
   else:
    #this plugin needs database, but it is disabled
    sys.stdout.write('s')
