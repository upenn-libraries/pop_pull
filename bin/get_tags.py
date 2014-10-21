import os
import json


files = [ 'POP_0001.json',
          'POP_0002.json',
          'POP_0003.json',
          'POP_0004.json',
          'POP_0005.json',
          'POP_0006.json',
          'POP_0007.json',
          'POP_0008.json',
          'POP_0009.json',
          'POP_0010.json',
          'POP_0011.json',
          'POP_0012.json',
          'POP_0013.json',
          'POP_0014.json',
          'POP_0015.json',
          'POP_0016.json',
          'POP_0017.json',
          'POP_0018.json',
          'POP_0019.json',
          'POP_0020.json',
          'POP_0021.json',
          'POP_0022.json',
          'POP_0023.json',
          'POP_0024.json' ]

tags = dict();
this_dir = os.path.dirname(__file__)

for file in files:
    blerg = json.load(open(os.path.join(this_dir, '../data', file)))

    for item in blerg:
        for tag in item['photo']['tags']['tag']:
            text = tag['text']
            if (not text in tags):
                tags[text] = tag

for text in tags:
    t = str(text.encode('utf-8'))
    r = str(tags[text]['raw'].encode('utf-8'))
    a = str(tags[text]['authorname'].encode('utf-8'))
    print "\"%s\",\"%s\",\"%s\"" % (t, r, a)
