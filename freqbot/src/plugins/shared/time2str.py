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

def time2str(diff, rnd=False, lng=config.LANG):
 """This function is not very exact, it doesn't take care
 of leap years, and of month with different number of days."""
 seconds = diff % 60
 years, months, days, hours, minutes, _, _, _, _ = map(lambda x,y: x-y, time.gmtime(diff), time.gmtime(0))
 if rnd: r = u'%d %s' % (round(seconds), get_seconds(round(seconds), lng))
 else: r = u'%0.2f %s' % (seconds, get_seconds(2, lng))
 if minutes: r = u'%d %s %s' % (minutes, get_minutes(minutes, lng), r)
 if hours: r = u'%d %s %s' % (hours, get_hours(hours, lng), r)
 if days: r = u'%d %s %s' % (days, get_days(days, lng), r)
 if months: r = u'%d %s %s' % (months, get_months(months, lng), r)
 if years: r = u'%d %s %s' % (years, get_years(years, lng), r)
 return r

def get_seconds(c, l):
 if l == u'ru':
  if c % 100 in xrange(10,20): return u'секунд'
  elif c % 10 == 1: return u'секунду'
  elif c % 10 in [2, 3, 4]: return u'секунды'
  else: return u'секунд'
 else:
  if c == 1: return u'second'
  else: return u'seconds'

def get_minutes(c, l):
 if l == u'ru':
  if c % 100 in xrange(10,20): return u'минут'
  elif c % 10 == 1: return u'минуту'
  elif c % 10 in [2, 3, 4]: return u'минуты'
  else: return u'минут'
 else:
  if c == 1: return u'minute'
  else: return u'minutes'

def get_hours(c, l):
 if l == u'ru':
  if c % 100 in xrange(10,20): return u'часов'
  elif c % 10 == 1: return u'час'
  elif c % 10 in [2, 3, 4]: return u'часа'
  else: return u'часов'
 else:
  if c == 1: return u'hour'
  else: return u'hours'

def get_days(c, l):
 if l == u'ru':
  if c % 100 in xrange(10,20): return u'дней'
  elif c % 10 == 1: return u'день'
  elif c % 10 in [2, 3, 4]: return u'дня'
  else: return u'дней'
 else:
  if c == 1: return u'day'
  else: return u'days'

def get_months(c, l):
 if l == u'ru':
  if c % 100 in xrange(10,20): return u'месяцев'
  elif c % 10 == 1: return u'месяц'
  elif c % 10 in [2, 3, 4]: return u'месяца'
  else: return u'месяцев'
 else:
  if c == 1: return u'month'
  else: return u'months'

def get_years(c, l):
 if l == u'ru':
  if c % 100 in xrange(10,20): return u'лет'
  elif c % 10 == 1: return u'год'
  elif c % 10 in [2, 3, 4]: return u'года'
  else: return u'лет'
 else:
  if c == 1: return u'year'
  else: return u'years'
