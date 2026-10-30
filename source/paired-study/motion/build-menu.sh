#!/bin/sh
set -eu
mkdir -p /work/build/out /usr/share/fonts/ami-preview
cp /work/fonts/*.ttf /usr/share/fonts/ami-preview/
cc -Wall -Wextra /work/render-menu.c -o /work/build/out/render-menu $(pkg-config --cflags --libs ecore-evas edje)
for name in Ami-Ember Ami-Silver; do
 cd /work/themes/$name
 edje_cc -id . -fd . source.edc /work/build/out/$name-menu.edj > /work/build/out/$name-build.log 2>&1
 timeout 10 /work/build/out/render-menu /work/build/out/$name-menu.edj /work/build/out/$name-menu.png > /work/build/out/$name-menu.log 2>&1
 cp ami-menu-icon-slots.json /work/build/out/$name-menu-icon-slots.json
done
cp /work/themes/motion-source.json /work/build/out/
cd /work/build/out
sha256sum *.edj *.png *-menu-icon-slots.json motion-source.json render-menu > SHA256SUMS
