7.7
==================================

h�cksler:
        GSTreamer(?) konvertiert alle video-files in normalisierte chunks (width*height, RGBA, maxlength)
        test-file: in raw RGBA


schaufler:
        f�gt neue chunks zum komposthaufen dazu
             komposthaufen w�chst




bots (python)
     manipulieren daten auf selbst-bestimmter ebene (frames, pixels, bytes)

     werden zyklisch aufgerufen

     kompost kann auch wieder schrumpfen

  kleines Framework?

  * composter.py
    ruft zyklisch die Bots aus der Liste (class BotList) auf.
  * cutvideo.py
    zerst�ckelt eingehende Videos zu Chunks und f�gt sie in die
    an zuf�lliger Stelle in die ChunkList ein.
  * gluechunks.py
    F�gt die Chunks aus der ChunkList zu einem (gro�en) File zusammen,
    das dann mit playraw.sh gespielt oder mit raw2video.sh wieder
    komprimiert werden kann.
  * addBotToList.py
    F�gt einen Bot zur BotList hinzu.

  * Klassen
    * Chunk(.py)
      Abstraktion f�r ein St�ck eines Videos.
    * ChunkList(.py)
      Liste von Chunks mit Methoden zum Management und zum Datenzugriff.
  * CompostAccess(.py)
    Eine Art Interface f�r Bots um auf Videodaten zugreifen zu k�nnen.
  * BotList(.py)
    Liste der Bots/Agents

Verzeichnisse und Files:

  home:       /home/vc/             :: basedir
  scripts:    /home/bc/bin/*        :: .sh and .py files
  chunks:     /home/vc/chunks/      :: .raw video chunks
  configs:    /home/vc/config/      :: configs for .py files
  incoming:   /home/vc/incoming/    :: incoming .ogv files
  raw video:  /home/vc/video.raw    :: result of gluechunks.py
  ogg video:  /home/vc/video.ogv    :: result of raw2video.sh
  new video:  /home/vc/infile.raw   :: result of video2raw.sh

