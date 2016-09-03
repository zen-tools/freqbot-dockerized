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

def chatlogs_passwd_handler(t, s, p):
 p = p.strip()
 PATH = config.CHATLOGS_DIR + '/' + s.room.jid + '/'
 if os.access(PATH, os.W_OK):
  if p == 'clear':
   try: os.remove(PATH + '.htaccess')
   except OSError: pass
   try: os.remove(PATH + '.htpasswd')
   except OSError: pass
   s.lmsg(t, 'cleared')
  else:
   p = p.split()
   if len(p) == 2:
    f = file(PATH + '.htaccess', 'w')
    f.write('AuthType Basic\nAuthName "Ask room owner for the username/password"\n' + \
    'AuthUserFile %s.htpasswd\nrequire valid-user' % (PATH, ))
    f.close()
    user = my_quote(p[0])
    passwd = my_quote(p[1])
    PF = my_quote(PATH + '.htpasswd')
    # no vulnerability, because all parameters are quoted with ""
    cmd = u'htpasswd -bmc %s %s %s 2>&1' % (PF, user, passwd)
    cmd = cmd.encode('utf8')
    pipe = os.popen(cmd)
    time.sleep(1)
    m = pipe.read().decode('utf8', 'replace')
    s.msg(t, m)
   else: s.syntax(t, 'chatlogs_passwd')
 else: s.lmsg(t, 'failed')

if config.CHATLOGS_ALLOW_PASSWD: passwd_access = 10
else: passwd_access = 50

bot.register_cmd_handler(chatlogs_passwd_handler, '.chatlogs_passwd', passwd_access, True)
