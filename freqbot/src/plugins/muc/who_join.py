#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

#by 40tman

from twisted.words.protocols.jabber import jid

USS=[]

def who_join(item):
    if item.room.jid+item.nick not in USS:
        USS.append(item.room.jid+item.nick)

def who_msg(t,s,p):
    f=''
    n=0
    for i in USS:
        if i.count(s.room.jid)>0:
            y = i.split(s.room.jid)
            n+=1
            f+=y[1]+'; '
    s.msg(t, u'Я здесь видел '+unicode(n)+u' юзеров:\n'+f)

bot.register_cmd_handler(who_msg, u'.who_join', 0, 0)
bot.register_join_handler(who_join)

