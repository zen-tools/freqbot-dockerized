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

import regex

class NickNotFound(Exception):
 def __init__(self, value):
  self.value = value
 def __str__(self):
  return repr(self.value)

class NoJID(Exception):
 def __init__(self, value):
  self.value = value
 def __str__(self):
  return repr(self.value)

class MyRegexpError(Exception):
 def __init__(self, value):
  self.value = value
 def __str__(self):
  return repr(self.value)

class aitem:
 def __init__(self, room, s, negative=True):
  """
  парсит выражения типа '/5m jid blabla@server', 'nick exp regexp', etc.
  короче в стиле глюкса
  """
  self.room = room
  self.negative = negative
  self.end_time, s = fetch_time(s)
  if s.count('||'): s, self.reason = s[:s.find('||')].strip(), s[s.find('||')+2:].strip()
  else: s, self.reason = s.strip(), ''
  if s.lower().startswith('jid '):
   self.by_jid = True
   s = s[4:].lower()
   if not s: raise ValueError
  elif s.lower().startswith('nick '):
   self.by_jid = False
   s = s[5:]
   if not s: raise ValueError
  else:
   self.by_jid = True
   self.regexp = False
   item = room.get(s, None)
   if item:
    if item.jid == item.realjid: raise NoJID(item.jid)
    else: self.value = item.realjid.lower()
   else: raise NickNotFound(s)
   return
  if s.lower().startswith('exp '):
   self.regexp = True
   s = s[4:]
   try: regex.match(s, 'test@jabber.org')
   except: raise MyRegexpError(s)
  else: self.regexp = False
  self.value = s
 def text(self, human = False, with_time = True):
  if self.by_jid: text = 'jid '
  else: text = 'nick '
  if self.regexp: text = text + u'exp '
  text = text + self.value
  if with_time: text = dump_time(self.end_time, text, human, self.room)
  if self.reason: return text + '||' + self.reason
  else: return text
 def __str__(self):
  return u'aitem: "%s", regexp: %s, by_jid: %s, value="%s", reason="%s"' % \
  (self.text(True), self.regexp, self.by_jid, self.value, self.reason)
 def check(self, item):
  if self.by_jid: s = item.realjid.lower()
  else: s = item.nick
  if self.regexp:
   return not(self.negative and (item.affiliation <> 'none')) and regex.match(self.value, s)
  else: return (self.value == s)
 def get_reason(self):
  if self.reason: return self.reason
  else: return 'You are not welcomed here'

def del_from_alists(room, s):
 for alist in ALISTS: alist.safe_remove(room, s)

