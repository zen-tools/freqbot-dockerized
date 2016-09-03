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

def ping_handler(t, s, p):
 jid = get_jid(s, p)
 typ = get_type(s, p)
 tpl = (jid, get_nick(jid), lang.get('from_you', l=lang.getLang(s.jid)), lang.get('from_me', l=lang.getLang(s.jid)))[typ]
 packet = IQ(bot.wrapper.x, 'get')
 packet.addElement('query', 'jabber:iq:version')
 packet.addCallback(ping_result_handler, t, s, p, tpl, time.time(), typ)
 reactor.callFromThread(packet.send, jid)

def ping_result_handler(t, s, p, tpl, ping_time, typ, x):
 if x['type'] == 'error':
  describe_error(t, s, x, typ)
 elif x['type'] == 'result':
  pong_time = time.time()
  s.lmsg(t, 'pong', tpl, time2str(pong_time-ping_time, False, lang.getLang(s.jid)))
 else: pass

bot.register_cmd_handler(ping_handler, '.ping')

