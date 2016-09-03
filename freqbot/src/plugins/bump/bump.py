#!/usr/bin/env python
# -*- coding: utf-8 -*-
#~#######################################################################
#~ Copyright (c) 2014 Dmitry Poltavchenko <zen@root.ua>                 #
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

#by zen

import random
from twisted.words.protocols.jabber import jid


PHRASES=[
 u'/me совершил "расправу" над %s путем инсталяции винды!',
 u'/me подбил глаз и отнял калвиатуру у %s',
 u'/me вырубил пользователя %s веслом по голове. %s очнется минут через 10...',
 u'/me узнал где живет %s и коварно улыбается...',
 u'/me вызвал гром и молнию на голову пользователя %s',
 u'/me обиделся на %s. Следующий вход в конфу через магарыч',
 u'/me сегодня раздражен. Горбатым сегодня будет %s',
 u'/me рекомендует книгу "Начинающий пользователь ПК" для %s',
 u'/me решил, что парад для %s на сегодня отменяется',
 u'/me вспоминает, что в здешнем лесу пропадают люди... %s, идем покажу?',
 u'/me вызвал 03. %s, за тобой пришли',
 u'/me , как истинный джентельмен, предлагает %s уйти красиво',
 u'/me подозревает, что %s молодец',
 u'/me отправил %s читать гугл',
 u'/me считает, что %s обязан сходить в кино',
 u'/me многозначительно помахал ружьём: - %s, извини, но у меня нет другого выхода',
 u'/me полагает, что %s пишет из горящего танка и ему пора отдохнуть',
 u'/me побледнел глядя на историю посещенных страниц пользователя %s',
 u'/me возмущен! %s, я конфеты и шоколад не пью!',
 u'/me требует, что бы %s спел и станцевал!',
 u'/me настоятельно просит %s не заходить конфу с микроволновки!',
 u'/me взялся за терминал: sudo su %s -c "Сделай мне сэндвич!"',
]

LAST=''
STRING=''

def get_jid(source, p):
 if p:
  if source.room:
   if p in source.room.items.keys():
    return source.room[p].jid
   else: return p
  else: return p
 else: return source.jid

def bump_msg(t,s,p):
 global LAST
 global STRING
 while ( STRING==LAST or LAST=='' ):
  STRING=random.choice(PHRASES)
  if len(PHRASES) < 2:
   break
  elif STRING!=LAST:
   LAST=STRING
   break
 nick = p.strip('\r\n ')
 jid = get_jid(s, nick)
 if s.room:
  if nick == jid: s.room.msg(u'Здесь таких нет!') 
  elif s.room.bot and (s.room.bot.jid==jid): s.room.msg(u'Не смешная шутка!')
  elif s.jid == jid and nick != "": s.room.msg(nick + u', ты в своем уме?')
  elif s.jid != jid: s.room.msg(STRING.replace('%s', nick))
  else: s.room.msg(u'Кого будем троллить?')
 else:
  s.msg(u'Данная команда работает только внутри конференции')

bot.register_cmd_handler(bump_msg, u'.bump', 0, True)

