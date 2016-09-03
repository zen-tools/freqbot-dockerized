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

def alias_add_handler(t, s, p):
 if p.count('='):
  a = p[:p.find('=')].lower().strip()
  command = p[p.find('=')+1:].strip()
  if p.count('\n'): s.syntax(t, 'alias_add')
  else:
   if not(alias) or not(p):
    s.syntax(t, 'alias_add')
   else:
    n = alias(a, command)
    if n.invalid: s.syntax(t, 'alias_add')
    elif n.security: s.lmsg(t, 'alias_security')
    else:
     if not n.with_access:
      alias_set(s.room.jid, n)
      s.lmsg(t, 'alias_saved')
     else:
      if s.allowed(n.a2):
       alias_set(s.room.jid, n)
       s.lmsg(t, 'alias_saved_with_access', n.a1, n.a2)
      else: s.lmsg(t, 'alias_no_access')
 else: s.syntax(t, 'alias_add')

bot.register_cmd_handler(alias_add_handler, '.alias_add', 8, 1)
