# Source meshes

Inputs for `scripts/build_models.py`.

- `lisa/base.stl` — the base from the
  [Lisa mouse conversion](https://github.com/wottle/lisa-mouse-logitech-m185) (`models/v1/base.stl` there; the M185 mounting is the same as the v1 base).
  The M185 mounting is taken from it.
- `m0100/` — the original Apple Macintosh mouse M0100 model: `M0100 - Lower Shell.STL`,
  `M0100 - Upper Shell.STL`, `M0100 - Button.STL` (and the SolidWorks parts they were
  exported from). **This folder is not tracked by git** (see `.gitignore`) until the
  model's licence is confirmed to allow redistribution. To rebuild, download the model
  and put the three STLs here under those names.

<!-- TODO(author): add the M0100 model's link, creator and licence; remove the .gitignore entry if redistribution is allowed. -->
