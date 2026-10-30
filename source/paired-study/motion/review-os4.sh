#!/bin/sh
set -eu
mkdir -p /work/build/out /usr/share/fonts/ami-preview
cp /work/fonts/*.ttf /usr/share/fonts/ami-preview/
cd /work/checked
sha256sum -c SHA256SUMS
cp *.edj /work/build/out/
cc -Wall -Wextra /work/render.c -o /work/build/out/render $(pkg-config --cflags --libs ecore-evas edje)
for name in Ami-Ember Ami-Silver; do
 mkdir -p /work/build/out/$name-frames
 timeout 35 /work/build/out/render /work/build/out/$name-motion.edj /work/build/out/$name-wallpaper-motion.edj /work/build/out/$name-frames capture > /work/build/out/$name-capture.log 2>&1
 timeout 35 /work/build/out/render /work/build/out/$name-motion.edj /work/build/out/$name-wallpaper-motion.edj /work/build/out/$name-frames bench > /work/build/out/$name-bench.log 2>&1
done
cp /work/icons/provenance.json /work/build/out/os4-icons-provenance.json
cd /work/build/out
sha256sum *.edj */*.png render > SHA256SUMS
