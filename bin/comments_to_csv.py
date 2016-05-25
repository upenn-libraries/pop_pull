#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import sys
import json
import re
import csv
import codecs
import unicodedata
import datetime
import unicodecsv

json_re = re.compile('\.json$')
files = []
# files.append(so.path.join(os.path.dirname(__file__), '..', 'POP_0001.json'))
data_dir =  os.path.join(os.path.dirname(__file__), '..', 'data')
rows = []

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

class Comment:
    def __init__(self, comments, record):
        self._comments = comments
        self._comment_dict = record

    @property
    def parent(self):
        return self._comments

    @property
    def id(self):
        return self._comment_dict['id']

    @property
    def url(self):
        return self._comment_dict['permalink']

    @property
    def authorname(self):
        return self._comment_dict['authorname']

    @property
    def text(self):
        return self._comment_dict['text']

    @property
    def date(self):
        tstamp = self._comment_dict['datecreate']
        return datetime.datetime.fromtimestamp(int(tstamp)).strftime('%Y-%m-%d %H:%M:%S')

class Comments:
    def __init__(self, record):
        self._comments_dict = record

    @property
    def comments_data(self):
        return self._comments_dict['comments']

    @property
    def photo_id(self):
        return self.comments_data['photo_id']

    @property
    def comments(self):
        return [ Comment(self,x) for x in self.comments_data['comment'] ]

class Photo:
    def __init__(self,record):
        "Create a photo thingy."
        self.photo_dict = record

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
    def comment_count(self):
        return int(self.photo['comments'])

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
    def updated(self):
        tstamp = self.photo['dates']['lastupdate']
        return datetime.datetime.fromtimestamp(int(tstamp)).strftime('%Y-%m-%d %H:%M:%S')

    @property
    def text_tags(self):
        return self.all_tag_vals('text')

    def mapped_tags(self, categories):
        tag_map = {}
        tag_map[Categories.NOT_FOUND] = []
        for cat in categories.cats:
            tag_map[cat] = []

        for tag in self.text_tags:
            tag = unicodedata.normalize('NFC', tag)
            if tag in categories.tags:
                cat = categories.tags[tag]
            else:
                cat = Categories.NOT_FOUND
                sys.stderr.write("Not found: %s\n" % tag)
            tag_map[cat].append(tag)
        return tag_map

comments_db = {}
for comment_file in glob.glob(os.path.join(data_dir, 'COMMENTS_*.json')):
    records = json.load(codecs.open(comment_file, 'r', 'utf-8'))
    for rec in records:
        comments = Comments(rec)
        comments_db[comments.photo_id] = comments

photos = []
for photo_file in glob.glob(os.path.join(data_dir, 'NFC', 'POP_*.json')):
    for rec in json.load(codecs.open(photo_file, 'r', 'utf-8')):
        photos.append(Photo(rec))

head = [ 'Photo tile', 'Photo ID', 'Photo URL', 'Photo Date', 'Comment Date', 'Comment', 'Comment Author', 'Comment URL' ]

rows = []

outfile = codecs.open("comments.tsv", "w+", 'utf-8')
outname = "comments.csv"
outfile = unicodecsv.writer(open(outname, 'w+'), encoding='utf-8')
outfile.writerow(head)
# outfile.write(u'\t'.join(head))
# outfile.write('\n')
for photo in photos:
    try:
        comments = comments_db[photo.pid]
        for comment in comments.comments:
            row = [ photo.title,
                    photo.pid,
                    photo.url,
                    photo.updated,
                    comment.date,
                    comment.text,
                    comment.authorname,
                    comment.url ]
            outfile.writerow(row)
            # outfile.write(u'\t'.join(row))
            # outfile.write('\n')
            # rows.append(row)
    except KeyError as ex:
        print "Could not find comments for photo: %13d; expected %2d" % (int(photo.pid), photo.comment_count)

    # outfile.write(u'\t'.join(row))
    # outfile.write('\n')
print "Wrote \"%s\"" % outname
