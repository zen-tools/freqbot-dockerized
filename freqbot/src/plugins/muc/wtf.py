#!/usr/bin/env python
# -*- coding: utf8 -*-
# __NEED_DB__
import sys

class Wtf:
    def __init__(self, bot):
        self.db = db.database('wtf')
        self.bot = bot
        q = self.db.query('select count(*) from SQLITE_MASTER where type="table" and tbl_name="wtf"')
        if q.fetchone()[0] == 0:
            self.bot.log.log('Create table for wtf')
            self.db.query('create table wtf(room text, wtf_id text, wtf_val text)')
            self.db.commit()

    def _wtf(self, room, wtf_id, d):
        c = self.db.query('select wtf_val from wtf where room=? and wtf_id=?',
            (room, wtf_id.lower()))
        if c:
            res = c.fetchone()
            if res:
                d.callback(res[0])
            else:
                d.callback(0)
        else: d.callback(0)
    
    def _dfn(self, room, wtf_id, wtf_val, d):
        try:
            if self.db.query('select count(*) from wtf where room=? and wtf_id=?',
                (room, wtf_id.lower())).fetchone()[0] == 0:
                self.db.query('insert into wtf values (?, ?, ?)',
                    (room, wtf_id.lower(), wtf_val))
            else:
                self.db.query('update wtf set wtf_val=? where room=? and wtf_id=?',
                    (wtf_val, room, wtf_id.lower()))
            self.db.commit()
            d.callback(0)
        except:
			error = sys.exc_info()[0]
			d.errback(error)
        
    def _wtf_find(self, room, s, d):
        res = self.db.query('select wtf_id from wtf where room=? and wtf_id like ?',
                (room, '%%%s%%'%s.lower())).fetchall()
        if res:
            d.callback([u'%s'%i[0] for i in res])
        else:
            d.callback(0)
            
    def _wtf_count(self, room, d):
        try:
            d.callback(self.db.query('select count(*) from wtf where room=?',
                (room,)).fetchone()[0])
        except:
            error = sys.exc_info()[0]
            d.errback(error)
            
    def _wtf_words(self, room, d):
        try:
            res = self.db.query('select wtf_id from wtf where room=?',
                (room,)).fetchall()
            if res:
                d.callback([u'%s'%i[0] for i in res])
            else:
                d.callback(0)
        except:
			error = sys.exc_info()[0]
			d.errback(error)

    def wtf(self, room, wtf_id):
        d = D()
        reactor.callFromThread(self.bot.call, self._wtf, room, wtf_id, d)
        return d
    
    def dfn(self, room, wtf_id, wtf_val):
        d = D()
        reactor.callFromThread(self.bot.call, self._dfn, room, wtf_id,
            wtf_val, d)
        return d
    
    def wtf_find(self, room, s):
        d = D()
        reactor.callFromThread(self.bot.call, self._wtf_find, room, s, d)
        return d
        
    def wtf_count(self, room):
        d = D()
        reactor.callFromThread(self.bot.call, self._wtf_count, room, d)
        return d
        
    def wtf_words(self, room):
        d = D()
        reactor.callFromThread(self.bot.call, self._wtf_words, room, d)
        return d

wt = Wtf(bot)

def wtf(t, s, p):
    p = p.strip()
    if p:
        d = wt.wtf(s.room.jid, p)
        d.addCallback(wtf_result, t, s)
        d.addErrback(wtf_error, t, s)
    else:
        s.syntax(t, 'wtf')

def wtf_find(t, s, p):
    p = p.strip()
    if p:
        d = wt.wtf_find(s.room.jid, p)
        d.addCallback(wtf_find_result, t, s)
        d.addErrback(wtf_error, t, s)
    else:
        s.lmsg(t, 'google?')

def wtf_count(t, s, p):
    d = wt.wtf_count(s.room.jid)
    d.addCallback(wtf_count_result, t, s)
    d.addErrback(wtf_error, t, s)

def wtf_words(t, s, p):
    d = wt.wtf_words(s.room.jid)
    d.addCallback(wtf_find_result, t, s)
    d.addErrback(wtf_error, t, s)

def dfn_handler(t, s, p):
    k, v = p.strip().split('=', 1)
    if k and v:
        d = wt.dfn(s.room.jid, k, v)
        d.addCallback(wtf_set_result, t, s)
        d.addErrback(wtf_error, t, s)
    else:
        s.syntax(t, 'wtfset')

def wtf_result(r, t, s):
    if r:
        s.msg(t, r)
    else:
        s.lmsg(t, 'not_found')

def wtf_error(err, t, s):
    s.lmsg(t, 'Error %s'%(err, ))

def wtf_find_result(r, t, s):
    if r:
        s.msg(t, show_list(r))
    else:
        s.lmsg(t, 'not_found')

def wtf_count_result(r, t, s):
    s.msg(t, u'%s штук'%r)
    
def wtf_set_result(r, t, s):
    s.lmsg(t, 'ok')


bot.register_cmd_handler(wtf, '.wtf', 0, True)
bot.register_cmd_handler(wtf_find, '.wtfsearch', 0, True)
bot.register_cmd_handler(wtf_count, '.wtfcount', 0, True)
bot.register_cmd_handler(wtf_words, '.wtfall', 0, True)
bot.register_cmd_handler(dfn_handler, '.dfn', 11, True)
