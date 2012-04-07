#!/usr/bin/env python

import os
from Compost import Compost
from vcconfig import *

compost = Compost ()
outfilename = os.path.join (basedir, "video.raw")
if os.path.isfile (outfilename):
  os.remove (outfilename)

outfile = open (outfilename, "w")

count = 0
for chunk in compost._chunks:
  if os.path.isfile (chunk._filename):
    infile = open (chunk._filename, "r")
    outfile.write (infile.read ())
    infile.close ()
    count += 1

msg = "[gluechunks] combined {0} chunks to '{1}'".format (count, outfilename)
print msg
# TODO write log message

# vim: tw=0 ts=2 expandtab
# EOF
