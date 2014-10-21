# -*- coding: utf-8 -*-
import os
import sys
import csv
import re

rdr = csv.reader(open(sys.argv[1]))
tag_re = re.compile('\W', re.UNICODE)
clean_re = re.compile('[\s"!@#\$%^&*():_+=\'/.;`<>\[\]?\\-]')

# clean_tag = raw_tag.gsub(/[\\s"!@#\\$\\%^&*():\\-_+=\\'\\/.;`<>\\[\\]?\\\\]/,"").downcase


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


outfile = open('updated_tags.orig.csv', 'w+')

wrtr = csv.writer(outfile)
head = [ 'Normalized', 'Raw', 'Model', 'field' ]
wrtr.writerow(head)

for row in rdr:
    new_row = []
    ugly, tag, mitch, laura, model, field, basis = row[:]
    if ugly:
        new_row = [ ugly, tag, model, field ]
    else:
        u = tag_re.sub('', unicode(tag,'utf-8').lower())
        new_row = [ u.encode('utf-8'), unicode(tag, 'utf-8').encode('utf-8'), model, field ]
    wrtr.writerow(new_row)

outfile.close()
print "Wrote \"%s\"" % (outfile.name, )
