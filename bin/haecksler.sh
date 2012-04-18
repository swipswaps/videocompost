#!/bin/sh

# add videos in incoming to compost

user="kompost"
group="kompost"
basedir="/home/${user}"
indir="${basedir}/incoming"
logger="${basedir}/bin/VCLogger.py"
lockfile="${basedir}/run/haecksler.lock"

# exit if a lockfile is present
if [ -f ${lockfile} ]
then
  ${logger} "[haecksler]: lockfile present.  exiting."
  exit 0
fi
touch ${lockfile}

# work in basedir
cd ${basedir}

# add videos sorted by upload time
for video in $(ls -t ${indir})
do
  infile="${indir}/${video}"

  if [ -f ${infile} ]
  then
    # convert it to .raw format
    ${logger} "[haecksler]: importing ${video}"
    ./bin/video2raw.sh ${infile} infile.raw
    
    # cut it to pieces and add it to compost
    ./bin/cutvideo.py
    
    # remove video from incoming
    rm -f ${infile}
    ${logger} "[haecksler]: finished importing ${video}"
  fi
done

rm -f ${lockfile}

# vim: ts=2 tw=0 expandtab
# EOF
