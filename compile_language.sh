#!/bin/bash
here=`dirname "$(cd ${0%/*} && echo $PWD/${0##*/})"`
cd $here

rm -rf ./locale

for lng in ./po/*.po ; do
    #~ echo $lng
    lng_code=$(basename $lng)
    lng_code=${lng_code:8:5}
    #~ echo $lng_code
    mkdir -p ./locale/$lng_code/LC_MESSAGES
    msgfmt --check --check-accelerators=_ $lng -o ./locale/$lng_code/LC_MESSAGES/gSpeech.mo
done
