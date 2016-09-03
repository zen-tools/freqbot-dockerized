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

VCARD_FIELDS = {
'ru::vCard/FN'          : u'Полное имя', 
'ru::vCard/URL'         : u'Сайт',
'ru::vCard/BDAY'        : u'День рождения',
'ru::vCard/DESC'        : u'О себе',
'ru::vCard/PHOTO/TYPE'  : u'Фото',
'ru::vCard/ORG/ORGNAME' : u'Организация',
'ru::vCard/TITLE'       : u'Роль',
'ru::vCard/ADR/CTRY'    : u'Государство',
'ru::vCard/EMAIL/USERID': u'Мыло',
'ru::vCard/NICKNAME'    : u'Ник',
'ru::vCard/TEL/NUMBER'  : u'Телефон',
'ru::vCard/ADR/REGION'  : u'Регион',
'ru::vCard/ADR/LOCALITY': u'Город',
'ua::vCard/FN'          : u'Им\'я', 
'ua::vCard/URL'         : u'Сайт',
'ua::vCard/BDAY'        : u'День народження',
'ua::vCard/DESC'        : u'О себе',
'ua::vCard/PHOTO/TYPE'  : u'Фото',
'ua::vCard/ORG/ORGNAME' : u'Органiзацiя',
'ua::vCard/TITLE'       : u'Роль',
'ua::vCard/ADR/CTRY'    : u'Краiна',
'ua::vCard/EMAIL/USERID': u'Мило',
'ua::vCard/NICKNAME'    : u'Ник',
'ua::vCard/ADR/LOCALITY': u'Мiсто',
'en::vCard/FN'          : u'Full Name',
'en::vCard/URL'         : u'Homepage',
'en::vCard/BDAY'        : u'Birthday',
'en::vCard/DESC'        : u'About',
'en::vCard/PHOTO/TYPE'  : u'Photo',
'en::vCard/ORG/ORGNAME' : u'Organization',
'en::vCard/TITLE'       : u'Role',
'en::vCard/ADR/CTRY'    : u'Country',
'en::vCard/EMAIL/USERID': u'Email',
'en::vCard/NICKNAME'    : u'Nick',
'en::vCard/ADR/LOCALITY': u'Locality',
}

def vcard_describe(field, lang):
 field = field[:len(field)-1]
 m = lang + '::' + field
 if m in VCARD_FIELDS.keys(): return VCARD_FIELDS[m]
 else: return field

def parse_vcard(x):
 r = {}
 if type(x) == domish.Element:
  for i in x.children:
   q = parse_vcard(i)
   for j in q.keys():
    r['%s/%s' % (x.name, j)] = q[j]
 else: r[''] = x
 return r
