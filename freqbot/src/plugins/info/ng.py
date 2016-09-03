#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Calendar plugin for FreQ bot
#    Copyright (C) 2011 Timur Timirkhanov <timur@timirkhanov.kz>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from datetime import datetime

def ng_handler(t, s, p):
 present = datetime.now()
 newyear = datetime(present.year+1, 1, 1,0,0,0)
 diff = newyear - present
 stime = u'Скоро новый год! До него осталось %d секунд...' % (diff.days*86400+diff.seconds,)
 s.msg(t, stime)

bot.register_cmd_handler(ng_handler, u'.ng')