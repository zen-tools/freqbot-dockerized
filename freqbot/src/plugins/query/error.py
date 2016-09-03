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

# http://www.xmpp.org/rfcs/rfc3920.html#stanzas-error

def describe_error(typ, source, stanza, rtyp):
 if rtyp == 0: target = stanza['from']
 elif rtyp in [1, 2]: target = get_nick(stanza['from'])
 else: target = 'o_O'
 query = [x for x in stanza.elements() if x.name=='error'][0]
 conditions = [x for x in query.elements() if x.uri=='urn:ietf:params:xml:ns:xmpp-stanzas' and x.name <> 'text']
 if len(conditions) <> 1:
  return source.lmsg(typ, 'invalid_error_stanza', query.toXml())
 condition = conditions[0].name
 if condition == 'feature-not-implemented': source.lmsg(typ, 'e_feature-not-implemented', target)
 elif condition in ['forbidden', 'not-allowed']: source.lmsg(typ, 'e_forbidden', target)
 elif condition == 'gone': source.lmsg(typ, 'e_gone', target)
 elif condition == 'internal-server-error': source.lmsg(typ, 'e_internal-server-error', target)
 elif condition == 'item-not-found': source.lmsg(typ, 'not_found', target)
 elif condition == 'jid-malformed': source.lmsg(typ, 'e_jid-malformed', target)
 elif condition == 'recipient-unavailable': source.lmsg(typ, 'e_recipient-unavailable', target)
 elif condition == 'remote-server-not-found': source.lmsg(typ, 'e_remote-server-not-found', target)
 elif condition == 'remote-server-timeout': source.lmsg(typ, 'e_remote-server-timeout', target)
 elif condition == 'service-unavailable': source.lmsg(typ, 'e_service-unavailable', target)
 else: source.msg(typ, condition)
