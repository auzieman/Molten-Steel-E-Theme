# Ami metallic study

Native Enlightenment candidates inspired by the user-selected
[DarkOs](https://www.amiga-look.org/artwork/darkos-theme) and
[SilverBlack](https://www.amiga-look.org/artwork/silverblack) references.

Ami-Ember keeps DarkOs's rounded silver rail, amber focused gadgets and dark
ribbed panel. Ami-Silver keeps SilverBlack's inset title tab, charcoal rail,
rectangular gadgets and pale silver buttons. These are raster adaptations of
the downloaded originals, not newly generated or original artwork.

## Scope

The verified Ice baseline supplies desktop contracts and unselected widgets.
This slice adapts the default border, horizontal/vertical shelf and standard
Elementary button artwork. The preview panel is a texture fixture, not proof
that all applications or menus have matching backgrounds. Programs, event
rectangles, resize zones and content/icon swallows retain baseline behavior.
SilverBlack's passive title tab follows existing focus transitions.

The first tab is fixed at 220 pixels; very long titles and narrow windows need
further layout review. Controls retain E's ordering for this first slice.
The source artwork remains at its original small pixel sizes; HiDPI acceptance
is pending. The shelf is an adaptation of window chrome, not an original
Amiga shelf asset. No wallpaper, icon pack or media-player skin is included.

## Reproduce

Use the unchanged, previously rebuilt Ice source retained under
`build/out/frosty/ice-source`; see ../frosted-glass/desktop/README.md for its
baseline run, hash, font provenance and inherited notices.

Download and extract the two reference LHA archives into private build storage:

- https://www.amiga-look.org/sites/default/files/77/darkos_0.lha
- https://www.amiga-look.org/sites/default/files/75/SilverBlack.lha

With Pillow available, run:

```sh
python prepare.py ../../build/out/frosty/ice-source ../../build/out/ami/reference NEW_OUTPUT
```

Run from this directory. The reference tree contains `darkos/DarkOS/Bitmaps`
and `silverblack/Bitmaps`. `ilbm.py` decodes planar indexed/24-bit ILBM,
ByteRun1, one-bit masks and eight alpha bitplanes. The generator records every
reference input hash and generated source hash in each `ami-source.json`.

Stage through the dedicated `ami-theme-build` BKC pipeline using `build.sh`,
`render.c` and the established hash-pinned compiler image. Build runs remotely
with two CPUs and 2 GiB. Render images are native buffer output; compilation
and those fixtures do not establish live desktop acceptance.

## Rights and rollback

Reference artwork retains its authors' rights. DarkOs is listed as freeware;
free download does not establish permission to relicense or redistribute an
adapted package. Keep reference and derived graphics in ignored local build
storage until permissions are resolved. No reference bitmaps are committed
here. Project-authored generator/decoder/renderer follow the project code
license; inherited Ice assets retain upstream notices.

No desktop setting is changed. Remove the new build storage to roll back local
candidates. A later live trial uses the existing independently timed restoration
workflow, after the candidates have passed visual review.

Reference archive SHA256:

```text
cda4959346a8d9d6703d3a326811c5788203d82d7fbe280f4ecfdf08107e8c9c  darkos_0.lha
599303746dfdb056ce6086f612017e1520a647eb03052cc4e1c4f78e2b3d70e2  SilverBlack.lha
```

The initial run `a832ed36-65f1-439b-b49a-00ef86efd14e` built Ember;
Silver compilation exposed an added passive target leaking into the independent
pixel-border group. Scope the target insertion to the default border group.
Native visual review also found missing external gadget alpha maps and stretched
button bevels; the corrected generator preserves masks and nine-slices the rim.
Those are introduced adaptation defects, not Ice baseline defects.

Corrected run `23b1aca2-fd92-4bf0-9270-190c30103f7b` compiled both full
archives; all five collected SHA256 entries passed. Offscreen native renders
show focused 820-pixel and inactive 390-pixel borders, horizontal/vertical
shelves and standard button group instances. The dark panel preserves the
reference ribbing, gadget masks and nine-sliced metallic button rims.
Silver's tab initially used the whole-window centre, while the title uses the
area between E's controls. The final generator anchors the passive tab's X
coordinates to `e.text.title` instead, preserving vertical rail geometry.

Final review build: `9dfe0df7-23c0-4843-aa75-79670851d5f8`.
Both archives compiled with empty compiler logs; native buffer renders were
visually inspected after the title-tab alignment correction. Container render
logs include expected missing system-bus/UPower diagnostics; both renders exit
successfully. Full desktop interaction acceptance remains pending.

- [Ember native preview](../../docs/images/ami-ember-native-20261026.png)
- [Silver native preview](../../docs/images/ami-silver-native-20261026.png)

Private EDJs and per-file source manifests are retained under
`build/out/ami/results/9dfe0df7-23c0-4843-aa75-79670851d5f8`.
Screenshots retain the reference-artwork rights and are local review evidence.

## Fire and Molten Steel motion study

The next slice adds original matching wallpapers and restrained material motion:
[motion sources, artwork and evidence](motion/README.md). These remain private
native candidates; the wallpaper artwork is original to this project.
