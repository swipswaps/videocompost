"""
this bot draws random squares of the same color somewhere in the video.
color is picked from one of the pixels
"""

"""
python classes used by this bot
"""
import time
import os.path
import pickle
import signal
import random

"""
custom classes to access video compost data
"""
from Compost import Compost
from VCLogger import writelog
from vcconfig import *

"""
Adapt config to your needs.  Use loadConfig () and saveConfig ()
to store data across runs.
"""
config = {}
config["myname"] = __name__
config["chunk"] = 0

"""
create an instance of Compost to access video data
"""
compost = Compost ()

class BotError (Exception):
  """
  custom exception
  """
  def __init__ (self, msg):
    self.msg = msg

def signalhandler (signum, frame):
  """
  handler for signals
  """
  raise BotError ("received signal {0}".format (signum))

def loadConfig ():
  """
  load config from file if available
  """
  global config
  filename = os.path.join (configdir, "%s.config" % __name__)
  if os.path.isfile (filename):
    infile = open (filename, "r")
    config = pickle.load (infile)
    infile.close ()

def saveConfig ():
  """
  store config to file
  """
  global config
  filename = os.path.join (configdir, "%s.config" % __name__)
  outfile = open (filename, "w")
  pickle.dump (config, outfile)
  outfile.close ()

def runMe ():
  """
  main method called by composter.py
  """
  signal.signal (signal.SIGHUP, signalhandler)
  signal.signal (signal.SIGINT, signalhandler)

  try:
    try:
      loadConfig ()
    except:
      pass
    width = 320
    height = 240
    bytes_per_pixel = 4
    frame_size = width * height
    min_square_width = 2
    max_square_width = 16

    writelog ("[{0}]: started at chunk {1}".format (__name__, config["chunk"]))

    for chunk in range (0, len (compost._chunks)):
      if chunk < config["chunk"]:
        chunk = config["chunk"]
      compost.mapChunk (chunk)
      map_length = len (compost._map)
      num_frames = map_length / (frame_size * bytes_per_pixel)
      random.seed ()

      # determine how many frames will be affected
      if num_frames <= 5:
        affected_frames = num_frames
      else:
        if num_frames <= 50:
          max_affected_frames = num_frames
        else:
          max_affected_frames = 50
        affected_frames = random.randint (5, max_affected_frames)

      # width of a square
      square_width = random.randint (min_square_width, max_square_width)

      # pixel where square starts
      frame_pixel = random.randint (0, ((frame_size - width * square_width)) - square_width)

      # first affected frame
      start_frame = random.randint (0, num_frames - affected_frames)

      # first byte of square
      start_byte = (frame_pixel + frame_size * start_frame) * bytes_per_pixel

      # get a random pixel color from somewhere in the frame
      color_index = (random.randint (0, map_length - bytes_per_pixel) / bytes_per_pixel) * bytes_per_pixel
      pixel_color = compost._map [color_index:color_index + bytes_per_pixel]
      compost.addEntropy (start_byte)

      for f in range (0, affected_frames):
        frameoffset = f * frame_size * bytes_per_pixel
        for h in range (0, square_width):
          lineoffset = start_byte + frameoffset + h * width * bytes_per_pixel
          for w in range (0, square_width):
            start = lineoffset + w * bytes_per_pixel
            try:
              compost._map[start:start + bytes_per_pixel] = pixel_color
            except IndexError:
              print 'Exception: square_width={0}, affected_frames={1}, start_byte={2}, start_frame={3}, map_length={4}, frameoffset={5}, lineoffset={6}'.format (
                square_width, affected_frames, start_byte, start_frame, map_length, frameoffset, lineoffset)

    config["chunk"] = 0
    saveConfig ()

  except BotError as e:
    config["chunk"] = chunk
    saveConfig ()
    writelog ('[{0}: stopped by signal.  saving chunk={1} for next run'.format (__name__, chunk))
    return 0

  """
  return a number != 0 to indicate an error to composter.py
  """
  return 0
  
if __name__ == "__main__":
  pass

# vim: tw=0 ts=2 expandtab
# EOF
