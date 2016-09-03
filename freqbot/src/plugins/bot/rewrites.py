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
def commands_handler(q):
 typ, source, text, stanza = q
 cm = '.commands '
 if text.startswith(cm):
  text = text[len(cm):]
  cmds = text.split(u';')
  return [(typ, source, cmd, stanza) for cmd in cmds if cmd]

#class my_wrapper:
 #def __init__(self, item, typ):
  #self.item = item
  #self.typ = typ
 #def __getattribute__(self, name):
  #if name == 'lmsg': return self.lmsg
  #elif name == 'msg': return self.msg
  #else: return self.item.__getattribute__(name)
 #def msg(self, typ, body):
  #if self.typ == 'private': self.item.msg('chat', body)
  #elif self.typ == 'null': pass
 #def lmsg(self, typ, body):
  #if self.typ == 'private': self.item.lmsg('chat', body)
  #elif self.typ == 'null': pass

def null_handler(q):
 typ, source, text, stanza = q
 cm = '.null '
 if text.startswith(cm):
  text = text[len(cm):]
  #item = my_wrapper(source, 'null')
  return [('null', source, text, stanza)]

def private_handler(q):
 typ, source, text, stanza = q
 cm = '.private '
 if text.startswith(cm):
  text = text[len(cm):]
  return [('chat', source, text, stanza)]

def redirect_handler(q):
 typ, source, text, stanza = q
 text = context_replace(text, typ, source)
 cm = '.redirect '
 if text.startswith(cm):
  if source.access() < 9:
   # if not source is room admin...
   return [(typ, source, '.echo ' + source.get_msg('not_allowed'), stanza)]
  if re.search('.*www.*|.*echo.*|.*status.*',text): return [(typ, source, '.echo ' + source.get_msg('not_allowed'), stanza)]
  try: nick, text = get_param(text[len(cm):])
  except:
   return [(typ, source, '.echo ' + source.get_msg('invalid_syntax_default'), stanza)]
  if source.room and (nick in source.room.keys()):
   return [('redirect:' + nick, source,text, stanza)]
  else:
   print (nick, source.room.keys())
   return [(typ, source, '.echo ' + source.get_msg('redirect_nowhere'), stanza)]

def mynick_handler(q):
 typ, source, text, stanza = q
 if not source.room or not source.room.bot: return False
 cm = u'%s: ' % (source.room.bot.nick, )
 if text.startswith(cm):
  text = text[len(cm):]
  return [(typ, source, text, stanza)]

bot.register_rewrite_engine(commands_handler)
bot.register_rewrite_engine(null_handler)
bot.register_rewrite_engine(private_handler)
bot.register_rewrite_engine(mynick_handler)
bot.register_rewrite_engine(redirect_handler)
