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
def stats_handler(t, s, p):
 if p:
  packet = IQ(bot.wrapper.x, 'get')
  query = packet.addElement('query', 'http://jabber.org/protocol/stats')
  query.addElement('stat').__setitem__('name', 'users/total')
  query.addElement('stat').__setitem__('name', 'users/online')
  packet.addCallback(stats_result_handler, t, s, p)
  reactor.callFromThread(packet.send, p)
 else: s.syntax(t, 'stats')

def stats_result_handler(t, s, p, x):
 if x['type'] == 'result':
  query = element2dict(x)['query']
  r = {}
  for i in query.children:
   r[i['name']] = i['value']
  s.lmsg(t, 'stats_result', p, r.get('users/total', '?'), r.get('users/online', '?'))
 elif x['type'] == 'error':
  describe_error(t, s, x, 0)

bot.register_cmd_handler(stats_handler, '.stats')

