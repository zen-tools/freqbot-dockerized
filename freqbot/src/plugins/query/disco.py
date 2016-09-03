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
def disco_handler(t, s, p):
 if p:
  if p.count(' '):
   n = p.find(' ')
   p, grep = p[:n], p[n+1:]
  else: p, grep = p, ' '
  packet = IQ(bot.wrapper.x, 'get')
  packet.addElement('query', 'http://jabber.org/protocol/disco#items')
  packet.addCallback(disco_result_handler, t, s, p, grep)
  reactor.callFromThread(packet.send, p)
 else: s.syntax(t, 'disco')

def disco_result_handler(t, s, p, grep, x):
 if x['type'] == 'result':
  query = element2dict(x)['query']
  query = [i.attributes for i in query.children if i.__class__==domish.Element]
  if p.count('conference.') or p.count('chat.') or p.count('muc.'):
   if p.count('@'):
    r = [i.get('name') for i in query]
    r.sort()
   else:
    r = []
    for i in query:
     try: g = re.search('^(.+)\(([0-9]+)\)$', i['name']).groups()
     except: g = (i['name'], '0')
     if int(g[1]) < 99: r.append((g[0], i['jid'], g[1]))
    r.sort(lambda x, y: cmp(int(y[2]), int(x[2])))
    r = ['%s - %s (%s)' % i for i in r]
  else:
   r = [i['jid'] for i in query]
   r.sort()
  if r: s.msg(t, show_list(r, grep))
  else: s.lmsg(t, 'disco_empty')
 else:
  describe_error(t, s, x, 0)

bot.register_cmd_handler(disco_handler, '.disco')

