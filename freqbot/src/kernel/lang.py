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
import options
import os
import config

lang_ext = '.msg'
LANG = {}

ll = [i for i in os.listdir('lang') if i.endswith(lang_ext)]
for i in ll:
 fp = file('lang/'+i, 'r')
 p = fp.read().decode('utf8').split('\n')
 p = [j.strip() for j in p if j.count(' ')]
 fp.close()
 for j in p:
  k = j[:j.find(' ')]
  v = j[j.find(' ')+1:]
  if not LANG.has_key(i): LANG[i] = {}
  LANG[i][k] = v.replace('\\n', '\n')

def get(m, l = config.LANG):
 try: return LANG[l+lang_ext][m]
 except:
  try: return LANG['en'+lang_ext][m]
  except: return 'Lang.NotFound:%s:%s' % (l, m)

def msg(tpl, params = (), l = config.LANG):
 p = []
 for i in params:
  if i.__class__ == u''.__class__:
   p.append(i)
  else: p.append(unicode(i))
 try: return get(tpl, l) % tuple(p)
 except: return 'lang.error:%s:%s' % (l, tpl)

def getLang(jid):
 jid = jid.split('/')[0]
 return options.get_option(jid, 'lang', config.LANG)

def setLang(jid, lang):
 jid = jid.split('/')[0]
 return options.set_option(jid, 'lang', lang)

def languages():
 return [i[:2] for i in LANG.keys()]

def dump(l, f):
 q = LANG[l+lang_ext]
 s = u''
 x = q.keys()
 x.sort()
 for i in x:
  s += u'%s %s\n' % (i, q[i].replace('\n', '\\n'))
 fp = file(f, 'w')
 fp.write(s.encode('utf8'))
 fp.close()

def set(m, l, value):
 f = 'lang/%s%s' % (l, lang_ext)
 q = '%s%s' % (l, lang_ext)
 LANG[q][m] = value
 dump(l, f)
