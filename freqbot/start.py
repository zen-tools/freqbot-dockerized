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

import sys
from twisted.words.protocols.jabber import xmlstream
from twisted.words.protocols.jabber.client import IQ
from twisted.internet.defer import Deferred as D
from twisted.web.html import escape
import traceback
import re
from twisted.internet import reactor
import os
import time
import sqlite3

os.environ['TZ'] = 'Europe/Kiev'
time.tzset()

wd = os.path.dirname(sys.argv[0])
if not wd: wd = '.'
os.chdir(wd)
sys.path.insert(0, 'src/kernel')
sys.path.insert(0, 'modules')
#print 'sys.path is %s' % (sys.path, )

import config

if len(sys.argv) > 1: cfg = sys.argv[1]
else: cfg = './freqbot.conf'
print 'Using %s as config file' % (cfg, )
config.init(cfg)

 
if config.ENABLE_SQLITE:
 try: import db
 except:
  config.ENABLE_SQLITE = False
  sys.stdout.write('Can\'t use db..\n')

tm = int(time.time()) + config.RESTART_INTERVAL
# we should not restart until time.time() == tm

pid = str(os.getpid())

try:
 fp = file(config.PIDFILE, 'r')
 p = fp.read()
 fp.close()
 if p <> pid:
  os.kill(int(p), 3)
  time.sleep(1)
  try: os.kill(int(p), 9)
  except: pass
  sys.stdout.write('pid %s killed.. ' % (p, ))
except: pass

fp = file(config.PIDFILE, 'w')
fp.write(pid)
fp.close()

from freq import freqbot
import lang
import options
from options import optstringlist

bot = freqbot(globals())

if config.DBDIR==None or False: config.DBDIR = config.DATADIR
if os.path.isfile('%s/%s' % (config.DBDIR,'wtf.db')): pass
else: 
 cn = sqlite3.connect('%s/%s' % (config.DBDIR,'wtf.db'))
 cr = cn.cursor()
 cr.execute('create table wtf (room text, key text, val text)')
 cn.commit()
 cn.close()
 bot.log.log_e('Create wtf database: %s/wtf.db'%config.DBDIR)

try:
 bot.plug.load_all()
 reactor.run()
except:
 bot.log.err(escape('FATAL ERROR: %s' % (traceback.format_exception(sys.exc_type, sys.exc_value, sys.exc_traceback), )))

def log(m, e=False):
 bot.log.log(m)
 if e: bot.log.err(m)

def restart():
 cmd = config.RESTART_CMD
 log(escape('restart now: %s' % (cmd, )))
 os.execv(cmd.split()[0], tuple(cmd.split()))

if bot.smart_shutdown:
 log('freQ-bot normally stopped')
 if bot.want_restart: restart()
elif not config.RESTART_INTERVAL:
 log('freQ-bot fault (restart disabled)', True)
else:
 log('freQ-bot fault (restarting...)', True)
 tm = tm - int(time.time())
 if tm > 0:
  log('wait %s seconds...' % (tm, ))
  time.sleep(tm)
 restart()
