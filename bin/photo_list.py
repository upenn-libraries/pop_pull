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
key        = os.environ['POP_FLICKR_API_KEY']
secret     = os.environ['POP_FLICKR_API_SECRET']
page_size  = 500
start_page = 1
end_page   = 27
# end_page   = 24

flickr_api.set_keys(api_key = key, api_secret = secret)

user = flickr_api.Person.findByEmail('pennrare@gmail.com')

# photos = user.getPublicPhotos()
# photos = user.getPublicPhotos(per_page=page_size, page=start_page)
# pages = photos.info.pages
# write_info(photos, key)
for page in xrange(start_page,end_page+1):
    photos = user.getPublicPhotos(per_page=page_size,page=page)
    fname = 'data/photo_list_%03d.json' % page
    with open(fname, 'w+') as f:
        for photo in photos:
            f.write("%s\t%s\n" % (str(photo.id), photo.title.encode('utf-8')))
    print "Wrote %s" % fname
