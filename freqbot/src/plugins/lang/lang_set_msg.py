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
def lang_set_msg_handler(t, s, p):
 q = re.search('^(..)\ ([^\ \=]+)\=(.+)$', p, re.DOTALL)
 if not q:
  s.syntax(t, 'lang_set_msg')
  return
 q = q.groups()
 language = q[0]
 msg = q[1]
 value = q[2]
 if language in lang.languages():
  lang.set(msg, language, value)
  s.lmsg(t, 'lang_msg_saved')
 else:
  s.lmsg(t, 'lang_not_found', language)

bot.register_cmd_handler(lang_set_msg_handler, '.lang_set_msg', 40)
