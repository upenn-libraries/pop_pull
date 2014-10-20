import json
import os
import sys
import time

from exceptions import Exception

import flickr_api
from flickr_api.api import flickr

error_file = 'errors.txt'

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
    f = open(fname, 'w+')
    f.write('[')
    for photo in photos:
        try:
            f.write(json.dumps(get_info(photo,key)))
            f.write(',')
        except Exception as ex:
            print "Caught an exception: %s" % str(ex)
            err = open(error_file, 'a+')
            err.write("%s - %s" % (str(photo.id), str(ex)))
            err.close()

    f.seek(-1, os.SEEK_END)
    f.truncate()
    f.write(']')
    f.close()
    # print "Wrote: %s %048s" % (fname, time.strftime('%Y-%m-%d %H:%M:%S'))

key        = os.environ['POP_FLICKR_KEY']
secret     = os.environ['POP_FLICKR_SECRET']
page_size  = 500
start_page = 6
end_page   = 6

flickr_api.set_keys(api_key = key, api_secret = secret)

user = flickr_api.Person.findByEmail('pennrare@gmail.com')

# photos = user.getPublicPhotos()
photos = user.getPublicPhotos(per_page=page_size, page=start_page)
pages = photos.info.pages
write_info(photos, key)
# for page in xrange(start_page,end_page):
#     photos = user.getPublicPhotos(per_page=page_size,page=(page+1))
#     write_info(photos,key)
