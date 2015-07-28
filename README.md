pop_pull
========

This is a rather sloppy collection of Python and Ruby scripts created
to download and sort image metadata from the POP Flickr feed. To sort
out various Unicode issues I tried some things both in Python (which
I'm so-so familiar with) and Ruby (which I know well).  This is
especially true for the scripts that convert the downloaded Flickr
metadata into other formats (like `csv_tagify.py/rb` and
`photo_csv.py/rb`).  C'est la vie.

If you want to download Flickr photo IDs and image metadata, see:
`bin/pull_metadata.py`.

If you want to download Flickr photo metadata using an existing list
of IDs, see: `bin/pull_by_ids.py`.

If you want to download comments from Flickr, see
`bin/comments_by_id.py`.  As the name suggests, you need a list of
Flickr photo IDs to run this script.
