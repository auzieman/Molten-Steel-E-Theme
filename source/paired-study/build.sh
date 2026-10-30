#!/bin/sh
set -eu
mkdir -p /work/build/out /usr/share/fonts/ami-preview
cp /work/fonts/*.ttf /usr/share/fonts/ami-preview/
cc -Wall -Wextra /work/render.c -o /work/build/out/render $(pkg-config --cflags --libs ecore-evas edje)
for name in Ami-Ember Ami-Silver; do
 cd /work/themes/$name
 edje_cc -id . -fd . source.edc /work/build/out/$name.edj > /work/build/out/$name.log 2>&1
 timeout 30 /work/build/out/render /work/build/out/$name.edj /work/build/out/$name.png > /work/build/out/$name-render.log 2>&1
 cp ami-source.json /work/build/out/$name-source.json
done
cd /work/build/out
sha256sum *.edj *.png render > SHA256SUMS
