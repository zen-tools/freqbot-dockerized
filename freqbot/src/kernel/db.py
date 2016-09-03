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
from sqlite3 import connect
from config import DATADIR
DBDIR = DATADIR + '/db'
if not os.access(DBDIR, os.F_OK): os.mkdir(DBDIR)

class database:
 def __init__(self, filename):
  self.db = connect('%s/%s.db' % (DBDIR, filename.encode('utf8', 'replace')))
  self.cursor = self.db.cursor()
 
 def __del__(self):
  if self.cursor: self.cursor.close()
  if self.db:
   self.db.commit()
   self.db.close()
 
 def query(self, *args, **kwargs):
  self.cursor.execute(*args, **kwargs)
  return self.cursor
 
 def commit(self):
  self.db.commit()
