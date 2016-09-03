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

jid_regexp = re.compile(u'^([^@\/]+@([a-z0-9-]+\.)+[a-z]{2,4})(\/.*)?$')

def m_parse(text):
 text = text.strip()
 if text.count('|'):
  n = text.find('|')
  return (text[:n], text[n+1:])
 else: return (text, '')

def moderate(t, s, p, nj, n_j, ra, set_to, reason):
 d = s.room.moderate(nj, n_j, ra, set_to, reason)
 d.addCallback(moderate_result_handler, t, s, p)

def moderate_result_handler(x, t, s, p):
 #print x.toXml()
 if x['type'] == 'result': s.lmsg(t, 'moderate_ok')
 else: s.lmsg(t, 'moderate_error')

def kick_handler(t, s, p):
 if p:
  #print m_parse(p)
  p, reason = m_parse(p)
  item = s.room.get(p)
  if item:
   moderate(t, s, p, 'nick', p, 'role', 'none', reason)
  else: s.lmsg(t, 'moderate_not_found')
 else: s.syntax(t, 'kick')

bot.register_cmd_handler(kick_handler, '.kick', 5, 1)


def visitor_handler(t, s, p):
 if p:
  #print m_parse(p)
  p, reason = m_parse(p)
  item = s.room.get(p)
  if item:
   if (not item.allowed(5)) or s.allowed(9):
    moderate(t, s, p, 'nick', p, 'role', 'visitor', reason)
   else: s.lmsg(t, 'not_allowed')
  else: s.lmsg(t, 'moderate_not_found')
 else: s.syntax(t, 'visitor')

bot.register_cmd_handler(visitor_handler, '.visitor', 5, 1)


def participant_handler(t, s, p):
 if p:
  #print m_parse(p)
  p, reason = m_parse(p)
  item = s.room.get(p)
  if item:
   if (not item.allowed(5)) or s.allowed(9):
    moderate(t, s, p, 'nick', p, 'role', 'participant', reason)
   else: s.lmsg(t, 'not_allowed')
  else: s.lmsg(t, 'moderate_not_found')
 else: s.syntax(t, 'participant')

bot.register_cmd_handler(participant_handler, '.participant', 5, 1)


def moderator_handler(t, s, p):
 if p:
  #print m_parse(p)
  p, reason = m_parse(p)
  item = s.room.get(p)
  if item:
   moderate(t, s, p, 'nick', p, 'role', 'moderator', reason)
  else: s.lmsg(t, 'moderate_not_found')
 else: s.syntax(t, 'moderator')

bot.register_cmd_handler(moderator_handler, '.moderator', 9, 1)


def admin_handler(t, s, p):
 if p:
  #print m_parse(p)
  p, reason = m_parse(p)
  item = s.room.get(p)
  if item:
   nj = 'nick'
   if (item.nick <> s.nick) and not s.allowed(11):
    #deny: делать админом кого-то кроме себя может только овнер
    s.lmsg(t, 'not_allowed')
    return
  else:
   if not s.allowed(11):
    #добавлять jid в список админов может только овнер
    s.lmsg(t, 'not_allowed')
    return
   j = jid_regexp.match(p)
   if j:
    nj = 'jid'
    p = j.groups()[0]
   else:
    s.lmsg(t, 'invalid_nick_or_jid')
    return
  moderate(t, s, p, nj, p, 'affiliation', 'admin', reason)
 else: s.syntax(t, 'admin')

bot.register_cmd_handler(admin_handler, '.admin', 9, 1)


def owner_handler(t, s, p):
 if p:
  #print m_parse(p)
  p, reason = m_parse(p)
  item = s.room.get(p)
  if item: nj = 'nick'
  else:
   j = jid_regexp.match(p)
   if j:
    nj = 'jid'
    p = j.groups()[0]
   else:
    s.lmsg(t, 'invalid_nick_or_jid')
    return
  moderate(t, s, p, nj, p, 'affiliation', 'owner', reason)
 else: s.syntax(t, 'owner')

bot.register_cmd_handler(owner_handler, '.owner', 11, 1)


def ban_handler(t, s, p):
 if check_if_bot_is_owner(t, s): return
 if p:
  #print m_parse(p)
  p, reason = m_parse(p)
  item = s.room.get(p)
  if item: nj = 'nick'
  else:
   j = jid_regexp.match(p)
   if j:
    nj = 'jid'
    p = j.groups()[0]
   else:
    s.lmsg(t, 'invalid_nick_or_jid')
    return
  moderate(t, s, p, nj, p, 'affiliation', 'outcast', reason)
 else: s.syntax(t, 'ban')

bot.register_cmd_handler(ban_handler, '.ban', 9, 1)


def none_handler(t, s, p):
 if check_if_bot_is_owner(t, s): return
 if p:
  #print m_parse(p)
  p, reason = m_parse(p)
  item = s.room.get(p)
  if item: nj = 'nick'
  else:
   j = jid_regexp.match(p)
   if j:
    nj = 'jid'
    p = j.groups()[0]
   else:
    s.lmsg(t, 'invalid_nick_or_jid')
    return
  moderate(t, s, p, nj, p, 'affiliation', 'none', reason)
 else: s.syntax(t, 'none')

bot.register_cmd_handler(none_handler, '.none', 9, 1)


def member_handler(t, s, p):
 if check_if_bot_is_owner(t, s): return
 if p:
  #print m_parse(p)
  p, reason = m_parse(p)
  item = s.room.get(p)
  if item: nj = 'nick'
  else:
   j = jid_regexp.match(p)
   if j:
    nj = 'jid'
    p = j.groups()[0]
   else:
    s.lmsg(t, 'invalid_nick_or_jid')
    return
  moderate(t, s, p, nj, p, 'affiliation', 'member', reason)
 else: s.syntax(t, 'member')

def check_if_bot_is_owner(t, s):
 if s.room.bot.affiliation.lower() == 'owner':
  s.lmsg(t, 'affiliation_editor_disabled')
  return True
 else: return False

bot.register_cmd_handler(member_handler, '.member', 9, 1)
