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

def vcard_handler(t, s, p):
 q = p.split()
 if q and q[0].startswith('-'):
  r = q[0][1:].upper().split(',')
  p = p[len(q[0])+1:]
 else:
  r = config.VCARD_FIELDS.split(',')
 jid = get_jid(s, p)
 packet = IQ(bot.wrapper.x, 'get')
 packet.addElement('vCard', 'vcard-temp')
 packet.addCallback(vcard_result_handler, t, s, p, r)
 reactor.callFromThread(packet.send, jid)

def vcard_result_handler(t, s, p, r, x):
 if x['type'] == 'result':
  try: vcard = parse_vcard(element2dict(x)['vCard'])
  except KeyError:
   s.lmsg(t, 'vcard_does_not_exists')
   return
  for i in vcard.keys():
   q = i.split('/')
   q = [j for j in q if j in r]
   if (not q and not('*' in r)) or i.count('BINVAL'): vcard.pop(i)
  res = [u'%s: %s' % (vcard_describe(i, s.get_lang()), vcard[i]) for i in vcard.keys() if vcard[i].strip()]
  if res: s.msg(t, 'vCard:\n' + '\n'.join(res))
  else: s.lmsg(t, 'vcard_not_found')
 else:
  describe_error(t, s, x, 0)

bot.register_cmd_handler(vcard_handler, '.vcard')

