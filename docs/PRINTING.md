# Printing

The parts were designed for a 0.4 mm nozzle and PLA. Orientations below are what each
part was designed for; slicer settings are not included yet.

<!-- TODO(author): add the printer, layer height, and slicer projects (print/) once the settings are final. -->

| Part | Orientation | Supports |
|------|-------------|----------|
| `lower_shell.stl` | As modelled, flat underside on the bed. | None needed. The underside is flat with a 3 mm × 45° bevel, and the case-screw recesses end in a 45° cone. The battery door seat is the only flat overhang (about 1 mm up), the same as on the Lisa mouse base. |
| `upper_shell.stl` | On its side, or top face down. | On its side: the side walls are vertical and flat, so the shell lies flat and the top stands square to the bed. Top face down: the screw posts ramp to the side walls at 45°, so only the two small rear latch tabs (7 × 3 mm) hang free. |
| `button_left.stl`, `button_right.stl` | Not settled. | The caps are solid. The striker posts have a 2.7 mm hole for an M3 screw. |
| `button_retainer.stl` | Flat, countersinks up. | None. |
| `logo_plate_blank.stl` | Show face down on the bed for the best finish. | None. The back edge has a 0.4 mm bevel so it seats fully in the recess. |
| `on_off_button.stl`, `battery_cover_1.stl`, `battery_cover_2.stl` | As for the Lisa mouse. | See the Lisa mouse printing guide. |

## Fit notes

- The buttons have 0.3 mm clearance per side in the shell opening and a 0.8 mm slot
  between them. Sand the cap edges lightly if they rub.
- The hinge bar on each button runs in sockets with 0.15 mm clearance, with the retainer
  plate 0.07 mm underneath. If a button does not swing freely, sand the bar lightly or
  back the retainer screws off a little.
- The logo recess is 10.1 × 10.1 mm and 1.4 mm deep; the blank is 9.9 × 9.9 × 1.4 mm.
