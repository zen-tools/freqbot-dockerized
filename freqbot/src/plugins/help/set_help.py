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

def set_help_handler(t, s, p):
 if p.count('='):
  n = p.find('=')
  k = p[:n].strip()
  v = u'%s\n' % (p[n+1:].strip(), )
  v = v.encode('utf8')
  fn = u'doc/help/%s-%s.txt' % (k, lang.getLang(s.jid))
  fp = file(fn.encode('utf8'), 'w')
  fp.write(v)
  fp.close()
  reactor.callFromThread(initialize_help)
  s.lmsg(t, 'help_saved')
 else: s.syntax(t, 'set_help')

bot.register_cmd_handler(set_help_handler, '.set_help', 50)
