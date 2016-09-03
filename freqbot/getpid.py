#!/usr/bin/python

import sys, os
wd = os.path.dirname(sys.argv[0])
if not wd: wd = '.'
os.chdir(wd)
sys.path.insert(0, 'src/kernel')
import config
config.init(sys.argv[1])

try:
 f = file(config.PIDFILE, 'r')
 p = f.read()
 f.close()
 if p: print p
 else: print "x"
except:
 sys.stderr.write('Can\'t read pidfile: %s\n' % (config.PIDFILE, ))
 sys.exit(1)
