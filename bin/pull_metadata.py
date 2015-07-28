import json
import os
import sys
import time
import codecs
import re

from exceptions import Exception

import flickr_api
from flickr_api.api import flickr

error_file = 'errors.txt'

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
rtl = '\u200F'.decode( 'unicode-escape' )
ltr = '\u200E'.decode( 'unicode-escape' )
bidi_re = re.compile("[%s%s]+" % (rtl, ltr), re.UNICODE)


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
def get_info(photo, key):
    return flickr_api.api.call_api(
        method="flickr.photos.getInfo",
        api_key=key,
        photo_id=photo.id)

def write_info(photos, key):
    stats = photos.info
    tstamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print "Writing %03d photos; page %04d of %04d %22s" % (stats.perpage, stats.page, stats.pages, tstamp)

    fname = "POP_%04d.json" % stats.page
    f = codecs.open(fname, 'w+', 'utf-8')
    f.write('[')
    for photo in photos:
        try:
            s = json.dumps(get_info(photo,key)).decode('utf-8')
            s = bidi_re.sub('', s)
            f.write(s)
            f.write(',')
        except Exception as ex:
            print "Caught an exception: %s" % str(ex)
            err = open(error_file, 'a+')
            err.write("ERROR: %s - %s - %s\n" % (time.strftime('%Y-%m-%d %H:%M:%S'), str(photo.id).strip(), str(ex)))
            err.close()

    f.seek(-1, os.SEEK_END)
    f.truncate()
    f.write(']')
    f.close()
    # print "Wrote: %s %048s" % (fname, time.strftime('%Y-%m-%d %H:%M:%S'))

key        = os.environ['POP_FLICKR_KEY']
secret     = os.environ['POP_FLICKR_SECRET']
page_size  = 500
start_page = 3
end_page   = 24

flickr_api.set_keys(api_key = key, api_secret = secret)

user = flickr_api.Person.findByEmail('pennrare@gmail.com')

# photos = user.getPublicPhotos()
photos = user.getPublicPhotos(per_page=page_size, page=start_page)
pages = photos.info.pages
write_info(photos, key)
for page in xrange(start_page,end_page):
    print "Sleeping for 10 minutes before next download..."
    time.sleep(600)
    photos = user.getPublicPhotos(per_page=page_size,page=(page+1))
    write_info(photos,key)
