#!/usr/bin/env python
# -*- coding: utf8 -*-
#~#######################################################################
#~ Copyright (c) 2008 Burdakov Daniel <kreved@kreved.org>
#~ Copyright (c) 2010 Kazakov Alexandr <ferym@jabber.ru>
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

import urllib
import simplejson

def google_handler(typ, source, params):
 params = params.strip()
 if not params: source.lmsg(typ,'google?'); return
 query = urllib.urlencode({'q': params.encode('utf-8')})
 url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
 try: page = urllib.urlopen(url)
 except: source.lmsg(typ,'google_no_results'); return
 fp = simplejson.load(page)
 if fp['responseStatus']==200:
  if not fp['responseData']['results']: source.lmsg(typ,'google_no_results'); return
  source.msg(typ,'%s:\n%s\n%s' % (html_decode(fp['responseData']['results'][0]['title']),html_decode(fp['responseData']['results'][0]['content']),fp['responseData']['results'][0]['unescapedUrl']))
 else: source.lmsg(typ,'google_no_results')
 

bot.register_cmd_handler(google_handler, '.google')
