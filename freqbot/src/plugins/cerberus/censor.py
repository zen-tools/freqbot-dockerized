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

CENSORLIST = optstringlist('censor')

def censor_list(t, s, p):
 q = CENSORLIST[s.room.jid]
 if q: s.msg(t, show_list(q, p))
 else: s.lmsg(t, 'censor_list_empty')

def censor_subscribe(t, s, p):
 q = CENSORLIST[s.room.jid]
 if s.jid <> s.realjid:
  jid = s.realjid
  if jid in q: s.lmsg(t, 'censor_already_subscribed')
  else:
   q.append(jid)
   s.lmsg(t, 'censor_subscribed', s.room.jid)
   bot.muc.msg('chat', jid, lang.msg('censor_subscribed', [s.room.jid], l=lang.getLang(s.room.jid)))
   CENSORLIST[s.room.jid] = q
 else: s.lmsg(t, 'censor_nojid')

def censor_unsubscribe(t, s, p):
 q = CENSORLIST[s.room.jid]
 if s.jid <> s.realjid:
  jid = s.realjid
  if not(jid in q): s.lmsg(t, 'censor_not_subscribed')
  else:
   q.remove(jid)
   s.lmsg(t, 'censor_unsubscribed', s.room.jid)
   bot.muc.msg('chat', jid, lang.msg('censor_unsubscribed', (s.room.jid, ), l=lang.getLang(s.room.jid)))
   CENSORLIST[s.room.jid] = q
 else: s.lmsg(t, 'censor_nojid')

def censor_handler(source, text, badword):
 q = CENSORLIST[source.room.jid]
 for jid in q:
  bot.muc.msg('chat', jid, lang.msg('censor', [source.room.jid, source.nick, source.realjid, badword, text], l=lang.getLang(source.room.jid)))

bot.register_bad_handler(censor_handler)
bot.register_cmd_handler(censor_list, '.censor_list', 9, g=1)
bot.register_cmd_handler(censor_subscribe, '.censor_subscribe', 9, g=1)
bot.register_cmd_handler(censor_unsubscribe, '.censor_unsubscribe', 9, g=1)
