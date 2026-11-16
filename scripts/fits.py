"""Stand-in boxes for the M185 electronics and a helper to swing a button about its hinge, used by the fit checks."""
from geo import *
from build_top import *
def rot_about_axle(M,deg):
    return M.translate([0,-AX_Y,-AX_Z]).rotate([deg,0,0]).translate([0,AX_Y,AX_Z])
# proxies for the electronics (Lisa base frame -> F)
def lbox(x0,x1,y0,y1,z0,z1): return box(x0+DX,x1+DX,y0+DY,y1+DY,z0+DZ,z1+DZ)
prox={'pcb':lbox(-23.3,15.3,-21,48.3,8.05,9.65),
      'swL':box(SW_L[0]-2.9,SW_L[0]+2.9,SW_L[1]-9,SW_L[1]+3.8,8.2,15.3)+box(SW_L[0]-1.45,SW_L[0]+1.45,SW_L[1]-.75,SW_L[1]+.75,15.3,SW_TOP),
      'swR':box(SW_R[0]-2.9,SW_R[0]+2.9,SW_R[1]-9,SW_R[1]+3.8,8.2,15.3)+box(SW_R[0]-1.45,SW_R[0]+1.45,SW_R[1]-.75,SW_R[1]+.75,15.3,SW_TOP),
      'encoder':box(SW_R[0]-10.5,SW_R[0]-3.1,SW_R[1]-6,SW_R[1]+8,8.2,19.0),
      'tact':box(SW_L[0]+3.2,SW_L[0]+10,SW_L[1]-7,SW_L[1]+2,8.2,19.0)}
# AA cell lying in the bay
import math
a0=np.array([-5.6+DX,-24.0+DY]); a1=np.array([16.2+DX,21.5+DY])   # approx bay axis ends
d=a1-a0; L_=np.linalg.norm(d); ang=math.degrees(math.atan2(d[1],d[0]))
aa=Manifold.cylinder(50.5,7.25,7.25,48).rotate([0,90,0]).rotate([0,0,ang]).translate([*(a0+d/L_*((L_-50.5)/2)),2.0+7.25])
prox['AA']=aa
