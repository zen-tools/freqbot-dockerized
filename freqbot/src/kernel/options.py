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
import os
from urllib import quote, unquote
from config import DATADIR

if not os.access(DATADIR + '/db', os.W_OK): os.mkdir(DATADIR + '/db')

enc = 'utf8'

def list2dict(q):
 p = {}
 for i in q:
  t = i.find(u'=')
  p[i[:t]] = i[t+1:]
 return p

def dict2list(q):
 #print q
 return [u'%s=%s' % (i, q[i]) for i in q.keys()]

def check_directory(groupchat):
 groupchat = groupchat.encode(enc)
 preprefix = '%s/text' % (DATADIR, )
 prefix='%s/text/groupchats' % (DATADIR, )
 d = '%s/%s' % (prefix, groupchat, )
 if not os.access(DATADIR, os.W_OK): os.mkdir(DATADIR)
 if not os.access(preprefix, os.W_OK): os.mkdir(preprefix)
 if not os.access(prefix, os.W_OK): os.mkdir(prefix)
 if not os.access(d, os.W_OK): os.mkdir(d)

def read_file(groupchat, f):
 fn = '%s/text/groupchats/%s/%s.txt' % (DATADIR, groupchat.encode('utf8'), f)
 fp = file(fn, 'r')
 r = fp.read()
 fp.close()
 return r.decode(enc)

def write_file(groupchat, f, text):
 check_directory(groupchat)
 fn = '%s/text/groupchats/%s/%s.txt' % (DATADIR, groupchat.encode('utf8'), f)
 fp = file(fn, 'w')
 fp.write(text.encode(enc))
 fp.close()

# =================================================================
class optstringlist:
 def __init__(self, fname):
  self.values = {}
  self.fname = fname

 def __getitem__(self, groupchat):
  if not(groupchat in self.values.keys()):
   try: x = read_file(groupchat, self.fname).split('\n')
   except: x = []
   self.values[groupchat] = [unquote(i.strip().encode(enc)).decode(enc) for i in x if i.strip()]
  return self.values[groupchat]

 def __setitem__(self, groupchat, values):
  write_file(groupchat, self.fname, u'\n'.join([quote(i.encode(enc)).decode(enc) for i in values]))
  self.values[groupchat] = values
  #print [quote(i) for i in values]
  #print values
# =================================================================

OPTIONS = optstringlist('options')

def get_option(groupchat, k, d = None):
 return list2dict(OPTIONS[groupchat]).get(k, d)

def set_option(groupchat, k, v):
 t = list2dict(OPTIONS[groupchat])
 t[k] = v
 OPTIONS[groupchat] = dict2list(t)
