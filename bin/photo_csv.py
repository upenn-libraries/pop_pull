#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import re
import csv
import codecs
import unicodedata

json_re = re.compile('\.json$')
files = []
# files.append(so.path.join(os.path.dirname(__file__), '..', 'POP_0001.json'))
data_dir =  os.path.join(os.path.dirname(__file__), '..', 'data')
rows = []

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

class Book:
    NORMAL_RE  = re.compile('\W')
    FOLIO_RE   = re.compile('^Folio\s*', re.IGNORECASE)

    names = ('call',
             'bibid',
             'title',
             'author',
             'conference',
             'pub',
             'date',
             'provenance',
             'printplace')

    def __init__(self, line):
        self._line = line.rstrip('\r\n')
        self._parts = self._line.split('\t')
        self._props = {}
        # call, bibid, title, author, conference, pub, date, provenance, printplace
        for i in xrange(len(self.names)):
            if len(self._parts) > i:
                self._props[self.names[i]] = self._parts[i]

    @property
    def normal_callno(self):
        s = self._props['call']
        if self.FOLIO_RE.search(s):
            s = self.FOLIO_RE.sub('', s)
            s += 'folio'
        return self.NORMAL_RE.sub('', s.lower())

class Books:

    def __init__(self, tsv):
        self._tsv = tsv
        self._call_to_bibid = {}
        self._books = []
        self._callno_map = {}
        self._index = 0
        self._load_tsv()

    def _load_tsv(self):
        for line in codecs.open(self._tsv, 'r', 'utf-8'):
            try:
                book = Book(line)
                self._books.append(book)
                self._callno_map[book.normal_callno] = book
            except ValueError as ex:
                print "Bad line: %s" % (line,)
                raise ex

    def __iter__(self):
        return self

    def find(self, normal_callno):
        return self._callno_map.get(normal_callno, None)

    def next(self):
        if self._index >= len(self._books):
            raise StopIteration
        self._index += 1
        return self._books[self._index - 1]

class Categories:
    NOT_FOUND = ('NOT_FOUND', 'NOT_FOUND')
    DEFAULT_CAT = 'TBD'

    def __init__(self, csv):
        "Create a new list of categories"
        self.csv = csv
        self.cat_set = set()
        self.tags = {}
        self.load_csv()

    def load_csv(self):
        for line in codecs.open(self.csv, 'r', 'utf-8'):
            try:
                # Ugly	Clean	Mitch's Category	Laura's Category	Model	Field	Basis
                # zaravoni	Zaravoni	Person	Person	Copy	Author	Transcription | Secondary | Imagery Description | Heraldry Description
                ugly, raw, mitch, laura, model, field = line.rstrip('\n').split('\t')
                # ugly, raw, model, field = row[:]
                cat = (model.strip().lower(),field.strip().lower())
                self.tags[raw] = cat
                self.cat_set.add(cat)
            except:
                print "Problem: %r" % line
                raise
        self.cat_set.add(Categories.NOT_FOUND)
        self.cats = list(self.cat_set)
        self.cats.sort()

class Photo:
    def __init__(self,record):
        "Create a photo thingy."
        self.photo_dict = record
        self._tag_map = {}

    @property
    def photo(self):
        return self.photo_dict['photo']

    def _stringify(self, s):
        return str(s.encode('utf-8')).strip()

    @property
    def pid(self):
        # return self._stringify(self.photo['id'])
        return self.photo['id']

    @property
    def title(self):
        # print 'title: %s' % (self.photo['title'], )
        # return self._stringify(self.photo['title'])
        return self.photo['title']

    @property
    def url(self):
        # return self._stringify(self.photo['urls']['url'][0]['text'])
        return self.photo['urls']['url'][0]['text']

    @property
    def tags(self):
        return self.photo['tags']['tag']

    def all_tag_vals(self, key):
        return [ x[key] for x in self.tags]

    @property
    def raw_tags(self):
        return self.all_tag_vals('raw')

    @property
    def text_tags(self):
        return self.all_tag_vals('text')

    def map_tags(self, categories):
        self._tag_map[Categories.NOT_FOUND] = []
        for cat in categories.cats:
            self._tag_map[cat] = []

        for tag in self.raw_tags:
            tag = unicodedata.normalize('NFC', tag)
            if tag in categories.tags:
                cat = categories.tags[tag]
            else:
                cat = Categories.NOT_FOUND
                sys.stderr.write("Tag not found: %s; photo_id: %s\n" % (tag, self.pid))
            self._tag_map[cat].append(tag)

    def mapped_tags(self, categories):
        if len(self._tag_map) == 0:
            self.map_tags(categories)
        return self._tag_map

    def call_nos(self):
        if len(self._tag_map) > 0 and self._tag_map.get((u'copy', u'call number'), None):
            return self._tag_map[(u'copy',u'call number')]
        else:
            return []

cats = Categories(sys.argv[1])
print cats.cats

books = Books(os.path.join(data_dir, 'call_bidid_map.tsv'))

# get the Photo JSON files
for fname in os.listdir(os.path.join(data_dir, 'NFC')):
    if re.search(json_re, fname):
        files.append(fname)

photos = None


head = [ 'ID', 'Title', 'URL', 'BibID' ]
for cat in cats.cats:
    head.append(':'.join(cat))

for fname in files:
    records = json.load(codecs.open(os.path.join(data_dir,'NFC',fname), 'r', 'utf-8'))
    for record in records:
        photo = Photo(record)
        row = [ photo.pid, photo.title, photo.url ]
        tags = photo.mapped_tags(cats)
        bibids = []
        for call in photo.call_nos():
            book = books.find(call)
            if book:
                bibids.append(book._props['bibid'])
        row.append('|'.join(bibids))
        for cat in cats.cats:
            row.append('|'.join(tags[cat]))
        rows.append(row)

outfile = codecs.open("photos_mapped.csv", "w+", 'utf-8')
outfile.write(u'\t'.join(head))
outfile.write('\n')
for row in rows:
    outfile.write(u'\t'.join(row))
    outfile.write('\n')

outfile.close()
print "Wrote \"%s\"" % outfile.name
