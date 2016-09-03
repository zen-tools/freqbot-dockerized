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

def my_quote(text, EscapeOnly=False):
 s = text.replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`')
 if not EscapeOnly: s = '"' + s + '"'
 return s

def my_replace(text, s1, s2):
 if text.count(s1):
  n = text.index(s1)
  return text[:n] + s2 + my_replace(text[n+len(s1):], s1, s2)
 else: return text

def get_end_count(text, d, n):
 if text.endswith(d): return get_end_count(text[:len(text)-1], d, n+1)
 else: return n

def get_param(text):
 text = text.strip()
 if not text: return ('', '')
 if text[0] in ["'", '"']:
  d = text[0]
  text = text[1:]
  if text.count(d):
   n = text.find(d)
   if (n > 0) and (text[n-1] == '\\'):
    p = text[:n-1]
    text = text[n:].strip()
    q = get_end_count(p, '\\', 0)
    print (p, text, q)
    if q % 2 == 1:
     p = my_replace(p, '\\\\', '\\')
     text = text[1:].strip()
    else:
     p = my_replace(p, '\\\\', '\\')
     a, b = get_param(text)
     p, text = p + d + a, b
   else:
    p, text = my_replace(text[:n], '\\\\', '\\'), text[n+1:].strip()
  else: raise ValueError('unbalanced quotes')
 else:
  if text.count(' '):
   n = text.find(' ')
   p = text[:n]
   text = text[n:].strip()
  else: p, text = text, ''
 return (p, text)

bigtime = 2000000000

def parse_time(s):
 l = s[len(s)-1].lower()
 c = int(s[:len(s)-1])
 if l == 'd': return 86400 * c
 elif l == 'h': return 3600 * c
 elif l == 'm': return 60 * c
 elif l == 's': return c
 else: raise ValueError

def fetch_time(s):
 s = s.strip()
 if s.startswith('/'):
  n = s.find(' ')
  end_time = int(parse_time(s[1:n]) + time.time())
  s = s[n+1:]
 elif s.startswith('@#/'):
  n = s.find(' ')
  end_time = int(s[3:n])
  s = s[n+1:]
 else: end_time = bigtime
 return (end_time, s)

def dump_time(tm, text, human=False, s=None):
 if tm == bigtime: return text
 else:
  if human: return u'%s (%s %s)' % (text, s.get_msg('left'), time2str(tm - time.time(), True, s.get_lang()))
  else: return u'@#/%d %s' % (tm, text)

# http://www.w3.org/TR/xml11/
#[2]   	Char	   ::=   	[#x1-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]	/* any Unicode character, excluding the surrogate blocks, FFFE, and FFFF. */
#[2a]   	RestrictedChar	   ::=   	[#x1-#x8] | [#xB-#xC] | [#xE-#x1F] | [#x7F-#x84] | [#x86-#x9F]

#Document authors are encouraged to avoid "compatibility characters", as defined in Unicode [Unicode]. The characters defined in the following ranges are also discouraged. They are either control characters or permanently undefined Unicode characters:

#[#x1-#x8], [#xB-#xC], [#xE-#x1F], [#x7F-#x84], [#x86-#x9F], [#xFDD0-#xFDDF],
#[#x1FFFE-#x1FFFF], [#x2FFFE-#x2FFFF], [#x3FFFE-#x3FFFF],
#[#x4FFFE-#x4FFFF], [#x5FFFE-#x5FFFF], [#x6FFFE-#x6FFFF],
#[#x7FFFE-#x7FFFF], [#x8FFFE-#x8FFFF], [#x9FFFE-#x9FFFF],
#[#xAFFFE-#xAFFFF], [#xBFFFE-#xBFFFF], [#xCFFFE-#xCFFFF],
#[#xDFFFE-#xDFFFF], [#xEFFFE-#xEFFFF], [#xFFFFE-#xFFFFF],
#[#x10FFFE-#x10FFFF].

accepted_ranges = [
(u'\u0009', u'\u000A'),
(u'\u000D', u'\u000D'),
(u'\u0020', u'\u007E'),
(u'\u0085', u'\u0085'),
(u'\u00A0', u'\u05FF'),
(u'\u0800', u'\uD7FF'),
(u'\uE000', u'\uFD49'),
(u'\uFE00', u'\uFE69'),
(u'\uFF00', u'\uFFFD'),
(u'\u10000', u'\u10A69'),
(u'\u10A80', u'\u1FFFD'),
(u'\u20000', u'\u2FFFD'),
(u'\u30000', u'\u3FFFD'),
(u'\u40000', u'\u4FFFD'),
(u'\u50000', u'\u5FFFD'),
(u'\u60000', u'\u6FFFD'),
(u'\u70000', u'\u7FFFD'),
(u'\u80000', u'\u8FFFD'),
(u'\u90000', u'\u9FFFD'),
(u'\uA0000', u'\uAFFFD'),
(u'\uB0000', u'\uBFFFD'),
(u'\uC0000', u'\uCFFFD'),
(u'\uD0000', u'\uDFFFD'),
(u'\uE0000', u'\uEFFFD'),
(u'\uF0000', u'\uFFFFD'),
(u'\u100000', u'\u10FFFD')
]

def clear_char(c):
 for rg in accepted_ranges:
  if (c >= rg[0]) and (c <= rg[1]): return c
 return u'\uFFFD'

def clear_text(s):
 res = map(clear_char, s)
 return u''.join(res)

bot.clear_text = clear_text

strip_tags = re.compile(u'<[^<>]+>')

def html_decode(text):
 text = text.replace(u'\n', u'')
 text = text.replace('<p>', '\n').replace('<li>', '\n')
 return strip_tags.sub(u'', text.replace(u'<br>',u'\n')).replace(u'&nbsp;', u' ').replace(u'&lt;',\
 u'<').replace(u'&gt;', u'>').replace(u'&quot;', u'"').replace(u'\t', u'')
