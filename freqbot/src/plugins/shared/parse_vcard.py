#!/usr/bin/env python
# -*- coding: utf8 -*-
#~#######################################################################
#~ Copyright (c) 2008 Burdakov Daniel <kreved@kreved.org>               #
#~ Copyright (c) 2011 Timur "TLemur" Timirkhanov                        #
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
'ru::vCard/N/SUFFIX'    : u'Суффикс',
'ru::vCard/N/GIVEN'     : u'Имя',
'ru::vCard/N/PREFIX'    : u'Префикс',
'ru::vCard/N/MIDDLE'    : u'Отчество',
'ru::vCard/N/FAMILY'    : u'Фамилия',
'ru::vCard/URL'         : u'Сайт',
'ru::vCard/BDAY'        : u'День рождения',
'ru::vCard/DESC'        : u'О себе',
'ru::vCard/PHOTO/TYPE'  : u'Фото',
'ru::vCard/ORG/ORGNAME' : u'Организация',
'ru::vCard/ORG/ORGUNIT' : u'Подразделение',
'ru::vCard/TITLE'       : u'Должность',
'ru::vCard/ADR/CTRY'    : u'Государство',
'ru::vCard/EMAIL'       : u'Мыло',
'ru::vCard/EMAIL/USERID': u'Мыло',
'ru::vCard/UID'         : u'UID',
'ru::vCard/JABBERID'    : u'JID',
'ru::vCard/ROLE'        : u'Роль',
'ru::vCard/NICKNAME'    : u'Ник',
'ru::vCard/TEL/NUMBER'  : u'Телефон',
'ru::vCard/ADR/REGION'  : u'Регион',
'ru::vCard/ADR/LOCALITY': u'Город',
'ru::vCard/ADR/STREET'  : u'Улица',
'ru::vCard/ADR/EXTADD'  : u'Адрес 2',
'ru::vCard/ADR/PCODE'   : u'Индекс',
'ru::vCard/GEO/LON'     : u'Долгота',
'ru::vCard/GEO/LAT'     : u'Широта',
'ru::vCard/GENDER'      : u'Пол',

'en::vCard/FN'          : u'Full Name',
'en::vCard/N/SUFFIX'    : u'Suffix',
'en::vCard/N/GIVEN'     : u'Given name',
'en::vCard/N/PREFIX'    : u'Prefix',
'en::vCard/N/MIDDLE'    : u'Middle name',
'en::vCard/N/FAMILY'    : u'Family name',
'en::vCard/URL'         : u'Homepage',
'en::vCard/BDAY'        : u'Birthday',
'en::vCard/DESC'        : u'About',
'en::vCard/PHOTO/TYPE'  : u'Photo',
'en::vCard/ORG/ORGNAME' : u'Organization',
'en::vCard/ORG/ORGUNIT' : u'Organization unit',
'en::vCard/TITLE'       : u'Title',
'en::vCard/ROLE'        : u'Role',
'en::vCard/ADR/CTRY'    : u'Country',
'en::vCard/EMAIL'       : u'Email',
'en::vCard/EMAIL/USERID': u'Email',
'en::vCard/UID'         : u'UID',
'en::vCard/JABBERID'    : u'JID',
'en::vCard/NICKNAME'    : u'Nick',
'en::vCard/ADR/LOCALITY': u'Locality',
'en::vCard/ADR/STREET'  : u'Street',
'en::vCard/ADR/EXTADD'  : u'Address 2',
'en::vCard/ADR/PCODE'   : u'Post code',
'en::vCard/GEO/LON'     : u'Longitude',
'en::vCard/GEO/LAT'     : u'Latitude',
'en::vCard/GENDER'      : u'Gender'
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
