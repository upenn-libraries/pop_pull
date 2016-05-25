#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import unicodedata

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
    for line in f:
        print(unicodedata.normalize('NFC', line.rstrip('\n')))
