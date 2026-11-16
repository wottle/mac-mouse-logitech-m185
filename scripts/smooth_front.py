"""v2: remove the front cable/screw tab from both shells and move the case screws to the front corners."""
from geo import *
SCREW=[(-23.2,36.8),(23.2,36.8)]     # front-corner case screws
SEAM=6.8
WALL_X=27.8; RAMP_TOP=23.1        # inner side wall; height where the post ramp meets it
NB=lambda z0,z1,y0=40.0: box(-13.5,13.5,y0,52,z0,z1)
def flush_ceiling(U,x0,x1,y0,y1,label=''):
    """Cut anything hanging below the roof's underside inside the given footprint, flush with the surrounding ceiling."""
    t=to_tm(U); m=2.5
    gx,gy=np.meshgrid(np.arange(x0-m,x1+m+.01,0.4),np.arange(y0-m,y1+m+.01,0.4)); n=gx.size
    loc,ri,_=t.ray.intersects_location(np.c_[gx.ravel(),gy.ravel(),np.full(n,8.0)],np.tile([0,0,1.0],(n,1)),multiple_hits=False)
    X,Y,Z=loc[:,0],loc[:,1],loc[:,2]; keep=Z>np.median(Z)-0.3
    for _ in range(8):
        co=np.linalg.lstsq(np.c_[X[keep],Y[keep],np.ones(keep.sum())],Z[keep],rcond=None)[0]
        r=Z-(co[0]*X+co[1]*Y+co[2]); keep=r>-0.03
    print(f'  ceiling {label}: z = {co[0]:.4f}x + {co[1]:.4f}y + {co[2]:.3f}; clean-ceiling scatter {r[keep].std():.3f} mm; removing up to {-(r.min()):.1f} mm')
    nrm=np.array([co[0],co[1],-1.0]); Ln=np.linalg.norm(nrm)
    return U-box(x0,x1,y0,y1,8,40).trim_by_plane(list(nrm),-(co[2]+0.01)/Ln)
def clean_inside(U):
    """Remove leftovers of the ball-mouse internals from inside the upper shell."""
    U=U-box(12.3,20.7,-19.8,-5.2,8,26.0)                       # bulk of the old rectangular frame
    U=flush_ceiling(U,12.0,21.0,-20.1,-4.9,'old frame')
    U=flush_ceiling(U,-18.5,-6.5,-31.0,-18.5,'diagonal rib')
    nrm=np.array([0,-1.0,-0.1071]); Ln=np.linalg.norm(nrm)      # front wall: one clean inner face (removes the cable-comb stubs)
    U=U-box(-13.5,13.5,36,46,SEAM,26.0).trim_by_plane(list(nrm),-43.55/Ln)
    return U
LOGO_BOX=(-18.7,-8.1,-27.5,-17.1)     # box round the original logo recess
LOGO_DEEPER=0.6                        # extra depth -> 1.4 mm total
LOGO_T=1.4; LOGO_CLEAR=0.1; LOGO_BEVEL=0.4
def logo_void(U):
    x0,x1,y0,y1=LOGO_BOX
    return box(x0,x1,y0,y1,27.3,31.5)-U
def logo_outline(U):
    """Plan outline of the rounded-square recess itself."""
    x0,x1,y0,y1=LOGO_BOX
    skin=(U^box(x0-4,x1+4,y0-4,y1+4,20,32)).hull()            # roof without the dent
    return (logo_void(U)^skin.translate([0,0,-0.35])).project()
def deepen_logo(U):
    x0,x1,y0,y1=LOGO_BOX
    V=logo_void(U); o=logo_outline(U)
    pad=(U^box(x0-1.2,x1+1.2,y0-1.2,y1+1.2,23.0,28.0)).translate([0,0,-LOGO_DEEPER])   # same roof thickness kept underneath
    cut=V.translate([0,0,-LOGO_DEEPER])^o.extrude(30).translate([0,0,15])               # only inside the rounded outline
    return U+pad-cut
def logo_plate(U_before):
    """Flat blank for the recess, on the bed, centred on the origin. z=0 is the back (bevelled); the top is the show face."""
    o=logo_outline(U_before)
    b=o.bounds(); cx,cy=(b[0]+b[2])/2,(b[1]+b[3])/2
    o=o.offset(-LOGO_CLEAR,mf.JoinType.Round).translate([-cx,-cy])
    back=(o.offset(-LOGO_BEVEL,mf.JoinType.Round).extrude(0.01)+o.extrude(0.01).translate([0,0,LOGO_BEVEL])).hull()
    return back+o.extrude(LOGO_T-LOGO_BEVEL).translate([0,0,LOGO_BEVEL])
