# Ami restrained motion study

Original Ember/Silver wallpaper artwork plus a native Edje motion layer on the
existing Ami border candidates. Keeps raster chrome, titles, gadgets and input
rectangles stationary. Animation uses approximately 14-second out-and-back motion,
with a long quiet interval and twelve discrete material updates. No video decoder, fluid solver, blur pass or particle engine is involved.

Fire (Ami-Ember) adds three faint curved heat traces and three ember specks. Molten Steel (Ami-Silver) adds a
broad soft reflection ribbon. These are simple code-native SVG overlays, not
regenerated replacements for the reference chrome. Wallpapers have two moving
layers confined to the lower edge/lower right; the quiet icon area is stationary.
This first study suggests moving fire/liquid through drifting highlights; it is
not a simulation or a frame-by-frame morph of the generated artwork.

The border loop starts on focus and stops on loss of focus. Both border and
wallpaper accept `ami,pause` and `ami,resume` from a host source. Pausing freezes
at the current phase. Still wallpaper EDJs contain no overlay animation programs.
Inactive borders remain at their low-intensity default material state.

## Build and evidence

Run `prepare.py BASELINE_VARIANT_DIRECTORY NEW_OUTPUT_DIRECTORY` with the
previous checked `build/out/ami/variants3` directory. Build with the dedicated
`ami-motion-build` BKC pipeline, established compiler image and 2 CPU/2 GiB
limits. `build.sh` compiles two full theme candidates and animated/still native
wallpapers. `render.c` samples actual E border and wallpaper groups for a full
14-second cycle; it also checks pause/resume and measures animated/paused
buffer rendering at 1920×1080. Those CPU figures are software-render fixture
results, not laptop compositor/GPU performance claims.

Native capture uses 6 fps for review files; Edje transitions use a 30 fps
animator setting in this harness. Desktop animator policy remains desktop-owned.
No desktop settings are changed or candidates installed by this study.

## Artwork provenance

The built-in image-generation tool produced the two new PNGs on 2026-10-26.
Prompts are retained in `prompts.json`. Original outputs remain in the local
Codex generated_images store; project copies are in `assets/`. The generator
writes small SVG effect overlays beside them and rasterizes those once with
CairoSVG. Edje loads the resulting small PNGs during motion. Generated wallpaper/effect assets
follow the project's original-artwork license; the full theme archives continue
to contain third-party reference assets covered by ../README.md, and remain
private experiments pending the existing permissions boundary.

Rollback removes this directory and its ignored build outputs. It does not
require changing a saved desktop theme or background.

The user selected **Fire and Molten Steel** as the visual direction during the
study. Existing internal Ami-Ember/Ami-Silver filenames remain traceable.

Preparation requires Pillow/CairoSVG in an isolated tools environment.

## Checked first study — 2026-10-26

Final BKC run: `ee53de7f-9c9b-40ac-bd10-6e5b7701a634`.
Source bundle SHA256:
`3fa77a1f581277b2e0abf45431474348b6019306e69380e22a374041629b1dc2`.
Both theme candidates and four animated/still wallpaper EDJs compiled. Returned
artifact hashes pass. Native pixel checks confirm motion, exact frozen pixels
while paused and changed pixels after resuming through the quiet interval.

- [Fire native motion clip](../../../docs/images/fire-motion-20261026.mp4)
- [Molten Steel native motion clip](../../../docs/images/molten-steel-motion-20261026.mp4)
- [Measured evidence](../../../docs/images/ami-motion-review-20261026.json)

The clips rotate the captured cycle to begin shortly before the moving phase.
They contain actual native buffer renders, not generated animation mockups.
Capture is 960×540, while the separate software cost sample is 1920×1080.

The initial continuous pass used 132–133% of one core during animation. Final
stepped motion used 33.35% (Fire) / 33.92% (Molten Steel) over the active
four-second interval; paused samples used 0.18% / 0.19%. Rasterizing SVG effects
once did not materially improve those numbers, although it removes runtime SVG
resizing from the design. Long quiet intervals reduce average work, but a full
cycle average and GPU/compositor cost have not been measured. This is a visual
prototype, not accepted low-cost desktop animation. Do not install by default.

The first vector flame silhouettes looked too stylized; the final pass uses
faint curved heat traces over the generated raster fire artwork. No true liquid
or flame deformation is claimed. A smoother/higher-detail version needs native
GPU/live desktop evidence before expanding the effect.

Pause/resume tests are scoped to the default border and wallpaper groups. Full
widget coverage, shelf animation, inherited border variants and desktop
interaction/scale acceptance remain future slices. Container system-bus/UPower
diagnostics occurred during successful offscreen renders; still wallpaper builds
warn about the unused motion texture, as expected when animation is excluded.

