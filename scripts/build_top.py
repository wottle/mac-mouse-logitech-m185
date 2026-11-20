from geo import *
# ---- shared dimensions (final frame) ----
AX_Y,AX_Z,AX_R=6.96,27.19,1.225            # button hinge axle (measured from the original button)
PLATE_TOP=25.90                          # 0.07 under the hinge bar
PLATE_T=2.4
BOSS=[(-11.75,0.2),(11.75,0.2)]
SADDLE_DX=10.6                           # extra hinge saddles: copies of the originals moved outboard
SW_L=(-20.9,26.5); SW_R=(15.7,26.5)      # M185 switch plungers: caliper 9 mm / 12 mm from the Lisa base edges, shifted with the mounting
SW_TOP=16.1                              # plunger free height
COL_BOT=18.9; COL_R=3.0
GAP=0.8                                  # slot between the two buttons

def build_upper(fdm=True):
    U=to_man(tm_mac('upper',fdm))
    # 1. close the cable opening in the nose
    U=U+box(-3.95,3.95,45.15,47.2,4.85,13.95)
    # 2. nose screw bores opened from 2.5 to 2.7 for M3
    for x in (-6.82,6.82): U=U-cyl(x,44.13,4.0,16.4,1.35)
    # 3. two more hinge saddles so each half-button sits in two
    for s in (1,-1):
        sad=to_man(tm_mac('upper',fdm))^box(min(s*5.5,s*7.5),max(s*5.5,s*7.5),2.85,10.5,26.0,30.3)
        U=U+sad.translate([s*SADDLE_DX,0,0])
    # 3b. close up the saddle sockets round the hinge bar (original had 0.5 mm of play above it; now 0.15)
    for s in (1,-1):
        for xa in (5.7,5.7+SADDLE_DX):
            x0,x1=sorted((s*(xa+0.15),s*(xa+1.45)))
            U=U+(box(x0,x1,5.6,8.3,AX_Z,29.3)-Manifold.cylinder(3,AX_R+0.15,AX_R+0.15,64).rotate([0,90,0]).translate([x0-0.5,AX_Y,AX_Z]))
    # 4. two bosses for the hinge retainer plate
    for x,y in BOSS:
        U=U+cyl(x,y,PLATE_TOP,30.0,3.5)
    for x,y in BOSS:
        U=U-cyl(x,y,PLATE_TOP-1,30.1,1.35)
    return U
def build_plate():
    g=rrect(-20.4,20.4,-3.6,8.5,1.5)
    P=prism(g,PLATE_TOP-PLATE_T,PLATE_TOP)
    for x,y in BOSS:
        P=P-cyl(x,y,PLATE_TOP-PLATE_T-1,PLATE_TOP+1,1.65)
        P=P-cyl(x,y,PLATE_TOP-PLATE_T-0.01,PLATE_TOP-PLATE_T+1.5,3.15,1.65)   # countersink, head underneath
    return P
def build_buttons():
    bt=tm_mac('button'); B=to_man(bt)
    capbox=box(-18.1,18.1,11.6,37.6,28.4,45)
    cap=(B^capbox).hull()
    S=B+cap
    S=S-box(-0.9,0.9,13.6,34.4,15,28.41)            # remains of the single-button rib
    for s in (1,-1):                                 # windows for the added saddles (same form as the original pair: bare axle under the saddle)
        x0,x1=sorted((s*(5.6+SADDLE_DX-0.3),s*(7.4+SADDLE_DX+0.4)))
        S=S-box(x0,x1,8.0,11.4,20,33)-box(x0,x1,4.0,8.3,AX_Z-0.2,33)
        S=S+Manifold.cylinder(x1-x0+0.2,AX_R,AX_R,48).rotate([0,90,0]).translate([x0-0.1,AX_Y,AX_Z])
    S=S-box(-GAP/2,GAP/2,-10,60,0,60)
    R=S^box(0,60,-10,60,0,60); Lh=S^box(-60,0,-10,60,0,60)
    up=to_man(tm_mac('upper'))
    # right striker: post under the cap
    R=R+cyl(SW_R[0],SW_R[1],COL_BOT,30.0,COL_R)
    R=R-cyl(SW_R[0],SW_R[1],COL_BOT-1,COL_BOT+9.0,1.35)
    # left striker: post outboard of the cap, tied into the side flange and the cap
    x,y=SW_L
    blk=box(x-COL_R-0.25,-14.5,y-3.25,y+3.25,25.0,28.7)
    for dz in (0,-0.9,-1.8):
        for dx in (0,0.4): blk=blk-up.translate([dx,0,dz])
    Lh=Lh+blk+cyl(x,y,COL_BOT,26.0,COL_R)
    Lh=Lh-cyl(x,y,COL_BOT-1,COL_BOT+7.5,1.35)
    relief=up.translate([0,0,-0.25])             # print tolerance under the shell edges that stop the buttons
    return Lh-relief,R-relief
