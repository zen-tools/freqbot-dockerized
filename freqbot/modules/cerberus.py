# -*- coding: utf-8 -*-

import re


wBad = [
    u'(^|\s)мля(\S*)',
    u'(^|\s)(б|6)ля(\S*)',
    u'(\S*)ъ(е|e)(б|6)(\S*)',
    u'(\S*)ж(о|o|0)(п|n)(\S*)',
    u'(^|\s)вы(е|e)(б|6)(\S*)',
    u'(^|\s)и(п|n)(а|a)т(\S*)',
    u'(^|\s)(е|e|ё)(п|n)т(\S*)',
    u'(^|\s)и(п|n)(е|e)т(\s|$)',
    u'(^|\s)ии(п|n)(е|e)т(\s|$)',
    u'(^|\s)(х|x)(е|e)(р|p)(\S*)',
    u'(^|\s)и(п|n)(а|a)(л|ть)(\S*)',
    u'(\S*)м(у|y)д(о|а|o|a|@)(\S*)',
    u'(\S*)пид(а|о|o|a|@)(р|p)(\S*)',
    u'(^|\s)д(р|p)(о|o|0)(ч|4)(\S*)',
    u'(^|\s)(с|c)(у|y)(к|k)(а|a)(\S*)',
    u'(\S*)(х|x)(у|y)(й|и|я|е|e)(\S*)',
    u'(\S*)г(а|о|0|o|a)нд(0|о|o)н(\S*)',
    u'(^|\s)(з|3)(а|a)л(у|y)(п|n)(\S*)',
    u'(^|\s)(а|о)к(у|y)(е|e)нн(а|о)(\S*)',
    u'(\S*)(е|e)(б|6)(а|@)(т|н|t|h)(\S*)',
    u'(^|\s)(с|c)(р|p)(а|a)(к|т|k|t)(\S*)',
    u'(^|\s)(п|n)(и|e|е)(с|c|з|3)д(а|a)(\S*)',
    u'(^|\s)(с|c|3|з)(а|a)(е|e)пи(с|c)ь(\s|$)'
    u'(\S*)(п(и|e|е)|3\.14)(з|3|c|с)(д|т)(а|a|e|е)(\S*)',
]

wGood = [
    u'(^|\S*)страх(\S*)', u'дебаты', u'пестель'
]


class censor:
    def __init__(self):
        self.values = map(lambda x: re.compile(x, re.IGNORECASE), wBad)
        self.good = map(lambda x: re.compile(x, re.IGNORECASE), wGood)

    def respond(self, str):
        str = str.lower()
        for i in range(0, len(self.values)):
            # match = self.values[i].match(str)
            match = self.values[i].search(str)
            if match:
                resp = match.group().strip()
                for i in range(0, len(self.good)):
                    r = self.good[i].match(resp)
                    if r:
                        return None
                return resp


def command_interface():
    print "Therapist\n---------"
    print "Talk to the program by typing in plain English, using normal upper-"
    print 'and lower-case letters and punctuation.  Enter "quit" when done.'
    print '=' * 72
    print "Hello.  How are you feeling today?"
    s = ""
    therapist = censor()
    while s != "quit":
        try:
            s = raw_input(">")
        except EOFError:
            s = "quit"
            print s
        while s[-1] in "!.":
            s = s[:-1]
        print therapist.respond(s.decode('utf-8'))


if __name__ == "__main__":
    command_interface()
