# CLAUDE.md

Notes for working on this repo with Claude. Read this before changing any model.

## What this is

A 3D-printed replica of the Apple Macintosh mouse (M0100) that holds the electronics of a Logitech
M185 wireless mouse and one AA cell. It was made to go with a replica of Apple's "Snow White" concept
computer. Published at <https://github.com/wottle/mac-mouse-logitech-m185>.

Sister project: the Lisa version at <https://github.com/wottle/lisa-mouse-logitech-m185> (local folder
`LisaMouseLogitechM185`). The M185 mounting here was taken from the Lisa base, and what was learned
here (screw strikers, hinge tightening, front screws with rear hooks, parallel sides, deep logo
recess) is being carried back to the Lisa mouse. That repo has its own `CLAUDE.md`.

## Layout

| Path | What |
|------|------|
| `models/common/` | The STLs people print either way: everything but the upper shell. All except the three carried-over parts are generated. |
| `models/fdm/`, `models/resin/` | `upper_shell.stl`: FDM with straightened, planed sides; resin with the original's lean (`build_upper(fdm=False)`, `smooth_upper(fdm=False)`). |
| `scripts/` | The whole build (see below). |
| `source/lisa/base.stl` | Base from the Lisa conversion; source of the M185 mounting. |
| `source/m0100/` | Original M0100 model (upper shell, lower shell, button). **Git-ignored**: its licence and creator are not confirmed. Needed locally to rebuild. Never commit it. |
| `build/` | Generated intermediates (git-ignored). |
| `docs/ASSEMBLY.md`, `docs/PRINTING.md`, `README.md` | User docs. Keep in step with the models. |
| `print/MacMouse_BambuStudio_A1.3mf` | Mike's slicer project: every part oriented, supports only where needed. He maintains it. It includes his own Apple logo plate as an easter egg; leave that in. |
| `images/photos/` | Photos of the printed mouse. `images/plates/` are slicer plate screenshots. |

`on_off_button.stl`, `battery_cover_1.stl`, `battery_cover_2.stl` are carried over from the Lisa
project unchanged and are not built by the scripts.

## Building

```
pip install -r scripts/requirements.txt
python3 scripts/build_models.py
```

This regenerates `models/{common,fdm,resin}/*.stl` and `images/preview.png`, then runs the fit checks for each upper
shell with the common parts. Pipeline:

| Script | Does |
|--------|------|
| `geo.py` | Frames, loaders, CSG helpers. `tm_mac()` loads an M0100 part into the final frame and (unless `straight=False`) straightens the upper shell's sides. |
| `lisa_solid.py` | Rebuilds the messy Lisa base layer by layer into one clean solid (`build/lisa_base_solid.stl`). |
| `build_lower.py` | New lower shell: M0100 outline with the Lisa/M185 interior. |
| `build_top.py` | Upper shell changes, the two buttons, the retainer plate. Switch, hinge and striker constants live here. |
| `smooth_front.py` | Smooth front, front-corner case screws, flat bottom and bevel, PCB front standoff, rear latch, inside clean-up, logo recess and blank plate. |
| `fits.py` | Stand-in boxes for the PCB, switches, encoder and AA cell; button swing helper. |
| `render.py` | Splat renderer used for previews and for checking work visually. |

## Frames

- **Final frame F**: X right, Y forward (toward the buttons), Z up, flat underside at z = 0. The seam
  between the shells is at `SEAM = 6.8`.
- **Lisa base frame** + (`DX`, `DY`, `DZ`) = (−1.0, −8.0, −1.4) → F.
- `T_MAC` in `geo.py` maps the original M0100 STLs into F.

## Measured facts (do not re-derive)

- M185 switch plungers are 9 mm from the left edge and 12 mm from the right edge of the Lisa base
  (57.65 wide), about 36.6 mm apart: `SW_L = (−20.9, 26.5)`, `SW_R = (15.7, 26.5)` in F. Plunger free
  top `SW_TOP = 16.1`. An early photo-based estimate was wrong; these are Mike's caliper values.
- The buttons only need to be centred on the outside of the case; the switches are not symmetric.
- PCB front: the wheel-cutout lip is 6.0 mm in from the outside of the front wall (`FRONT_OUT` 45.28);
  the strip of board in front of the cutout is about 2 mm wide; the front rests on ledges at
  `PCB_SEAT = 6.65`. Mike's screw heads have about a 1.2 mm lip; a washer is the fallback.
- Hardware: M3 pilot Ø2.7, clearance Ø3.3, countersink recess Ø6.3 with a 90° cone 1.5 deep.
- Original upper shell side walls lean in 0.0305 mm/mm (1.75°).
- Hinge axle: `AX_Y, AX_Z, AX_R = 6.96, 27.19, 1.225`.

