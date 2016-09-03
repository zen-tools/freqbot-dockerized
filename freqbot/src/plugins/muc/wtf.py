#!/usr/bin/env python
# -*- coding: utf8 -*-
#~#######################################################################
#~ Copyright (c) 2008 Burdakov Daniel <kreved@kreved.org>               #
#~ Copyright (c) 2010 Kazakov Alexandr <ferym@jabber.ru>                #
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

import sqlite3
from random import randint
import string

wtfbase = config.DBDIR+'/wtf.db'

def dfn_handler(t, s, params):
  if params:
   cn = sqlite3.connect(wtfbase)
   cr = cn.cursor()
   kv = string.split(params, '=', 1)
   if not len(kv)<2:
    key = string.lower(kv[0]).strip()
    val = kv[1].strip()
    if not val:
     try:
      cr.execute('delete from wtf where room=? and key=?',(s.room.jid,key))
      cn.commit()
      cn.close()
      s.lmsg(t,'dfn_remove')
     except: s.lmsg(t,'dfn_failed')
    else:
     cr.execute('delete from wtf where room=? and key=?',(s.room.jid,key))
     cr.execute('insert into wtf values (?,?,?)',(s.room.jid,key,val+"\n(by %s %s)" % (s.nick,time.strftime("%d.%m.%Y %H:%M:%S"))))
     cn.commit()
     cn.close()
     s.lmsg(t,'dfn_save')
   else: s.lmsg(t,'dfn_empty')
  else: s.lmsg(t,'dfn_empty')

def wtf_handler(t,s,params):
 if not params: s.lmsg(t,'wtf_empty'); return
 cn = sqlite3.connect(wtfbase)
 cr = cn.cursor()
 try:
  res = cr.execute('select val from wtf where room=? and key=?',(s.room.jid,params)).fetchone()
  s.lmsg(t,'wtf_result',params,''.join(res))
  cn.close()
 except: s.lmsg(t,'wtf_not_found'); cn.close()
 
def wtfnames_handler(t,s,params):
 cn = sqlite3.connect(wtfbase)
 cr = cn.cursor()
 keys = cr.execute('select * from wtf where room=?',(s.room.jid,))
 res = []
 try:
  for i in keys:
   res.append(i[1])
  if len(res)==0: s.lmsg(t,'wtfnames_empty'); return
  s.lmsg(t,'wtfnames_result',', '.join(res),str(len(res)))
  cn.close()
 except: s.lmsg(t,'failed'); cn.close()
 
def wtfsearch_handler(t,s,params):
 if not params: s.lmsg(t,'wtfsearch_not_parameters'); return
 cn = sqlite3.connect(wtfbase)
 cr = cn.cursor()
 params = '%'+params+'%'
 try:
  res = cr.execute('select * from wtf where (room=?) and (key like ? or val like ?)',(s.room.jid,params,params))
  out = []
  for i in res:
   out.append(i[1])
  if len(out)<1: s.lmsg(t,'wtfsearch_error'); return
  s.lmsg(t,'wtfsearch_result',', '.join(out))
  cn.close()
 except: s.lmsg(t,'wtfsearch_error'); cn.close()


bot.register_cmd_handler(dfn_handler, '.dfn', 9)
bot.register_cmd_handler(wtf_handler, '.wtf')
bot.register_cmd_handler(wtfnames_handler, '.wtfnames')
bot.register_cmd_handler(wtfsearch_handler, '.wtfsearch')
