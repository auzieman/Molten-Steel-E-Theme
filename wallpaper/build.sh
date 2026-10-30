#!/bin/sh
# Run in the existing constrained BKC native compiler job, not on the desktop.
set -eu
cd "$(dirname "$0")"
mkdir -p ../build
edje_cc -id . wallpaper.edc ../build/wallpaper-still.edj
edje_cc -DANIMATED -id . wallpaper.edc ../build/wallpaper-animated.edj
