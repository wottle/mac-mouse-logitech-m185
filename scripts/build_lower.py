from geo import *
import shapely.affinity as sa
def build_lower(verbose=True):
    lo=to_man(tm_mac('lower'))
    L=to_man(trimesh.load(LISA_SOLID,force='mesh')).translate([DX,DY,DZ])
    big=lambda g,z0=-5,z1=45: prism(g,z0,z1)
    # --- Mac shell: keep skin, rim, rear latch wall and nose; strip the ball-mouse internals
    P_in=xs_to_shapely(section_xs(tm_mac('lower'),3.6))
    # interior = largest hole of the rim ring
    ring=max(P_in.geoms,key=lambda p:p.area) if P_in.geom_type!='Polygon' else P_in
    interior=sg.Polygon(max(ring.interiors,key=lambda r:sg.Polygon(r).area))
    strip=interior.intersection(sg.box(-40,-42.6,40,60))
    FLOOR=3.1                                   # original floor top
    A=lo-box(-50,50,-60,60,-5,0)                # flat underside
    A=A-big(strip,FLOOR,45)
    flat=rrect(-25.0,25.0,-41.5,38.2,1.5)
    A=A+prism(flat.buffer(-0.02),0,FLOOR)       # fills ball opening, label recess, screw wells
    A=A+prism(strip.buffer(0.02),FLOOR-0.6,FLOOR)   # make the floor top continuous
    # --- M185 mounting from the Lisa base
    R_int=rrect(-24.8,24.8,-41.0,38.0,1.3)      # where the Lisa floor replaces the Mac floor
    R_all=sg.box(-27.35+DX,-32.7+DY,27.2+DX,48.4+DY).intersection(interior.buffer(-0.15))
    LF=2.15
    Lmod=L^(big(R_all,LF,45)+big(R_int,-5,LF))
    A=A-big(R_int,-5,FLOOR+0.001)
    B=(Lmod^big(R_int))+((Lmod^box(-60,60,-60,60,FLOOR-0.01,45))-big(R_int))
    low=A+B
    # plug the Lisa case-screw holes that land in the floor
    for x in (-23.89,23.89):
        p=cyl(x+DX,-29.8+DY,0,LF,3.4)^big(R_int)
        low=low+p
    # nose: remove cable strain-relief block, open screw holes for M3
    low=low-box(-4.2,4.2,44.4,48.0,4.82,9)
    for x in (-6.82,6.82): low=low-cyl(x,44.13,-1,9,1.6)
    up=to_man(tm_mac('upper'))
    for dx,dy in ((0.15,0),(-0.15,0),(0,0.15),(0,-0.15)): low=low-up.translate([dx,dy,0])   # print tolerance where the shells interlock
    low=max(low.decompose(),key=lambda d:d.volume())      # drop sealed internal voids
    return low,Lmod,dict(interior=interior,R_int=R_int,R_all=R_all,strip=strip)
