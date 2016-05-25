#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import re
import sys
import time
import sys
import codecs

from exceptions import Exception

import flickr_api
from flickr_api.api import flickr

error_file = 'errors.txt'

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
rtl = '\u200F'.decode( 'unicode-escape' )
ltr = '\u200E'.decode( 'unicode-escape' )
bidi_re = re.compile("[%s%s]+" % (rtl, ltr), re.UNICODE)

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def usage():
    print "Usage: %s IDFILE" % (os.path.dirname(__file__), )


# flickr.photos.getInfo
#
# api_key (Required)
#   Your API application key. See here for more details.
#
# photo_id (Required)
#   The id of the photo to get information for.
#
# secret (Optional)
#   The secret for the photo. If the correct secret is passed then permissions
#   checking is skipped. This enables the 'sharing' of individual photos by
#   passing around the id and secret.
#
def get_comments(photo_id, key):
    return flickr_api.api.call_api(
        method="flickr.photos.comments.getList",
        api_key=key,
        photo_id=photo_id)

def write_info(ids, key, outfile):
    f = codecs.open(outfile, 'w+', 'utf-8')
    f.write('[')
    for photo_id in ids:
        try:
            s = json.dumps(get_comments(photo_id,key))
            s = bidi_re.sub('', s)
            f.write(s)
            f.write(',')
        except Exception as ex:
            print "Caught an exception: %s" % str(ex)
            err = open(error_file, 'a+')
            err.write("ERROR: %s - %s - %s\n" % (time.strftime('%Y-%m-%d %H:%M:%S'), str(photo_id).strip(), str(ex)))
            err.close()

    f.seek(-1, os.SEEK_END)
    f.truncate()
    f.write(']')
    f.close()

key        = os.environ['POP_FLICKR_KEY']
secret     = os.environ['POP_FLICKR_SECRET']

flickr_api.set_keys(api_key = key, api_secret = secret)

# user = flickr_api.Person.findByEmail('pennrare@gmail.com')

try:
    idfile = sys.argv[1]
except:
    print "Please provide an IDFILE"
    usage()
    sys.exit(1)


ids = [ phid.strip() for phid in open(idfile) ]

total = 0

for i in xrange(len(ids)/500 + 1):
    outfile = 'COMMENTS_%04d.json' % (i, )
    chunk = ids[i*500:(i+1)*500]
    write_info(chunk, key, outfile)
    chunk_len = len(chunk)
    total += chunk_len
    print "Wrote: %s for %3d photos (total: %5d)" % (outfile, chunk_len, total)
    print "Sleeping 10 minutes before next download"
    time.sleep(600)
