#!/bin/sh
set -eu
mkdir -p /work/build/out /usr/share/fonts/ami-preview
cp /work/fonts/*.ttf /usr/share/fonts/ami-preview/
cc -Wall -Wextra /work/render-menu.c -o /work/build/out/render-menu $(pkg-config --cflags --libs ecore-evas edje)
cc -Wall -Wextra /work/render-wallpaper.c -o /work/build/out/render-wallpaper $(pkg-config --cflags --libs ecore-evas edje)
if [ -f /work/accepted-menu.edj ]; then
 cp /work/accepted-menu.edj /work/build/out/Molten-Steel-Liquid-Menu.edj
 cp /work/accepted-menu.png /work/build/out/molten-menu.png
 cp /work/accepted-menu.log /work/build/out/menu-render.log
else
 cd /work/themes/Ami-Silver
 edje_cc -id . -fd . source.edc /work/build/out/Molten-Steel-Liquid-Menu.edj > /work/build/out/menu-build.log 2>&1
 timeout 10 /work/build/out/render-menu /work/build/out/Molten-Steel-Liquid-Menu.edj /work/build/out/molten-menu.png > /work/build/out/menu-render.log 2>&1
fi
for name in Ami-Ember Ami-Silver; do
 cd /work/themes/$name-wallpaper
 edje_cc -DANIMATED -id . wallpaper.edc /work/build/out/$name-wallpaper-strong.edj > /work/build/out/$name-wallpaper-build.log 2>&1
 mkdir -p /work/build/out/$name-frames
 timeout 20 /work/build/out/render-wallpaper /work/build/out/$name-wallpaper-strong.edj /work/build/out/$name-frames > /work/build/out/$name-wallpaper-render.log 2>&1
done
cp /work/themes/motion-source.json /work/build/out/
cd /work/build/out
sha256sum *.edj *.png *-frames/*.png render-menu render-wallpaper motion-source.json > SHA256SUMS
