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
key               = os.environ['FLICKR_API_KEY']
secret            = os.environ['FLICKR_API_SECRET']
flickr_user_email = 'pennrare@gmail.com'
page_size         = 500     # images/request (i.e., page)
start_page        = 1
end_page          = 27      # (<NUM_PHOTOS>/page_size) + 1
# How long to sleep to avoid exceeding Flickr's 3600 calls/hour limit
sleep_seconds     = 600

flickr_api.set_keys(api_key = key, api_secret = secret)

user = flickr_api.Person.findByEmail(flickr_user_email)


# photos = user.getPublicPhotos()
# photos = user.getPublicPhotos(per_page=page_size, page=start_page)
# pages = photos.info.pages
for page in xrange(start_page,end_page+1):
    photos = user.getPublicPhotos(per_page=page_size,page=page)
    for photo in photos:
      outname = photo.title + ".jpg"
      photo.save(outname)
      print "Wrote %s" % outname

    print "Sleeping: %d seconds" % sleep_seconds
    time.sleep(sleep_seconds)