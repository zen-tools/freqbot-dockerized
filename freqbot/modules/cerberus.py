# -*- coding: utf-8 -*-

import string
import re
import random

class censor:
  def __init__(self):
    self.values = map(lambda x:re.compile(x, re.IGNORECASE), wBad)
    self.good = map(lambda x:re.compile(x, re.IGNORECASE), wGood)

  def respond(self, str):
    str=str.lower()
    for i in range(0,len(self.values)):
#      match = self.values[i].match(str)
	match = self.values[i].search(str)
	if match:
	    resp = match.group().strip()
	    for i in range(0,len(self.good)):
		r = self.good[i].match(resp)
		if r:
		    return None
	    return resp

wBad = [u'(^|\s)(б|6)ля(\S*)', u'(\S*)(х|x)(у|y)(й|и|я|е|e)(\S*)',  #u'(^|\s)мля(\S*)',
	u'(\S*)(п(и|e|е)|3\.14)(з|3|c|с)(д|т)(а|a|e|е)(\S*)', u'(\S*)пид(а|о|o|a|@)(р|p)(\S*)', u'(\S*)(е|e)(б|6)(а|@)(т|н|t|h)(\S*)', u'(\S*)г(а|о|0|o|a)нд(0|о|o)н(\S*)',
	u'(^|\s)(з|3)(а|a)л(у|y)п(\S*)', u'(\S*)ж(о|o|0)п(\S*)', u'(^|\s)(с|c)(р|p)(а|a)(к|т|k|t)(\S*)',
	u'(\S*)м(у|y)д(о|а|o|a|@)(\S*)', u'(^|\s)ип(а|a)т(\S*)', u'(^|\s)вы(е|e)(б|6)(\S*)',
	u'(^|\s)иип(е|e)т(\s|$)', u'(^|\s)ип(е|e)т(\s|$)', u'(^| )(е|e|ё)пт(\S*)',
	u'(\S*)ъ(е|e)(б|6)(\S*)', u'(^| )д(р|p)(о|o|0)(ч|4)(\S*)', u'(^| )п(и|e|е)(с|c|з|3)д(а|a)(\S*)',
	u'(^| )(с|c|3|з)(а|a)(е|e)пи(с|c)ь(\s|$)', u'(^| )(а|о)к(у|y)(е|e)нн(а|о)(\S*)']
	 
wGood = [u'(^|\S*)страх(\S*)', 'пестель']

def command_interface():
  print "Therapist\n---------"
  print "Talk to the program by typing in plain English, using normal upper-"
  print 'and lower-case letters and punctuation.  Enter "quit" when done.'
  print '='*72
  print "Hello.  How are you feeling today?"
  s = ""
  therapist = censor();
  while s != "quit":
    try: s = raw_input(">")
    except EOFError:
      s = "quit"
      print s
    while s[-1] in "!.": s = s[:-1]
    print therapist.respond(s.decode('utf-8'))


if __name__ == "__main__":
  command_interface()