def smooth_upper(U):
    H=(U-box(-16,16,40,60,-5,60)).hull()                 # outer form without the tab
    U=U^H
    U=U-box(-12.6,12.6,39.6,52,0,17.4)                   # tab remnants inside (screw blocks, cable comb)
    U=U+((H-H.translate([0,-2.8,0]))^NB(SEAM,17.6))      # continuous front wall
    lowband=(U^box(-60,60,-60,60,SEAM,15.0)).hull()
    band2=(U^box(-60,60,-60,60,15.0,23.5)).hull()
    for x,y in SCREW:
        s=1 if x>0 else -1
        boss=cyl(x,y,SEAM,15.0,3.4)
        web=box(min(x,s*29),max(x,s*29),y-2.6,y+2.6,SEAM,15.0)+box(x-2.6,x+2.6,y,46,SEAM,15.0)
        U=U+((boss+web)^lowband)
        # 45 degree ramp from the post up to the side wall, so nothing overhangs when printed top face down
        fp=(cyl(x,y,15.0,23.5,3.4)+box(min(x,s*29),max(x,s*29),y-2.6,y+2.6,15.0,23.5)+box(x-2.6,x+2.6,y,46,15.0,23.5))
        U=U+((fp.trim_by_plane([s,0,-1],(WALL_X-RAMP_TOP)/2**0.5))^band2)
    for x,y in SCREW: U=U-cyl(x,y,SEAM-1,13.8,1.35)
    return clean_inside(U)
BEVEL=3.0
def flat_bottom(Lo):
    """Replace the shallow boat-shaped underside with a dead flat one and a 45 degree bevel round the edge."""
    ZT=4.5
    O=xs_to_shapely(section_xs(to_tm(Lo),ZT))
    O=sg.Polygon((max(O.geoms,key=lambda p:p.area) if O.geom_type!='Polygon' else O).exterior).convex_hull
    bev=(prism(O.buffer(-BEVEL),0,0.01)+prism(O,BEVEL,BEVEL+0.01)).hull()
    solid=bev+prism(O,BEVEL,ZT)
    env=(Lo^box(-60,60,-60,60,-1,ZT)).hull()             # the old outer form
    Lo=Lo+(solid-env.scale([0.985,0.985,1.0]))           # fill between old curve and new flat/bevel (overlapping into the old skin)
    Lo=Lo-(box(-60,60,-60,60,-1,BEVEL)-bev)              # trim anything outside the bevel
    return Lo
# --- extra PCB hold-down in the scroll-wheel cutout -------------------------------------------
FRONT_OUT=45.28                 # outside face of the front wall
CUT_LIP=FRONT_OUT-6.0           # front edge of the PCB wheel cutout (caliper: 6.0 mm in from the outside front)
PCB_SEAT=6.65                   # height of the ledges the front of the PCB rests on
ST_X=-4.0                       # centre of the cutout, left-right (from photo)
ST_Y=CUT_LIP-2.1                # screw axis: shank sits 0.6 mm behind the 2 mm PCB bridge (erring into the cutout); head or washer overlaps it
def front_standoff(Lo):
    post=box(ST_X-3.5,ST_X+3.5,ST_Y-3.0,42.3,0.5,PCB_SEAT)      # runs forward under the bridge and into the front wall
    return Lo+post-cyl(ST_X,ST_Y,0.8,PCB_SEAT+1,1.35)
def relax_latch(Lo):
    """Rear latch: taller, squarer slots (0.85 mm above the tabs instead of touching) and a thicker bar over them."""
    for s in (1,-1):
        x0,x1=sorted((s*4.6,s*15.3))
        Lo=Lo+box(min(s*3.5,s*16.4),max(s*3.5,s*16.4),-44.17,-41.3,15.5,16.7)     # bar reinforced toward the inside
        Lo=Lo-box(x0,x1,-44.6,-41.0,11.9,15.5)
    return Lo
def smooth_lower(Lo):
    H=(Lo-box(-16,16,40,60,-5,60)).hull()
    Lo=Lo^H
    Lo=Lo+(H^NB(-1,SEAM))                                # solid where the tab and its screw holes were
    Lo=Lo-(H.translate([0,-3.3,0])^NB(3.1,12))           # then re-open the interior up to a normal rim
    for x,y in SCREW:
        Lo=Lo+(cyl(x,y,0,SEAM,3.6)^H)
    for x,y in SCREW:                                    # tie the screw posts to the side and front walls so tightening can't flex the floor
        s=1 if x>0 else -1
        web=box(min(x,s*29),max(x,s*29),y-2.5,y+2.5,0.5,SEAM)+box(x-2.5,x+2.5,y,46,0.5,SEAM)
        Lo=Lo+(web^H)
    Lo=flat_bottom(Lo)
    Lo=relax_latch(Lo)
    for x,y in SCREW:
        Lo=Lo-cyl(x,y,-1,SEAM+1,1.65)-cyl(x,y,-1,3.3,3.15)-cyl(x,y,3.299,4.8,3.15,1.65)   # 3.3 clearance; 6.3 recess ending in a 90 degree cone for a countersunk head
    Lo=front_standoff(Lo)
    return max(Lo.decompose(),key=lambda d:d.volume())
