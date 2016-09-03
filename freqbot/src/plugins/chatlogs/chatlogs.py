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

# here we use some parts of Neutron code http://svn.hypothetic.org/neutron/trunk/plugins/log_plugin.py
# html/css design copied from ejabberd chatlogs

from twisted.web.html import escape
from twisted.words.protocols.jabber import jid

def read_file(f):
 q = open(f, 'r')
 s = q.read().decode('utf8', 'replace')
 q.close()
 return s

LOG_FILES = {}
TOPICS = {}
log_header = read_file('templates/chatlog_header.html')
log_footer = read_file('templates/chatlog_footer.html')

def check_dir(s):
 if not os.access(s, os.F_OK): os.mkdir(s)

def write_to_log(groupchat, text, with_timestamp=True, with_br=True):
 if config.CHATLOGS_IN_MAIN_THREAD:
  reactor.callFromThread(write_to_log_, groupchat, text, with_timestamp, with_br)
 else: write_to_log_(groupchat, text, with_timestamp, with_br)

def write_to_log_(groupchat, text, with_timestamp=True, with_br=True):
 p1 = '%s/%s' % (config.CHATLOGS_DIR, groupchat.encode('utf8', 'replace'))
 p2 = '%s/%s' % (p1, time.strftime('%Y'))
 p3 = '%s/%s' % (p2, time.strftime('%m'))
 p4 = '%s/%s.html' % (p3, time.strftime('%d'))
 if (groupchat in LOG_FILES) and (LOG_FILES[groupchat] <> p4):
  close_log(LOG_FILES[groupchat])
  LOG_FILES[groupchat] = p4
  topic = TOPICS.get(groupchat)
  if topic: chatlogs_topic_handler(groupchat, topic, immediately=True)
 LOG_FILES[groupchat] = p4
 if not os.access(p4, os.F_OK):
  check_dir(p1)
  check_dir(p2)
  check_dir(p3)
  fp = file(p4, 'w')
  user, server = groupchat.split(u'@')
  header = log_header.replace('$user', user).replace('$server', server).replace('$year', time.strftime('%Y'))
  header = header.replace('$month', time.strftime('%m')).replace('$day', time.strftime('%d'))
  header = header.replace('$lang', lang.getLang(groupchat))
  prev = time.strftime('../../%Y/%m/%d.html', time.localtime(time.time()-86400))
  next = time.strftime('../../%Y/%m/%d.html', time.localtime(time.time()+86400))
  header = header.replace('$next', next).replace('$prev', prev)
  fp.write(header.encode('utf8', 'replace'))
  fp.close()
 if with_timestamp: tm = time.strftime(u'<a name="%H:%M:%S" href="#%H:%M:%S" class="ts">[%H:%M:%S]</a>')
 else: tm = u''
 text = u'%s %s' % (tm, text)
 if with_br: text = text + u'<br/>\n'
 fp = file(p4, 'a')
 fp.write(text.encode('utf8', 'replace'))
 fp.close()

def close_log(fn):
 if os.access(fn, os.W_OK):
  fp = file(fn, 'a')
  fp.write(log_footer.encode('utf8', 'replace'))
  fp.close()

def log_regex_url(matchobj):
 # 06.03.05(Sun) slipstream@yandex.ru urls parser
 return '<a href="' + matchobj.group(0) + '">' + matchobj.group(0) + '</a>'

def replace_links(text):
 return re.sub(u'(http|https|ftp)(\:\/\/[^\s<]+)', log_regex_url, text)

def chatlogs_msg_handler(source, body):
 if not body: return
 else: body = body.strip()
 j = jid.JID(source)
 room = j.userhost()
 nick = j.resource
 if not nick: nick = room
 if (room in bot.g.keys()) and (bot.g[room].get_option('chatlogs', config.CHATLOGS_ENABLE)=='on'):
  if body.startswith(u'/me ') and (len(body)>4):
   m = u'<font class="mne">* %s %s</font>' % (escape(nick), replace_links(escape(body[4:]).replace('\n', '<br/>')))
  else:
   m = u'<font class="mn">&lt;%s&gt;</font> %s' % (escape(nick), replace_links(escape(body).replace('\n', '<br/>')))
  write_to_log(room, m)

