import os
import json
# files = [ 'POP_0001.json.fixed' ]

files = [ 'POP_0001.json.fixed',
          'POP_0002.json.fixed',
          'POP_0003.json.fixed',
          'POP_0004.json.fixed',
          'POP_0005.json.fixed',
          'POP_0006.json.fixed',
          'POP_0007.json.fixed',
          'POP_0008.json.fixed',
          'POP_0009.json.fixed',
          'POP_0010.json.fixed',
          'POP_0011.json.fixed',
          'POP_0012.json.fixed',
          'POP_0013.json.fixed',
          'POP_0014.json.fixed',
          'POP_0015.json.fixed',
          'POP_0016.json.fixed',
          'POP_0017.json.fixed',
          'POP_0018.json.fixed',
          'POP_0019.json.fixed',
          'POP_0020.json.fixed',
          'POP_0021.json.fixed',
          'POP_0022.json.fixed',
          'POP_0023.json.fixed',
          'POP_0024.json.fixed' ]


tags = dict();

for file in files: 
    blerg = json.load(open(file))

    for item in blerg:
        for tag in item['photo']['tags']['tag']:
            raw = tag['raw']
            if (not raw in tags):
                tags[raw] = tag
            # try: 
            #     set.add(tag['raw'])
            # except: 
            #     print "Troubles with %s" % tag['id']

for raw in tags:
    t = str(raw.encode("utf-8"))
    a = str(tags[raw]['authorname'].encode("utf-8"))
    print "\"%s\",\"%s\"" % (t, a)
