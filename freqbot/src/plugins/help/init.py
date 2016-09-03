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
def initialize_help():
 global HELP_LANGS
 global HELP_CATEGORIES
 HELP_LANGS = {}
 HELP_CATEGORIES = {}
 q = os.listdir('doc/help')
 for i in q:
  p = re.search(u'^\.*(.+)\-(..)\.txt$', i.decode('utf8'))
  if p:
   p = p.groups()
   language = p[1]
   p = p[0]
   HELP_LANGS.setdefault(p, [])
   HELP_LANGS[p].append(language)
   fn = 'doc/help/%s' % (i, )
   fp = file(fn, 'r')
   c = fp.readline().decode('utf8')
   fp.close()
   for j in c.split():
    HELP_CATEGORIES.setdefault(j, [])
    if not p in HELP_CATEGORIES[j]: HELP_CATEGORIES[j].append(p)

initialize_help()

