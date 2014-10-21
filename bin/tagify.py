# -*- coding: utf-8 -*-
import os
import sys
import csv
import re
import unicodedata

sys.path.append(os.path.dirname(__file__))
from unicode_csv import UTF8Recoder, UnicodeReader, UnicodeWriter

rdr = UnicodeReader(open(sys.argv[1]))
tag_re = re.compile('\W', re.UNICODE)
clean_re = re.compile('[\s"!@#\$%^&*():_+=\'/.;`<>\[\]?\\-]')

# clean_tag = raw_tag.gsub(/[\\s"!@#\\$\\%^&*():\\-_+=\\'\\/.;`<>\\[\\]?\\\\]/,"").downcase


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


outfile = open('updated_tags.orig.csv', 'w+')

wrtr = UnicodeWriter(outfile, delimiter='\t')
head = [ 'Normalized', 'Raw', 'Model', 'field' ]
wrtr.writerow(head)

for row in rdr:
    new_row = []
    ugly, raw, mitch, laura, model, field, basis = row[:]
    new_row = [ ugly, raw, model, field ]

    if ugly:
        new_row = [ ugly, raw, model, field ]
    else:
        u = unicodedata.normalize('NFC', raw)
        u = tag_re.sub('', u.strip().lower())
        new_row = [ u, raw, model, field ]
    wrtr.writerow(new_row)

outfile.close()
print "Wrote \"%s\"" % (outfile.name, )