def chatlogs_topic_handler(source, subject, immediately=False):
 j = jid.JID(source)
 room = j.userhost()
 #bot.g[room].topic = subject
 #print 'try print subject..'
 #print [subject]
 TOPICS[room] = subject
 nick = j.resource
 #print [nick]
 if (bot.g[room].get_option('chatlogs', config.CHATLOGS_ENABLE)=='on'):
  if nick:
   #print [nick]
   m = lang.msg('chatlog_change_subject', (escape(nick), replace_links(escape(subject).replace('\n', '<br/>'))), lang.getLang(source))
   #print [m]
   m = u'<font class="roomcsubject">' + m + u'</font>\n'
   #print [m]
  else:
   m = lang.msg('chatlog_subject', (replace_links(escape(subject).replace('\n', '<br/>')), ), lang.getLang(source))
   m = u'<div class="roomsubject">' + m + u'</div>\n'
  #print 'let\'s write_to_log'
  #print (room, m, nick <> None)
  if immediately: write_to_log_(room, m, nick <> None, nick <> None)
  else: write_to_log(room, m, nick <> None, nick <> None)
 else: bot.log.log('got subject.. but logs disabled', 2)

def chatlogs_join_handler(item):
 if item.room and (item.room.get_option('chatlogs', config.CHATLOGS_ENABLE)=='on'):
  m = u'<font class="mj">%s %s</font>' % (escape(item.nick), lang.get('chatlog_joined', lang.getLang(item.jid)))
  write_to_log(item.room.jid, m)

def chatlogs_leave_handler(item, typ, reason):
 # typ: 0: leave
 #      1: kick
 #      2: ban
 #      3: rename
 if item.room and (item.room.get_option('chatlogs', config.CHATLOGS_ENABLE)=='on'):
  if typ == 0:
   if reason: m = lang.msg('chatlog_leaved_reason', (escape(reason), ), lang.getLang(item.jid))
   else: m = lang.get('chatlog_leaved', lang.getLang(item.jid))
  elif typ == 1:
   if reason: m = lang.msg('chatlog_kicked_reason', (escape(reason), ), lang.getLang(item.jid))
   else: m = lang.get('chatlog_kicked', lang.getLang(item.jid))
  elif typ == 2:
   if reason: m = lang.msg('chatlog_banned_reason', (escape(reason), ), lang.getLang(item.jid))
   else: m = lang.get('chatlog_banned', lang.getLang(item.jid))
  elif typ == 3:
   m = lang.msg('chatlog_changed_nick', (escape(item.nick), ), lang.getLang(item.jid))
  if typ == 3: nick = reason
  else: nick = item.nick
  m = u'<font class="ml">%s %s</font>' % (escape(nick), m)
  write_to_log(item.room.jid, m)

if config.CHATLOGS_ALLOW_SWICH: log_access = 11
else: log_access = 50

def enable_logging(t, s, p):
 if s.room.get_option('chatlogs', config.CHATLOGS_ENABLE) == 'on':
  s.lmsg(t, 'chatlogs_already_enabled')
 else:
  s.room.set_option('chatlogs', 'on')
  s.lmsg(t, 'chatlogs_enabled')

def disable_logging(t, s, p):
 if s.room.get_option('chatlogs', config.CHATLOGS_ENABLE) == 'off':
  s.lmsg(t, 'chatlogs_already_disabled')
 else:
  s.room.set_option('chatlogs', 'off')
  s.lmsg(t, 'chatlogs_disabled')

bot.register_cmd_handler(enable_logging, '.enable_logging', log_access, True)
bot.register_cmd_handler(disable_logging, '.disable_logging', log_access, True)
bot.register_msg_handler(chatlogs_msg_handler, g=True)
bot.register_topic_handler(chatlogs_topic_handler)
bot.register_join_handler(chatlogs_join_handler)
bot.register_leave_handler(chatlogs_leave_handler)

# We should have write access to config.CHATLOGS_DIR
if os.access(config.CHATLOGS_DIR, os.W_OK) == 0:
 os.mkdir(config.CHATLOGS_DIR)
 os.mkdir(config.CHATLOGS_DIR+'/images')
 from shutil import copyfile
 for img in ['powered-by-freq.png', 'powered-by-python.png', 'valid-css.gif', 'valid-xhtml.png']:
  copyfile('static/'+img, config.CHATLOGS_DIR+'/images/'+img)
