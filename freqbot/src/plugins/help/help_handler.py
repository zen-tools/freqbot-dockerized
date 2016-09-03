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

def help_handler(t, s, p):
 p = p.strip()
 q = re.search('^(\-..\ )?\.?(.+)$', p)
 if q:
  rlang = q.groups()[0]
  if rlang: rlang = rlang[1:3]
  else: rlang = lang.getLang(s.jid)
  p = q.groups()[1]
  if p.startswith('.'): p = p[1:]
 else:
  rlang = lang.getLang(s.jid)
  p = ''
 if p:
  if p.startswith('.'): p = p[1:]
  if p in HELP_CATEGORIES:
   answer = HELP_CATEGORIES[p]
   answer.sort()
   answer = ', '.join(answer)
   s.lmsg(t, 'help_category', answer)
  else:
   if p in HELP_LANGS:
    q = HELP_LANGS[p]
    if rlang in q:
     content = load_help_content(p, rlang)
     categories = ', '.join([w for w in HELP_CATEGORIES.keys() if p in HELP_CATEGORIES[w]])
     s.lmsg(t, 'help_show', categories, content)
    else:
     languages = HELP_LANGS[p]
     languages = ["'.help -%s %s'" % (w, p) for w in languages]
     s.lmsg(t, 'help_other_languages', p, rlang, ', '.join(languages))
   else: s.lmsg(t, 'help_not_found', p)
 else:
  ans = ['%s(%s)' % (w, len(HELP_CATEGORIES[w])) for w in HELP_CATEGORIES.keys()]
  ans.sort()
  categories = ', '.join(ans)
  s.lmsg(t, 'help_categories', categories)

bot.register_cmd_handler(help_handler, '.help')
bot.register_cmd_handler(help_handler, 'help')

