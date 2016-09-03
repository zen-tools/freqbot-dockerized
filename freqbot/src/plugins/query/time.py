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

from datetime import datetime
from datetime import timedelta

def time_handler(t, s, p):
 jid = get_jid(s, p)
 packet = IQ(bot.wrapper.x, 'get')
 packet.addElement('time', 'urn:xmpp:time')
 packet.addCallback(time_result_handler, t, s, get_nick(jid))
 reactor.callFromThread(packet.send, jid)

def old_time_handler(t, s, p):
 jid = get_jid(s, p)
 packet = IQ(bot.wrapper.x, 'get')
 packet.addElement('query', 'jabber:iq:time')
 packet.addCallback(old_time_result_handler, t, s, get_nick(jid))
 reactor.callFromThread(packet.send, jid)

def old_time_result_handler(t, s, p, x):
 try:
  query = element2dict(x)['query']
  display = element2dict(query)['display']
  s.msg(t, display.children[0])
 except:
  s.lmsg(t, 'time_error')
 
def time_result_handler(t, s, p, x):
 try:
  query = element2dict(x)['time']
  tzo = element2dict(query)['tzo'].children[0]
  utc = element2dict(query)['utc'].children[0]
  try:
    [sign, tzh, tzm] = re.match('(\+|-)?([0-9]+):([0-9]+)',tzo).groups()
    utc_time = datetime.strptime(utc, '%Y-%m-%dT%H:%M:%SZ')
    zone = timedelta(hours=int(tzh), minutes=int(tzm))
  except:
    s.msg(t, 'Unknown time format')
    return
  if sign == '-':
   local_time = utc_time - zone
  else:
   if sign == '+':
    local_time = utc_time + zone
   else:
    local_time = utc_time
  s.msg(t, datetime.strftime(local_time, '%A %d.%m.%Y %H:%M:%S')+tzo)
 except:
  old_time_result_handler(t, s, p, x)

bot.register_cmd_handler(time_handler, '.time')
bot.register_cmd_handler(old_time_handler, '.time_old')

