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

flickr_tags = set()
tag_source = os.path.join(os.path.dirname(__file__), '../data/tags_from_flickr.csv')
with open(tag_source) as f:
    tagreader = UnicodeReader(f)
    for tagrow in tagreader:
        text, raw, author = tagrow[:]
        flickr_tags.add(text)

outfile = open('updated_tags.orig.csv', 'w+')

wrtr = UnicodeWriter(outfile)
head = [ 'Normalized', 'Raw', 'Model', 'field' ]
wrtr.writerow(head)

for row in rdr:
    new_row = []
    ugly, raw, mitch, laura, model, field, basis = row[:]
    u = 'MISSING'
    if ugly:
        u = ugly if ugly in flickr_tags else ('CURR:NO_MATCH:%s' % ugly)
    else:
        ugly = unicodedata.normalize('NFC', raw)
        ugly = tag_re.sub('', ugly.strip().lower())
        u = ugly if ugly in flickr_tags else ('NEW:NO_MATCH:%s' % ugly)
    
    new_row = row[:]
    new_row[0] = u
    wrtr.writerow(new_row)

outfile.close()
print "Wrote \"%s\"" % (outfile.name, )
