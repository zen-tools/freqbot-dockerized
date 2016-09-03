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

TLDS = file('static/tlds.txt').read().decode('utf8', 'replace').splitlines()
TLDS.sort()
TLDS = [line.strip().split(':') for line in TLDS if line.count(':')]
TLDS = [(tld[0].lower(), tld[1].lower()) for tld in TLDS]

def tld_handler(typ, source, param):
 param = param.strip()
 if not param: source.syntax(typ, '.tld')
 else:
  param = param.lower()
  res = [tld for tld in TLDS if param in tld]
  if not res: res = [tld for tld in TLDS if tld[0].count(param) or tld[1].count(param)]
  if len(res) == 0: source.lmsg(typ, 'not_found')
  elif len(res) == 1:
   if res[0][0].count(param): source.msg(typ, res[0][1])
   else: source.msg(typ, res[0][0])
  else:
   res = [u'%s: %s' % (i[0].upper(), i[1]) for i in res]
   source.msg(typ, show_list(res))

bot.register_cmd_handler(tld_handler, '.tld')


def parse_area(s):
 return re.match(r'^(..)\ (.+)$', s).groups()

AREAS = file('static/arearu.txt').read().decode('utf8', 'replace').splitlines()
AREAS.sort()
AREAS = [parse_area(line) for line in AREAS if line.count(' ')]

def regionru_handler(t, s, p):
 p = p.strip()
 if not p: s.syntax(t, 'region')
 else:
  if p.isdigit():
   #code
   if len(p) == 1: p = '0' + p
   res = [i for i in AREAS if i[0] == p]
   if res: s.msg(t, res[0][1])
   else: s.lmsg(t, 'not_found')
  else:
   #region name (or part)
   res = [i for i in AREAS if i[1].lower().count(p.lower())]
   res = ['%s: %s' % i for i in res]
   s.msg(t, show_list(res, empty=s.get_msg('not_found')))

bot.register_cmd_handler(regionru_handler, '.regionru')
