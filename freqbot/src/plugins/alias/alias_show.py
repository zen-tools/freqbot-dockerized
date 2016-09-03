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
def alias_show_handler(t, s, p):
 alias_check(s.room.jid)
 q = ALIASES[s.room.jid].items()
 if q:
  q = [i[1].string() for i in q]
  if p: q = [i for i in q if i.count(p)]
  if q: s.msg(t, show_list(q))
  else: s.lmsg(t, 'alias_not_found')
 else: s.lmsg(t, 'alias_empty')

bot.register_cmd_handler(alias_show_handler, '.alias_show', 8, 1)
