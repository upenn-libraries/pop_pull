#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import unicodedata
import re

# <U+200F>
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
rtl = '\u200F'.decode( 'unicode-escape' )
ltr = '\u200E'.decode( 'unicode-escape' )
bidi_re = re.compile("[%s%s]+" % (rtl, ltr), re.UNICODE)

with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
    for line in f:
        print(bidi_re.sub('', line.rstrip('\n')))
