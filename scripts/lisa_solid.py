"""Rebuild the Lisa mouse base (a messy export) as a clean solid, layer by layer, so it can be used in boolean operations."""
from geo import *
def make_lisa_solid():
    b=trimesh.load(LISA_BASE,force='mesh')
    zs=np.unique(np.round(b.vertices[:,2],2)); parts=[]
    for z0,z1 in zip(zs[:-1],zs[1:]):
        if z1-z0<0.005: continue
        g=section_xs(b,(z0+z1)/2)
        if g.is_empty(): continue
        parts.append(prism(g,z0,z1))
    L=Manifold.batch_boolean(parts,mf.OpType.Add)
    print('lisa base solid: volume',round(L.volume(),1),'mm3 (source mesh',round(b.volume,1),')')
    save(L,LISA_SOLID); return L
if __name__=='__main__': make_lisa_solid()
