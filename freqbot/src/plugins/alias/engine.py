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
from item import item_x

def alias_engine(q):
 bot.log.log(escape(u'alias_engine called with command=%s' % (q, )), 1)
 t, source, text, stanza = q
 if source.room: groupchat = source.room.jid
 else: groupchat = source.jid
 params = text.split()
 if params:
  alias = params[0].lower()
  r = alias_get(groupchat, text)
  if r:
   r = r[0]
   s = r.command
   params = r.parse(text).split()
   #replacing %1, %2, %3... %*
   if r.with_access:
    if not source.allowed(r.a1):
     return [(t, source, '.echo '+lang.msg('alias_not_allowed', l=lang.getLang(source.jid)), stanza)]
    else:
     source = item_x(source, r.a2)
   for i in range(len(params)): s = s.replace('%%%s' % (i+1, ), params[i])
   s = s.replace('%*', r.parse(text))
   for i in range(len(params)): s = s.replace('%%Q%s' % (i+1, ), my_quote(params[i], True))
   s = s.replace('%Q*', my_quote(r.parse(text), True))
   s = context_replace(s, t, source)
   return [(t, source, s, stanza)]
  else: return False
 else: return False

ALIASES = {}

bot.register_rewrite_engine(alias_engine)
