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

ACCESS_LISTS = options.optstringlist('access_lists')

def get_access(groupchat, jid):
 jid = jid.lower()
 l = [access_parse(item) for item in ACCESS_LISTS[groupchat]]
 l = [item['access'] for item in l if item['jid'] == jid]
 if len(l) == 0: return None
 elif len(l) == 1: return l[0]
 else: bot.log.err_e('troubles with access_lists in room %s, jid=%s' % (groupchat, jid))

def access_parse(text):
 p = text.split()
 return {'jid': p[0].lower(), 'access': int(p[1])}

def access_add(t, s, p):
 p = p.lower()
 try: j = access_parse(p)
 except:
  s.lmsg(t, 'access_add_invalid_syntax')
  return
 k = get_access(s.room.jid, j['jid'])
 if k == None: acc = j['access']
 else: acc = max(j['access'], k)
 if s.allowed(acc):
  l = [item for item in ACCESS_LISTS[s.room.jid] if access_parse(item)['jid'] <> j['jid']]
  l.append(p)
  ACCESS_LISTS[s.room.jid] = l
  s.lmsg(t, 'access_added')
 else: s.lmsg(t, 'not_allowed')

def access_del(t, s, p):
 p = p.lower()
 if not p:
  s.syntax(t, 'access_del')
  return
 acc = get_access(s.room.jid, p)
 if acc == None:
  s.lmsg(t, 'access_del_404')
 elif s.allowed(acc):
  l = [item for item in ACCESS_LISTS[s.room.jid] if access_parse(item)['jid'] <> p]
  ACCESS_LISTS[s.room.jid] = l
  s.lmsg(t, 'access_deleted')
 else: s.lmsg(t, 'not_allowed')

def access_clear(t, s, p):
 ACCESS_LISTS[s.room.jid] = []
 s.lmsg(t, 'access_cleared')

def access_show(t, s, p):
 p = p.lower()
 l = ACCESS_LISTS[s.room.jid]
 if l: s.msg(t, show_list(l, p, 'not found'))
 else: s.lmsg(t, 'access_list_empty')

def access_add_global(t, s, p):
 p = p.lower()
 try: j = access_parse(p)
 except:
  s.lmsg(t, 'access_add_invalid_syntax')
  return
 l = [item for item in ACCESS_LISTS['global'] if access_parse(item)['jid'] <> j['jid']]
 l.append(p)
 ACCESS_LISTS['global'] = l
 s.lmsg(t, 'access_added')

def access_del_global(t, s, p):
 p = p.lower()
 if not p:
  s.syntax(t, 'access_del')
  return
 acc = get_access('global', p)
 if acc == None:
  s.lmsg(t, 'access_del_404')
 else:
  l = [item for item in ACCESS_LISTS['global'] if access_parse(item)['jid'] <> p]
  ACCESS_LISTS['global'] = l
  s.lmsg(t, 'access_deleted')

def access_clear_global(t, s, p):
 ACCESS_LISTS['global'] = []
 s.lmsg(t, 'access_cleared')

def access_show_global(t, s, p):
 p = p.lower()
 l = ACCESS_LISTS['global']
 if l: s.msg(t, show_list(l, p, 'not found'))
 else: s.lmsg(t, 'access_list_empty')

def rewrite_access(item, old_access):
 q = get_access('global', item.realjid)
 if q <> None: return q
 if item.room:
  q = get_access(item.room.jid, item.realjid)
  if q == None: return old_access
  else: return q
 else: return old_access

bot.register_cmd_handler(access_add, '.access_add', 11, True)
bot.register_cmd_handler(access_del, '.access_del', 11, True)
bot.register_cmd_handler(access_clear, '.access_clear', 11, True)
bot.register_cmd_handler(access_show, '.access_show', 9, True)
bot.register_cmd_handler(access_add_global, '.access_add_global', 50)
bot.register_cmd_handler(access_del_global, '.access_del_global', 50)
bot.register_cmd_handler(access_clear_global, '.access_clear_global', 50)
bot.register_cmd_handler(access_show_global, '.access_show_global', 50)
bot.register_access_modificator(rewrite_access)
