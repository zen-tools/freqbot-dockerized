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
def test_handler(t, s, p):
 if p: s.syntax(t, 'test')
 else: s.lmsg(t, 'test.passed')

bot.register_cmd_handler(test_handler, '.test')

def test_jid_handler(t, s, p):
 if s.jid <> s.realjid:
  bot.muc.msg('chat', s.realjid, lang.msg('test.passed', [], l=lang.getLang(s.realjid)))
 else: s.lmsg(t, 'censor_nojid')

bot.register_cmd_handler(test_jid_handler, '.test_jid')
