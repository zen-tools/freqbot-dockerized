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

def htmldecode(text):
 text = u' '.join(text.split())
 text = re.sub(u'<(br|p|BR|P)\/?>', u'\n', text)
 r = u'nbsp: ;lt:<;gt:>;amp:&;quot:";copy:©;#39:\''
 for  i in r.split(';'):
  x = i.split(':')
  text = text.replace(u'&%s;' % (x[0], ), x[1])
 text = re.sub(u'<[^<>]*>', u' ', text)
 text = re.sub(u'\ +', u' ', text)
 return text
