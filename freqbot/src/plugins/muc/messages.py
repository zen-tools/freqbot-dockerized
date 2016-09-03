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

class msgbox_full(Exception):
 pass

class msg_ignored(Exception):
 pass

class room_pending(Exception):
 pass

class auth_request_sent(Exception):
 pass

class messagestorage:
 """
 used by .tell
 this class should be used only in main thread
 """
 def __init__(self, bot):
  self.db = db.database('messages')
  self.bot = bot
  q = self.db.query('select count(*) from SQLITE_MASTER where type="table" and tbl_name="messages"')
  if q.fetchone()[0] == 0:
   self.bot.log.log('Create tables for messages')
   self.db.query('create table messages(room text, fromjid text, tojid text, stime integer, msg text)')
   self.db.query('create table privacy(jid text, room text, mode integer)')
   self.db.commit()
 
 def privacy_add(self, jid, room, mode):
  """ mode is 0: ban or  1: whitelist """
  jid = jid.lower()
  room = room.lower()
  self.db.query('delete from privacy where jid=? and room=?', (jid, room))
  self.db.query('insert into privacy values(?, ?, ?)', (jid, room, mode))
  self.db.commit()
 
 def privacy_del(self, jid, room):
  jid = jid.lower()
  room = room.lower()
  self.db.query('delete from privacy where jid=? and room=?', (jid, room))
  self.db.commit()
 
 def privacy_clear(self, jid, mode):
  jid = jid.lower()
  self.db.query('delete from privacy where jid=? and mode=?', (jid, mode))
  self.db.commit()
 
 def privacy_get(self, jid, mode):
  jid = jid.lower()
  q = self.db.query('select room from privacy where jid=? and mode=?', (jid, mode))
  return [i[0] for i in q.fetchall()]
 
 def send_msg(self, room, fromjid, tojid, msg):
  fromjid = fromjid.lower()
  room = room.lower()
  tojid = tojid.lower()
  self.db.query('delete from messages where stime<?', (int(time.time())-config.MSG_TIME_TO_LIVE, ))
  msg = msg[:1200].strip()
  n = self.db.query('select count(*) from messages where tojid=?', (tojid, )).fetchone()[0]
  if n >= config.MSGBOX_SIZE:
   raise msgbox_full("His MSGBOX is full")
  m = self.db.query('select mode from privacy where room=? and jid=?', (room, tojid)).fetchall()
  if m:
   mode = m[0][0]
   if mode == 0:
    # this room in black list
    raise msg_ignored("Messages from this room are ignored by recipient")
   else:
    # this room in white list
    self.db.query('insert into messages values(?, ?, ?, ?, ?)', (room, fromjid, tojid, int(time.time()), msg))
    self.db.commit()
    self.try_deliver(tojid)
  else:
   # this room is not authorized to send messages to <tojid>
   n = self.db.query('select msg from messages where tojid=? and room=?', (tojid, room)).fetchall()
   if n:
    # this room is pending
    raise room_pending("This room is waiting for authorization")
   else:
    # send message (and authentication will be requested)
    self.db.query('insert into messages values(?, ?, ?, ?, ?)', (room, fromjid, tojid, int(time.time()), msg))
    self.db.commit()
    self.try_deliver(tojid)
    raise auth_request_sent("Message will be delivered after successful authorization.")
 
 def try_deliver(self, tojid):
  tojid = tojid.lower()
  for room in self.bot.g.keys():
   for nick in self.bot.g[room].keys():
    item = self.bot.g[room][nick]
    if item.realjid.lower() == tojid:
     self.deliver(item)
     return
 
 def deliver(self, item):
  tojid = item.realjid.lower()
  m = self.db.query('select room, fromjid, msg, stime from messages where tojid=?', (tojid, ))
  messages = m.fetchall()
  for room, fromjid, msg, stime in messages:
   m = self.db.query('select mode from privacy where jid=? and room=?', (tojid, room)).fetchall()
   if m:
    mode = m[0][0]
    if mode == 0:
     # this room is ignored
     pass
    else:
     # this room is white-listed
     try: nick = NickStorage.db.query('select nick from users where room=? and jid=?', \
     (room, fromjid)).fetchall()[0][0]
     except: nick = fromjid
     tm = time2str(time.time()-stime, True, item.get_lang())
     item.lmsg('chat', 'incoming_message', tm, nick, room, msg)
    # deleting this message from MSGBOX
    self.db.query('delete from messages where tojid=? and room=? and fromjid=? and msg=?', (tojid, room, fromjid, msg))
    self.db.commit()
   else:
    # request authentication
    item.lmsg('chat', 'msg_authentication_request', room, room, room)
    # do not delete this message from MSGBOX

MSGBOX = messagestorage(bot)

def msg_whitelist_handler(t, s, p):
 reactor.callFromThread(msg_privacylists_handler, t, s, p, 1)

def msg_blacklist_handler(t, s, p):
 reactor.callFromThread(msg_privacylists_handler, t, s, p, 0)

def msg_privacylists_handler(t, s, p, mode):
 """
 This function must be launched in main thread
 """
 p = p[:64].strip()
 if p:
  f = p.split()[0]
  if f == 'clear':
   MSGBOX.privacy_clear(s.realjid, mode)
   s.lmsg(t, 'cleared')
  elif f == 'show':
   q = MSGBOX.privacy_get(s.realjid, mode)
   ms = show_list(q, empty=s.get_msg('list_empty'))
   s.msg(t, ms)
  elif f == 'del':
   q = MSGBOX.privacy_get(s.realjid, mode)
   room = p[4:]
   if room in q:
    MSGBOX.privacy_del(s.realjid, room)
    s.lmsg(t, 'deleted')
   else: s.lmsg(t, 'not_found')
  else:
   MSGBOX.privacy_add(s.realjid, p, mode)
   s.lmsg(t, 'added')
   if mode == 1: MSGBOX.deliver(s)
 else: s.lmsg(t, 'invalid_syntax_default')

bot.register_cmd_handler(msg_whitelist_handler, '.msg_whitelist')
bot.register_cmd_handler(msg_blacklist_handler, '.msg_blacklist')

def tell_handler(t, s, p):
 if p.count(':'):
  n = p.find(':')
  nick = p[:n]
  text = p[n+1:].strip()
  if text:
   d = NickStorage.fetch_info(s.room.jid, None, nick)
   d.addCallback(tell_stage2, t, s, nick, text)
   d.addErrback(seen_error, t, s, nick)
  else:
   s.lmsg(t, 'tell_without_message')
 else:
  s.lmsg(t, 'invalid_syntax_default')

def tell_stage2(info, t, s, nick, text):
 tojid = info[0][1]
 try:
  MSGBOX.send_msg(s.room.jid, s.realjid, tojid, text)
  s.lmsg(t, 'msg_sent')
 except msgbox_full: s.lmsg(t, 'msgbox_is_full')
 except msg_ignored: s.lmsg(t, 'this_room_is_ignored')
 except room_pending: s.lmsg(t, 'room_pending')
 except auth_request_sent: s.lmsg(t, 'msg_auth_requested')

bot.register_cmd_handler(tell_handler, '.tell', 4, True)

def deliver_service_join_handler(item):
 reactor.callFromThread(MSGBOX.deliver, item)

bot.register_join_handler(deliver_service_join_handler)