class alist:
 def __init__(self, bot, typ, action, negative=True):
  self.negative = negative
  self.action = action
  self.lists = optstringlist(typ)
  bot.register_join_handler(self.join_handler)
  bot.register_leave_handler(self.leave_handler)
 def append(self, room, s):
  q = aitem(room, s)
  s = q.text(False, False)
  del_from_alists(room, s)
  p = self.lists[room.jid]
  p.append(q.text())
  p.sort()
  self.lists[room.jid] = p
  self.apply_to_room(room)
 def delete(self, room, n):
  p = self.lists[room.jid]
  p.pop(n-1)
  self.lists[room.jid] = p
 def safe_remove(self, room, s):
  tm, s = fetch_time(s)
  items = self.items(room)
  new_items = [i for i in items if i.text(False, False) <> s]
  if len(new_items) < len(items):
   self.lists[room.jid] = [i.text() for i in new_items]
 def items(self, room):
  q = [aitem(room, i, self.negative) for i in self.lists[room.jid]]
  t = time.time()
  if [True for i in q if i.end_time<t]:
   q = [i for i in q if i.end_time>t]
   self.lists[room.jid] = [i.text() for i in q]
  return q
 def clear(self, room):
  self.lists[room.jid] = []
 def check(self, room, item):
  q = [i.get_reason() for i in self.items(room) if i.check(item)]
  if len(q) > 0: return q[0]
  else: return False
 def cmd(self, typ, source, cmd):
  room = source.room
  if cmd.count(' '):
   n = cmd.find(' ')
   c, p = cmd[:n].lower(), cmd[n+1:]
  else: c, p = cmd.lower(), ''
  if c == 'del':
   try: n = int(p)
   except:
    source.lmsg(typ, 'invalid_syntax_default')
    return
   if len(self.items(room)) < n: source.lmsg(typ, 'number_not_found')
   else:
    self.delete(room, n)
    source.lmsg(typ, 'deleted')
  elif c in ['list', 'show']:
   q = [i.text(True) for i in self.items(room)]
   if q: source.msg(typ, show_list(q, p, source.get_msg('not_found')))
   else: source.lmsg(typ, 'list_empty')
  elif c == 'clear':
   self.clear(room)
   source.lmsg(typ, 'cleared')
  else:
   try:
    self.append(room, cmd[:80])
    source.lmsg(typ, 'added')
   except NickNotFound: source.lmsg(typ, 'nick_not_found')
   except NoJID: source.lmsg(typ, 'alist_add_nojid')
   except MyRegexpError: source.lmsg(typ, 'invalid_regexp')
   except ValueError: source.lmsg(typ, 'invalid_syntax_default')
 def apply_to_item(self, item):
  reason = self.check(item.room, item)
  if (reason <> False): self.action(item, reason)
 def apply_to_room(self, room):
  for nick in room.keys(): self.apply_to_item(room[nick])
 def join_handler(self, item):
  self.apply_to_item(item)
 def leave_handler(self, item, typ, reason):
  if typ == 3: #changed nick
   self.apply_to_item(item)

def a_kick(item, reason):
 item.room.moderate('nick', item.nick, 'role', 'none', reason)

def a_visitor(item, reason):
 item.room.moderate('nick', item.nick, 'role', 'visitor', '')

def a_moderator(item, reason):
 item.room.moderate('nick', item.nick, 'role', 'moderator', '')
 
def a_ban(item, reason):
 item.room.moderate('nick', item.nick, 'affiliation', 'outcast', reason)
 
def a_participant(item, reason):
 item.room.moderate('nick', item.nick, 'role', 'participant', '')


AKICK = alist(bot, 'akick', a_kick, False)
AVISITOR = alist(bot, 'avisitor', a_visitor, False)
AMODERATOR = alist(bot, 'amoderator', a_moderator, False)
ABAN = alist(bot, 'aban',  a_ban, True)
APARTICIPANT = alist(bot, 'aparticipant', a_participant, False)
ALISTS = [AKICK, AVISITOR, AMODERATOR, ABAN, APARTICIPANT]

def akick_handler(t, s, p):
 p = p.strip()
 if not p: s.syntax(t, 'akick')
 else: AKICK.cmd(t, s, p)

def avisitor_handler(t, s, p):
 p = p.strip()
 if not p: s.syntax(t, 'avisitor')
 else: AVISITOR.cmd(t, s, p)

def amoderator_handler(t, s, p):
 p = p.strip()
 if not p: s.syntax(t, 'amoderator')
 else: AMODERATOR.cmd(t, s, p)
 
def aban_handler(t, s, p):
 p = p.strip()
 if not p: s.syntax(t, 'aban')
 else: ABAN.cmd(t, s, p)
 
def aparticipant_handler(t, s, p):
 p = p.strip()
 if not p: s.syntax(t, 'aparticipant')
 else: APARTICIPANT.cmd(t, s, p)

bot.register_cmd_handler(akick_handler, '.akick', 9, True)
bot.register_cmd_handler(avisitor_handler, '.avisitor', 9, True)
bot.register_cmd_handler(amoderator_handler, '.amoderator', 9, True)
bot.register_cmd_handler(aban_handler, '.aban', 9, True)
bot.register_cmd_handler(aparticipant_handler, '.aparticipant', 9, True)
