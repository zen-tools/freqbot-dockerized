#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# Copyright (c) 2014-2016 Dmitry Poltavchenko <admin@linuxhub.ru>      #
#                                                                      #
# This file is part of FreQ-bot.                                       #
#                                                                      #
# FreQ-bot is free software: you can redistribute it and/or modify     #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# FreQ-bot is distributed in the hope that it will be useful,          #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with FreQ-bot.  If not, see <http://www.gnu.org/licenses/>.    #
########################################################################

# by zen

import random
import itertools

TOTAL_IDS_CNT = 22
SHUFFLED_PHR_IDS = None
SHUFFLED_PHR_CNT = 0


def get_jid(source, p):
    if p:
        if source.room:
            if p in source.room.items.keys():
                return source.room[p].jid
        return p
    else:
        return source.jid


def get_next_phrase_id():
    global SHUFFLED_PHR_IDS, SHUFFLED_PHR_CNT, SHUFFLED_PHR_TTL

    if SHUFFLED_PHR_CNT % (TOTAL_IDS_CNT * 2) == 0:
        SHUFFLED_PHR_IDS = None

    if SHUFFLED_PHR_IDS is None:
        phrases_ids = ['bump_phrase_' + str(i) for i in xrange(TOTAL_IDS_CNT)]
        random.shuffle(phrases_ids)
        SHUFFLED_PHR_IDS = itertools.cycle(phrases_ids)

    SHUFFLED_PHR_CNT += 1
    return SHUFFLED_PHR_IDS.next()


def bump_msg(t, s, p):
    phrase_id = get_next_phrase_id()
    nick = p.strip('\r\n ')
    jid = get_jid(s, nick)
    if s.room:
        if nick == jid:
            s.room.msg(lang.msg('bump_no_jid'))
        elif s.room.bot and (s.room.bot.jid == jid):
            s.room.msg(lang.msg('bump_freq'))
        elif s.jid == jid and nick != "":
            s.room.msg(lang.msg('bump_self', [nick]))
        elif s.jid != jid:
            s.room.msg(lang.msg(phrase_id, [nick]))
        else:
            s.room.msg(lang.msg('bump_no_nick'))
    else:
        s.msg(lang.msg('bump_not_in_muc'))

bot.register_cmd_handler(bump_msg, u'.bump', 0, True)
