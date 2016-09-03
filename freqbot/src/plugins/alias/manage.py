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
def parse_alias(text):
 if text == u'&': return (2, None, None, text, False)
 if text == '': return (1, None, None, None, None)
 if text.startswith(u'access:'):
  q = re.match(u'^access:(\d{1,3}):(\d{1,3})@(.*[^&])(&?)$', text)
  if q:
   groups = q.groups()
   glue = groups[3]==u'&'
   return (0, int(groups[0]), int(groups[1]), groups[2], glue)
  else: return (1, None, None, None, None)
 else:
  if text.endswith('&'): return (2, None, None, text[:-1], True)
  else: return (2, None, None, text, False)

class alias:
 def __init__(self, text, command):
  q = parse_alias(text)
  self.glue = q[4]
  self.with_access = q[0]==0
  self.invalid = q[0]==1
  self.security = u'access_' in command
  self.alias = q[3]
  self.a1 = q[1]
  self.a2 = q[2]
  self.command = command
 def check(self, text):
  text = text.lower()
  if self.glue: return text.startswith(self.alias)
  else: return (text==self.alias) or text.startswith(self.alias + u' ')
 def string(self):
  if self.with_access: s = u'access:%s:%s@%s' % (self.a1, self.a2, self.alias)
  else: s = self.alias
  if self.glue: return u'%s&=%s' % (s, self.command)
  else: return u'%s=%s' % (s, self.command)
 def parse(self, text):
  text = text[len(self.alias):]
  if text and not self.glue: text = text[1:]
  return text

def alias_check(groupchat):
 if not ALIASES.has_key(groupchat):
  alias_load(groupchat)

def alias_load(groupchat):
 try:
  w = options.list2dict(options.optstringlist('aliases')[groupchat])
  ALIASES[groupchat] = {}
  for t in w.keys():
   s = alias(t, w[t])
   ALIASES[groupchat][s.alias] = s
 except: ALIASES[groupchat] = {}

def alias_dump(groupchat):
 options.optstringlist('aliases')[groupchat] = [alias[1].string() for alias in ALIASES[groupchat].items()]
 #print 'alias_dump'

def alias_get(groupchat, text):
 alias_check(groupchat)
 w = [i[1] for i in ALIASES[groupchat].items()]
 return [a for a in w if a.check(text)]

def alias_set(groupchat, alias):
 alias_check(groupchat)
 ALIASES[groupchat][alias.alias] = alias
 alias_dump(groupchat)

def alias_del(groupchat, salias):
 alias_check(groupchat)
 ALIASES[groupchat].pop(salias)
 alias_dump(groupchat)

def alias_clear(groupchat):
 alias_check(groupchat)
 ALIASES[groupchat].clear()
 alias_dump(groupchat)
