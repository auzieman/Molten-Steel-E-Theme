# Icon source study

The user selected a nearly transparent shelf with colorful Amiga drawer icons,
then pointed to the OS4 icon catalogue. The project-authored SVG drawers in this
directory are an **unused draft**, not the selected icon direction.

Use authentic artwork from [Icons for AmigaOS](https://www.amiga-look.org/artwork/icons-amigaos)
for the local shelf sample. `import-os4.py` reads the source FACE/ARGB chunks and
exports original normal/selected pixels to PNG, preserving alpha and dimensions.
No recoloring, upscaling or newly drawn replacement is involved in the export.

The original pack is by IconDesigner and credits Martin Merz and Frank Ruthe for
some symbols. The source page lists freeware; exported icons remain third-party
artwork. Keep them in private ignored build storage with the original readme,
per-input hashes and explicit filename mappings. No redistribution permission or
complete freedesktop icon-theme coverage is established by this sample.

The six shelf fixtures demonstrate pack artwork. Their Linux fixture names do
not mean that Amiga app-specific symbols have become installed Linux defaults.
A proper mapped theme needs selected semantics and complete fallback coverage.

Reviewed archive: `icons-for-amigaos.lha` (30-03-2015 source version).
SHA256 `6063efc7fc4d4289f98dffba496d767e2d69ea57ca00b3a123c5917eb354b94c`.
The attached LHA uses a header variant not accepted by the local bsdtar; the
isolated lhafile reader extracted it into private reference storage. The importer
retains dimensions and both normal/selected source states without alteration.

## Companion theme candidate

`import-os4.py --desktop-theme SOURCE NEW_OUTPUT` exports eight explicit freedesktop MIME mappings, an index.theme and hicolor fallback, preserving original normal/selected pixels. Selected images remain review assets, not automatic desktop selection states. Partial file-type coverage only; application and drawer mappings remain pending. Candidate and preview are under build/out/ami/test-candidates. No icon setting changed.

## Drawer-first Enlightenment build

`build-companion.py SOURCE NEW_OUTPUT` is the drawer-first companion generator.
It maps 21 freedesktop names across Places, Devices and Applications, with
hicolor fallback. Home, documents, downloads, music, videos and open-folder names
share the original plain drawer for now; pictures/apps and drives have selected
pack artwork. These aliases are explicit in provenance.json. Seven original
source icons supply the set. Original normal/selected RGBA frames remain under
original-states; icon lookup uses normal images, padded square and downsampled
without enlargement. No new OS4-native package is produced.

The standalone build-lab.sh and validate.c fixture verify PNG hashes, resolve
every name using native Efreet at 16/32/64, decode images with Evas and export a
native contact sheet. The dedicated ami-drawers-build BKC lane uses the existing
hash-pinned compiler image with 2 CPUs and 2 GiB. Installed files exist only in
the disposable build container. Native lookup/render acceptance is separate
from live Enlightenment shelf/file-manager acceptance.

Private third-party artwork stays in ignored build storage. Code is retained
here; the source pack's original notice accompanies the generated package.
