import os
import sys
import json
import re
import csv

json_re = re.compile('\.json$')
files = []
data_dir =  os.path.join(os.path.dirname(__file__), '..', 'data')
rows = []

class Categories:
    DEFAULT_CAT = 'TBD'

    def __init__(self, csv):
        "Create a new list of categories"
        self.csv = csv
        self.cat_set = set()
        self.tags = {}
        self.load_csv()

    def load_csv(self):
        rdr = csv.reader(open(self.csv))
        for row in rdr:
            try:
                # Ugly	Clean	Mitch's Category	Laura's Category	Model	Field	Basis
                # zaravoni	Zaravoni	Person	Person	Copy	Author	Transcription | Secondary | Imagery Description | Heraldry Description
                ugly, cat, mitch, laura, model, field, basis = row[:]

                self.tags[cat] = (model,field)
                self.cat_set.add(cat)
            except:
                print "Problem: %r" % row
                raise
        self.cat_set.add('NOT_FOUND')
        self.cats = list(self.cat_set)
        self.cats.sort()

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
        return self._stringify(self.photo['id'])

    @property
    def title(self):
        return self._stringify(self.photo['title'])

    @property
    def url(self):
        return self._stringify(self.photo['urls']['url'][0]['text'])

    @property
    def tags(self):
        return self.photo['tags']['tag']

    def all_tag_vals(self, key):
        return [ self._stringify(x[key]) for x in self.tags]

    @property
    def raw_tags(self):
        return self.all_tag_vals('raw')

    @property
    def text_tags(self):
        return self.all_tag_vals('text')

    def mapped_tags(self, categories):
        tag_map = {}
        tag_map['NOT_FOUND'] = []
        for cat in categories.cats:
            tag_map[cat] = []

        for raw in self.raw_tags:
            s = raw.strip().upper()
            cat = categories.tags[s] if s in categories.tags else "NOT_FOUND"
            tag_map[cat].append(raw)
        return tag_map

def stringify(s):
    return s.encode('utf-8')

#cats = Categories(os.path.join(data_dir, sys.argv[0]))
cats = Categories(sys.argv[1])
print cats.cats

# for fname in os.listdir(data_dir):
#     if re.search(json_re, fname):
#         files.append(fname)

# photos = None

# head = [ 'ID', 'Title', 'URL' ]
# for cat in cats.cats:
#     head.append(cat)

# for fname in files:
#     records = json.load(open(os.path.join(data_dir,fname)))
#     for record in records:
#         photo = Photo(record)
#         row = [ photo.pid, photo.title, photo.url ]
#         tags = photo.mapped_tags(cats)
#         for cat in cats.cats:
#             row.append('|'.join(tags[cat]))
#         rows.append(row)

# outfile = open("photos_laura.csv", "w+")
# csv_writer = csv.writer(outfile)
# csv_writer.writerow(head)
# csv_writer.writerows(rows)
# outfile.close()
# print "Wrote \"%s\"" % outfile.name
