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

# __NEED_DB__

class nickstorage_not_found(Exception):
 pass

class nickstorage_error(Exception):
 pass

class nickstorage:
 """
 Database storage, should be thread-safe
 Fields: room, jid, nick, ftime, ltime, ltype, lreason
 ltype: [0: leave, 1: kick, 2: ban, 3: changes nick]
 """
 def __init__(self, bot):
  self.db = db.database('users')
  self.bot = bot
  q = self.db.query('select count(*) from SQLITE_MASTER where type="table" and tbl_name="users"')
  if q.fetchone()[0] == 0:
   self.bot.log.log('Create table for nickstorage')
   self.db.query('create table users(room text, jid text, nick text, ftime integer, ltime integer, ltype integer, lreason text)')
   self.db.commit()
 
 def onJoin(self, item):
  reactor.callFromThread(self.bot.call, self._onJoin, item)
 
 def onLeave(self, item, typ, reason):
  reactor.callFromThread(self.bot.call, self._onLeave, item, typ, reason)
 
 def _onJoin(self, item):
  room = item.room.jid
  nick = item.nick
  jid = item.realjid
  ftime = int(time.time())
  ltime = ftime
  ltype = 0
  lreason = ''
  if self.db.query('select count(*) from users where room=? and jid=?', (room, jid)).fetchone()[0] == 0:
   n = 0
   while self.db.query('select count(*) from users where room=? and nick=?', (room, nick)).fetchone()[0] > 0:
    #ник занят, выбираем другой
    n += 1
    nick = item.nick + str(n)
   self.db.query('insert into users values (?, ?, ?, ?, ?, ?, ?)',\
   (room, jid, nick, ftime, ltime, ltype, lreason))
  else:
   self.db.query('update users set nick=? where room=? and jid=?', (nick, room, jid))
  self.db.commit()
 
 def _onLeave(self, item, typ, reason):
  room = item.room.jid
  jid = item.realjid
  ltime = int(time.time())
  ltype = typ
  lreason = reason
  self.db.query('update users set ltime=?, ltype=?, lreason=? where room=? and jid=?',\
  (ltime, ltype, lreason, room, jid))
  self.db.commit()
 
 def fetch_info(self, room, jid=None, nick=None):
  d = D()
  reactor.callFromThread(self.bot.call, self._fetch_info, room, jid, nick, d)
  return d
 
 def _fetch_info(self, room, jid, nick, d):
  if jid:
   if nick: c = self.db.query('select * from users where room=? and (jid=? or nick=?)',\
   (room, jid, nick))
   else: c = self.db.query('select * from users where room=? and jid=?', (room, jid))
  else: c = self.db.query('select * from users where room=? and nick=?', (room, nick))
  r = c.fetchall()
  if len(r) == 0: d.errback(nickstorage_not_found(''))
  elif len(r) == 1: d.callback(r)
  else:
   if jid and nick: d.callback(r)
   else:
    self.bot.log.err_e('Problems with database: jid %s or nick %s is not unique in room %s' % (jid, nick, room))
    d.errback(nickstorage_error('db'))
 
 def update(self, room, jid, nick):
  d = D()
  reactor.callFromThread(self.bot.call, self._update, room, jid, nick, d)
  return d
 
 def _update(self, room, jid, nick, d):
  cj = self.db.query('select count(*) from users where room=? and jid=?', (room, jid)).fetchone()[0]
  cn = self.db.query('select count(*) from users where room=? and nick=?', (room, nick)).fetchone()[0]
  if (cj == 1) and (cn == 0):
   # OK, jid exists and unique, nick does not exist..
   self.db.query('update users set nick=? where room=? and jid=?', (nick, room, jid))
   self.db.commit()
   d.callback(None)
  else: d.errback()

NickStorage = nickstorage(bot)
bot.register_join_handler(NickStorage.onJoin)
bot.register_leave_handler(NickStorage.onLeave)

def nickstorage_get(t, s, p):
 p = p.strip()
 d = NickStorage.fetch_info(s.room.jid, p, p)
 d.addCallback(nickstorage_get_result, t, s)
 d.addErrback(nickstorage_get_error, t, s)

def nickstorage_get_result(r, t, s):
 res = [u'%s => %s' % (i[1], i[2]) for i in r]
 s.msg(t, show_list(res))

def nickstorage_get_error(err, t, s):
 s.lmsg(t, 'not_found')
 #s.msg(t, repr(err.getTraceback()))

bot.register_cmd_handler(nickstorage_get, '.nickstorage_get', 11, True)

def nickstorage_set(t, s, p):
 p = p.strip()
 try: jid, nick = re.match('^([^=]+)=(.+)', p).groups()
 except:
  s.syntax(t, 'nickstorage_set')
  return
 d = NickStorage.update(s.room.jid, jid, nick)
 d.addCallback(nickstorage_set_result, t, s)
 d.addErrback(nickstorage_set_error, t, s)

def nickstorage_set_result(_, t, s):
 s.lmsg(t, 'ok')

def nickstorage_set_error(err, t, s):
 s.lmsg(t, 'failed')

bot.register_cmd_handler(nickstorage_set, '.nickstorage_set', 11, True)

def seen_handler(t, s, p):
 p = p.strip()
 if p:
  if p in s.room.keys() or [q for q in s.room.items.values() if q.realjid.startswith(p)]:
   s.lmsg(t, 'he_is_here', p)
  else:
   d = NickStorage.fetch_info(s.room.jid, p, p)
   d.addCallback(seen_result, t, s)
   d.addErrback(seen_error, t, s, p)
 else:
  s.lmsg(t, 'whom?')

def seen_error(err, typ, source, nick):
 if err.check(nickstorage_not_found):
  source.lmsg(typ, 'i_never_see_him', nick)
 elif err.check(nickstorage_error):
  source.lmsg(typ, 'some_error')
 else:
  source.msg(typ, str(err))
  raise

def seen_result(res, typ, source):
 ans = []
 for user in res:
  nick = user[2]
  ltime = user[4]
  ltype = user[5]
  lreason = user[6]
  stime = time2str(time.time() - ltime, True, source.get_lang())
  if lreason.strip():
   if ltype == 1: source.lmsg(typ, 'seen_kicked_here_reason', nick, stime, lreason)
   elif ltype == 2: source.lmsg(typ, 'seen_banned_here_reason', nick, stime, lreason)
   else: source.lmsg(typ, 'seen_was_here_reason', nick, stime, lreason)
  else:
   if ltype == 1: source.lmsg(typ, 'seen_kicked_here', nick, stime)
   elif ltype == 2: source.lmsg(typ, 'seen_banned_here', nick, stime)
   else: source.lmsg(typ, 'seen_was_here', nick, stime)

bot.register_cmd_handler(seen_handler, '.seen', g=True)
