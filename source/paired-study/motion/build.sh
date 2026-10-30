#!/bin/sh
set -eu
mkdir -p /work/build/out /usr/share/fonts/ami-preview
cp /work/fonts/*.ttf /usr/share/fonts/ami-preview/
cc -Wall -Wextra /work/render.c -o /work/build/out/render $(pkg-config --cflags --libs ecore-evas edje)
for name in Ami-Ember Ami-Silver; do
 cd /work/themes/$name
 edje_cc -id . -fd . source.edc /work/build/out/$name-motion.edj > /work/build/out/$name-build.log 2>&1
 cd /work/themes/$name-wallpaper
 edje_cc -DANIMATED -id . wallpaper.edc /work/build/out/$name-wallpaper-motion.edj > /work/build/out/$name-wallpaper-build.log 2>&1
 edje_cc -id . wallpaper.edc /work/build/out/$name-wallpaper-still.edj >> /work/build/out/$name-wallpaper-build.log 2>&1
 mkdir -p /work/build/out/$name-frames
 timeout 35 /work/build/out/render /work/build/out/$name-motion.edj /work/build/out/$name-wallpaper-motion.edj /work/build/out/$name-frames capture > /work/build/out/$name-capture.log 2>&1
 timeout 35 /work/build/out/render /work/build/out/$name-motion.edj /work/build/out/$name-wallpaper-motion.edj /work/build/out/$name-frames bench > /work/build/out/$name-bench.log 2>&1
done
cp /work/themes/motion-source.json /work/build/out/
cd /work/build/out
sha256sum *.edj */*.png render > SHA256SUMS