## Title-bar and transparent-shelf refinement

The user requested visible fire in the title bar, a ripple in Molten Steel,
and a nearly transparent shelf with colorful Amiga drawers. Dedicated 512×32
code-native sprites now change flame shape and produce paired light/dark silver
ripples. The centre stays clear under live title text. The original bounded
focus-gated animation programs remain; native action programs are asserted
unchanged by the generator. Wallpaper artwork and effects remain unchanged.

Title-bar build `f0fe851e-1dfe-40e4-8c2a-05e78d73ef82` compiled both candidates.
The transparent-shelf candidate build is
`7bbd0a36-6659-4361-a027-56e8061c0624`; source shelf alpha is 32/255 with a
passive thin warm/cool rim. Original shelf action/signal/orientation programs
remain intact. Its first icon fixtures were unused draft drawings; those are
superseded by the authentic OS4 sample in ../icons/README.md.

The OS4 review pipeline reuses the verified shelf EDJs and renders original
IconDesigner source pixels as launcher fixtures. Those visible fixtures prove
composition only: they are not an installed Linux icon theme or functional
launcher test. Private source readme, normal/selected images and semantic
mappings are retained in ignored build storage. Do not redistribute original
freeware icon artwork under the project's original-artwork license.

Authentic OS4 shelf review run:
`d0353c45-6853-4a67-9b21-1c486e7cb8a6`. Reuses the verified EDJs byte-for-byte
and renders the original OS4 icons externally. Updated comparison clips:
[Fire](../../../docs/images/fire-os4-shelf-20261026.mp4) and
[Molten Steel](../../../docs/images/molten-steel-os4-shelf-20261026.mp4).
Local test handoff is `build/out/ami/test-candidates/20261026` with six EDJs,
original OS4 normal/selected PNG sample pixels, provenance and SHA256SUMS.
The sibling tar.gz is a private local testing bundle, not a release artifact.
Neither the themes nor the icons have been installed or selected.


## Native menu/start extension

`prepare-menus.py BASELINE ICONS NEW_OUTPUT --drawer-theme DRAWER_THEME` binds
the existing metallic panel/rail/pressed-button rasters to real E menu groups,
embeds the private OS4 drawer payloads and replaces the start arrow with a drawer.
Menu/start program bodies and menu swallow names are asserted identical to the
baseline. Silver labels use dark ink without shadow/glow on the light panel.

`build-menu.sh` compiles the two full themes and uses `render-menu.c` for still
native menu/shelf/start fixtures. Stage it as `build/prototype/build.sh` in the
existing BKC source layout. This bounded lane uses one CPU and 2 GiB and performs
no motion encoding, wallpaper rebuild, installation or desktop selection.
The fixture uses real embedded `system-file-manager` and `configure` aliases;
`preferences-applications` is absent from the inherited compiled collection.

The fixtures demonstrate group loads and appearance, including selected and
disabled labels and submenu arrows. They do not test live menu clicks or desktop
scale/HiDPI. Folder rows intentionally share generic drawer aliases; dedicated
category icon artwork and remaining inherited widgets are still follow-ups.
The inherited reference art remains private review material under its original
notices, as described in ../README.md and ../icons/README.md.


## Strong wallpaper and liquid menu review

`prepare-material-pass.py MENU_BASELINE NEW_OUTPUT` retains the checked menu
contracts and icons. It binds the original Silver wallpaper raster to menu
edges, with a passive pale centre for dark labels. Fire uses eight changing,
soft-edged native SVG flame silhouettes. Silver uses paired dark/light curved
ripple bands in the lower region. The upper icon area stays stationary. These
are authored motion layers, not a flame/fluid simulation.

`build-material.sh` builds the selected menu and both animated wallpapers;
when accepted-menu files are staged it reuses those exact verified bytes.
`render-wallpaper.c` captures short native sequences and pause/resume samples.
Final native run: 0bd8ae7b-131b-4dbb-ab9f-e9f23751218f. All 45 returned hashes
pass. Pixel movement, exact pause freeze and resume pass for both wallpapers.
Wallpaper-only 960x540 software samples were 6.44%/2.17% of one core active,
about 0.2% paused; no live desktop/HiDPI/GPU acceptance is implied.

Installed selector entries include Fire/Molten-Steel-Wallpaper-Strong-Motion-
20261026, plus Molten-Steel-Theme-Liquid-Menu-20261026. Earlier candidates remain.
No selection was changed. Preview/evidence: [native review](../../../docs/images/ami-strong-material-review-20261026.json)
and the corresponding strong-wallpaper/menu PNGs.
