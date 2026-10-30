# Molten Steel — Enlightenment theme preparation

Independent repository extracted from BlackKnight-E-Theme's working tree on
2026-10-30. Native wallpaper source is self-contained in `wallpaper/`, with
original generated raster, effect layers and provenance. In the existing BKC
compiler job, `sh wallpaper/build.sh` builds still/animated EDJs; no desktop
setting is selected. This extracted recipe has not yet been rebuilt.

The desktop adaptation tools are retained in `source/paired-study/`. They still
operate on the paired Fire/Molten Steel study; these are migration inputs, not a
finished single-theme build interface. They require private Ice/reference/icon
inputs, which are deliberately absent. The repository contains no full derived
theme EDJ, OS4 icon payloads or DarkOs/SilverBlack bitmap archive.

Original code: GPL-3.0-only. Original wallpaper/effect artwork: CC-BY-SA-4.0,
credit Auzieman / AuzieTek; see LICENSES and assets/provenance.json. Third-party
inputs retain their own rights. See NOTICE.md and docs/history for boundaries.

Historical native run: `0bd8ae7b-131b-4dbb-ab9f-e9f23751218f`; existing pixel
motion/pause/resume checks passed. No new compile, live desktop, GPU or HiDPI
acceptance follows from this extraction.

Next: give the desktop generator a single-theme interface, resolve upstream
permissions and validate through BKC before packaging full theme binaries.
No GitHub remote or public release has been created.