## The design and why

Each item below came from a test print. Do not undo one without a reason.

- **Two buttons** from the single M0100 button, split with a 0.8 mm slot (`GAP`).
- **Strikers:** M3×8 countersunk screw, head toward the switch, in a Ø6 post under each button
  (`COL_BOT`, `COL_R`). Tune with the case screws tight: tightening the case once left the left button
  held down, fixed by turning its striker about a quarter turn shorter. This is in the assembly guide.
- **Hinge / sag:** the left button sagged in the middle and the two could bind. Fix: two extra hinge
  saddles (`SADDLE_DX`) so each half sits in two, sockets closed to 0.15 mm round the bar, and a flat
  retainer plate 0.07 mm under the whole bar (`PLATE_TOP`).
- **Smooth front:** the cable/screw tab is gone from both shells. Case screws are at the front corners
  (`SCREW`), bosses with 45° ramps so the upper shell prints top-down.
- **Rear latch:** the two rear tabs hook into slots in the lower shell; the front screws do the
  clamping. `LATCH_GAP = 0.25`: 0 was too tight to assemble, 0.9 left about 1 mm of play, 0.25 fits
  "nice and tight".
- **Flat bottom:** underside perfectly flat with a 3 mm 45° bevel (`BEVEL`), no shallow curve off the
  bed. Screw recesses are conical, not flat-topped.
- **PCB front standoff** in the wheel cutout (`ST_X`, `ST_Y`), level with the ledges: an M3×6 clamps
  the front of the board so it cannot lift when the rear screw is tightened. Placed erring toward the
  inside of the cutout.
- **Parallel sides (FDM upper only):** `straighten_sides()` makes the upper shell's sides vertical, then they are
  planed to `SIDE_PLANE = 30.39`, so the shell prints standing on a side. That orientation prints much better.
  The resin upper keeps the original's 1.75° lean (Mike, 2026-11-20). Straightening only moves |x| > 22 and above the
  seam, so the lower shell, buttons and retainer are the same for both and pass the checks with either upper.
- **Inside clean-up:** ball-mouse leftovers removed (rectangular frame, the raised patch under it, the
  diagonal rib, stubs on the front wall). An added rib under the roof once hit the battery holder with
  0.15 mm to spare in the model; it was removed.
- **Logo:** recess deepened by 0.6 to 1.4 mm, cut only inside the original rounded outline (an earlier
  cut left a square step round it). `logo_plate_blank.stl` is a template, 0.1 mm clearance, 0.4 mm
  bevel on the back.

## Status

Published and printed; Mike reports the fit is good. Last commit `92b11cc`. Working tree clean as of
2026-11-16.

Open items (all Mike's):
- M0100 model link, creator and licence (`README.md` and `source/README.md` TODOs); confirm the repo
  licence (CC BY-NC-SA 4.0) is compatible. Until then `source/m0100/` stays untracked.
- Assembly photos (`docs/ASSEMBLY.md` TODO).

## Animation

`images/animation.gif` (README, 640×360, 15 fps) and `images/animation.mp4` (1280×720, 30 fps, 10 s loop)
are VTK renders of the assembled models: exploded, together, one full turn, apart again. They were rendered
outside the repo (offscreen VTK through EGL, piped to ffmpeg); re-render them when the models change.

## Working conventions

- **Mike runs git himself.** Leave changes uncommitted and give him the commit command. Claude cannot
  push.
- Never report something as removed, replaced or delivered without checking the output: look at a
  render of the exact feature, and after writing files to the Mac compare checksums there against the
  build. Do not copy and write in the same parallel step.
- Two outputs: FDM upper (print-friendly changes) and resin upper (the original's outside). Keep anything that
  changes the outside only for printing on FDM behind the `fdm` switch.
- Print-friendliness rules Mike has asked for (FDM): flat bottoms with 45° bevels, 45° ramps under bosses,
  conical countersinks, parallel sides for on-side printing, supports only where unavoidable.
- One named constant per tunable dimension, with a comment saying what it does and what was tried.
- Checks: overlap between every pair of parts and against the electronics stand-ins, buttons at rest
  and pressed, **and** a clearance scan (an overlap-only test passed the rib that hit the battery
  holder).
- Manifold notes: `trim_by_plane(n, d)` needs `d` divided by |n|; `.simplify()` before export so STLs
  reload watertight; do not name a script `inspect.py` (shadows the standard library).
- Mike's calipers have drifted off zero more than once; confirm a surprising number before building
  on it.
