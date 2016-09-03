#!/usr/bin/env python
# -*- coding: utf8 -*-
#~#######################################################################
#~ Copyright (c) 2008 Burdakov Daniel <kreved@kreved.org>               #
#~ Copyright (c) 2010 Alexandr Kazakov <ferym@jabber.ru>                #
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
import urllib2, re, popen2

def update_handler(typ, source, params):
 if params==u'info':
  i = urllib2.urlopen('http://cvs.berlios.de/svnroot/repos/freq-dev/trunk/').read()
  exp='.*?(\\d+)'
  rg = re.compile(exp,re.IGNORECASE|re.DOTALL)
  m = rg.search(i)
  if m:
    rev=m.group(1)
    pipe = os.popen('sh -c "LANG=%s svn log %s --limit 1" 2>&1' % (config.SH_LANG,"svn://svn.berlios.de/freq-dev/trunk", ))
    time.sleep(1)
    ms = clear_text(pipe.read().decode('utf8', 'replace'))
    ml = ms.splitlines()
    ms = '\n'.join(line.strip() for line in ml if line.strip() and not line.startswith('-----'))
    if not bot.getVer().count(rev):
        source.lmsg(typ,'update_info', bot.getVer().split('.')[-1],rev+"\n========== INFO =========\n"+ms)
    else: source.lmsg(typ,'update_info', bot.getVer().split('.')[-1],rev)
  return
 if params==u'start':
  if os.name=='posix':
   cmd = "bash -c 'LANG=%s svn up' 2>&1"%(config.SH_LANG)
   p = popen2.Popen3(cmd, True)
   while p.poll() == -1: pass
   source.msg(typ, ''.join(p.fromchild.readlines()).decode('utf-8'))
   time.sleep(2)
   bot.stop('.update command from bot owner', True)
   return
 else: source.lmsg(typ,'invalid_syntax_default')

bot.register_cmd_handler(update_handler,'.update',100)
