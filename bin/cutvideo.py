#!/usr/bin/env python

"""
  takes the file 'infile.raw' (expected in /basedir)
  and cuts it into chunks of a defined size, adding the chunks
  to compost and storing them in /basedir/compost/.
"""

import hashlib
import time
import sys
import os
from Compost import Compost
from vcconfig import *
from VCLogger import writelog

if os.path.isfile (infilename):
  infile = open (infilename, "r")
else:
  writelog ("[cutvideo]: {0} not found".format (infilename))
  print "[cutvideo]: {0} not found".format (infilename)
  sys.exit (1)

# pixels_per_frame * bytes_per_pixel * frames
# will be changed to aprox. 2GB
chunksize = 320 * 240 * 4 * 68
chunk = True
chunknum = 0

compost = Compost ()

while True:
  infile.seek (chunksize * chunknum)
  chunk = infile.read (chunksize)
  if not chunk:
    break
  hash = hashlib.md5 (str (time.time ()))
  chunkfilename = os.path.join (compostdir, "%s.raw" % hash.hexdigest ())
  chunkfile = open (chunkfilename, "w")
  chunkfile.write (chunk)
  chunkfile.close ()
  compost.addChunk (chunkfilename)
  chunknum += 1

os.remove (infilename)
compost.save ()
writelog ("[cutvideo]: successfully added {0} chunks from {1} to compost.".format (chunknum, infilename))

# vim: tw=0 ts=2 expandtab
# EOF
