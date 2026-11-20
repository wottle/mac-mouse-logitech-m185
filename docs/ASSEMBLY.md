# Assembly

Taking the M185 apart, sliding its power switch to the side, and fitting the power
slider, battery contacts and battery door are the same as for the Lisa mouse. Use the
[Lisa mouse assembly guide](https://github.com/wottle/lisa-mouse-logitech-m185/blob/main/docs/ASSEMBLY.md)
for those steps; the steps below cover what is different. The upper shell is in `models/fdm/` or
`models/resin/` (whichever you printed); everything else is in `models/common/`.

<!-- TODO(author): add assembly photos. -->

## Lower shell

1. Fit the power slider and seat the PCB in the lower shell. The front of the board rests
   on the two angled ledges and on the standoff in the scroll-wheel cutout.
2. Fasten the rear of the PCB with the M3×4 flat head screw.
3. Fasten the front with an M3×6 in the standoff in the scroll-wheel cutout. Its head
   clamps the narrow strip of PCB in front of the cutout; add a washer if the head does
   not reach far enough. This stops the front of the board lifting when the rear screw
   is tightened.
4. Fit the battery contacts and the battery door.

## Upper shell

5. Turn the upper shell upside down. Drop both buttons in so the hinge bar on each sits
   in its two sockets.
6. Lay the retainer plate over the hinge bars, countersinks facing you, and fasten it to
   the two bosses with M3×6 countersunk screws. The buttons should swing freely.
7. Drive an M3×8 countersunk screw into the post under each button, head toward the
   switch. Start about 1 mm short of fully seated.

## Closing up

8. Hook the two tabs at the rear of the upper shell into the slots in the lower shell's
   rear wall, then lower the front.
9. Fit the two M3×8 countersunk case screws into the front corners from underneath.

## Tuning the buttons

10. Each striker screw sets how far its button travels before the switch clicks:
    out = longer (clicks sooner), in = shorter. Aim for no free play and no pre-click.
11. Do the final tuning with the two case screws fully tight. Tightening them pulls the
    upper shell down a little, which lowers both strikers. A button that clicked fine
    with the screws loose can end up held down (it feels stuck, with no click) once they
    are tight. If that happens, open the shell, turn that button's striker screw in about
    a quarter turn to shorten it, close up, tighten and test again. On the first build
    the left button needed this and the right did not.

## Logo

12. Print your logo plate from `logo_plate_blank.stl` and glue it into the recess on top.
