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

from twisted.web.client import getPage
from twisted.internet.error import DNSLookupError, TimeoutError
from twisted.internet.defer import TimeoutError as DeferTimeout
from twisted.web.error import Error as WebError
from html2text import html2text

www_regexp = re.compile(u'^(https?\:\/\/)?(((\w|\-)+\.)*\w+)(:\d+)?(\/(\w|[\-\._])+)*\/?$')

def www_handler(typ, source, params):
 params = params.strip()
 if params.count(' '): url, enc = params.split()[:2]
 else: url, enc = params, 'utf8'
 if not enc in ['utf8', 'cp1251', 'koi8-r', 'utf-8']: # to be continued
  source.lmsg(typ, 'invalid_encoding')
  return
 url = url.strip().encode(enc)
 if not url.startswith('http'): url = 'http://' + url
 if not url or not www_regexp.match(url): source.syntax(typ, 'www')
 else:
  d = getPage(url, timeout=20)
  d.addCallback(www_result, typ, source, enc)
  d.addErrback(www_error, typ, source)

def www_result(page, typ, source, enc):
 page = page.decode(enc, 'replace')
 try: page = html2text(page)
 except: pass
 if len(page) > 100000: page = page[:100000]
 source.msg(typ, page)

def www_error(reason, typ, source):
 if reason.check(DNSLookupError): source.lmsg(typ, 'www_dns_error')
 elif reason.check(TimeoutError, DeferTimeout): source.lmsg(typ, 'www_timeout_error')
 elif reason.check(WebError): source.lmsg(typ, 'www_error')
 else: source.lmsg(typ, 'www_error_reason', repr(reason))

bot.register_cmd_handler(www_handler, '.www')
