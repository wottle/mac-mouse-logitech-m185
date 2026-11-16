"""Shared geometry helpers. Final frame F: X right, Y forward (button end), Z up, flat underside at z=0."""
import numpy as np, trimesh, manifold3d as mf
from manifold3d import Manifold, CrossSection, Mesh
import shapely.geometry as sg
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC=os.path.join(ROOT,'source'); BUILD=os.path.join(ROOT,'build'); os.makedirs(BUILD,exist_ok=True)
MACF={'lower':os.path.join(SRC,'m0100','M0100 - Lower Shell.STL'),'upper':os.path.join(SRC,'m0100','M0100 - Upper Shell.STL'),'button':os.path.join(SRC,'m0100','M0100 - Button.STL')}
LISA_BASE=os.path.join(SRC,'lisa','base.stl')            # base.stl from lisa-mouse-logitech-m185/models
LISA_SOLID=os.path.join(BUILD,'lisa_base_solid.stl')     # cleaned copy, made by lisa_solid.py
ZCUT=0.6                       # original underside sits at 0.6 above its ball ring / feet; that becomes z=0
T_MAC=np.array([[-1,0,0,33.39],[0,0,1,-49.06],[0,1,0,-0.12-ZCUT],[0,0,0,1.0]])
DX,DY,DZ=-1.0,-8.0,-1.4        # Lisa base frame -> F
SIDE_DRAFT=0.0305              # the original upper shell's side walls lean in by this much per mm of height (1.75 degrees)
def straighten_sides(m,z0=6.8,x_in=22.0,x_full=27.0):
    """Push the upper shell's side walls out so they are vertical and parallel (seam width unchanged). Only |x|>22 moves."""
    v=m.vertices.copy(); ax=np.abs(v[:,0])
    w=np.clip((ax-x_in)/(x_full-x_in),0,1); w=w*w*(3-2*w)
    v[:,0]+=np.sign(v[:,0])*w*SIDE_DRAFT*np.clip(v[:,2]-z0,0,None)
    m.vertices=v; return m
def tm_mac(name):
    m=trimesh.load(MACF[name],force='mesh'); m.apply_transform(T_MAC); m.merge_vertices(digits_vertex=5)
    if name=='upper': straighten_sides(m)
    return m
def to_man(m):
    M=Manifold(Mesh(vert_properties=np.asarray(m.vertices,dtype=np.float32),tri_verts=np.asarray(m.faces,dtype=np.uint32)))
    assert M.status()==mf.Error.NoError, M.status(); return M
def to_tm(M):
    me=M.to_mesh(); t=trimesh.Trimesh(np.asarray(me.vert_properties)[:,:3],np.asarray(me.tri_verts),process=False); return t
def box(x0,x1,y0,y1,z0,z1): return Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def cyl(x,y,z0,z1,r,r2=None,n=64): return Manifold.cylinder(z1-z0,r,r if r2 is None else r2,n).translate([x,y,z0])
def xs_from_shapely(g):
    polys=[g] if g.geom_type=='Polygon' else list(g.geoms)
    cs=[]
    for p in polys:
        if p.is_empty or p.area<1e-4: continue
        rings=[np.asarray(p.exterior.coords)[:-1]]+[np.asarray(i.coords)[:-1] for i in p.interiors]
        cs.append(CrossSection(rings, mf.FillRule.EvenOdd))
    return CrossSection.batch_boolean(cs,mf.OpType.Add) if len(cs)>1 else (cs[0] if cs else CrossSection())
def prism(g,z0,z1):
    """extrude shapely geometry or CrossSection"""
    c=g if isinstance(g,CrossSection) else xs_from_shapely(g)
    return c.extrude(z1-z0).translate([0,0,z0])
def rrect(x0,x1,y0,y1,r): return sg.box(x0+r,y0+r,x1-r,y1-r).buffer(r,resolution=24) if r>0 else sg.box(x0,y0,x1,y1)
def section_xs(tm,z,min_area=1e-3):
    """CrossSection of a mesh at height z (even-odd fill of the cut loops)"""
    s=tm.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
    if s is None: return CrossSection()
    rings=[]
    for e in s.discrete:
        p=np.asarray(e)[:,:2]
        if len(p)<4 or np.linalg.norm(p[0]-p[-1])>1e-4: continue      # skip open fragments
        p=p[:-1]
        a=0.5*abs(np.dot(p[:,0],np.roll(p[:,1],-1))-np.dot(p[:,1],np.roll(p[:,0],-1)))
        if a>min_area: rings.append(p)
    return CrossSection(rings, mf.FillRule.EvenOdd) if rings else CrossSection()
def xs_to_shapely(c):
    import shapely.ops as so
    polys=c.to_polygons()
    ext=[sg.Polygon(p) for p in polys]
    # even-odd assemble
    g=sg.Polygon()
    for p in sorted(ext,key=lambda q:-q.area): g=g.symmetric_difference(p.buffer(0))
    return g
def save(M,path):
    t=to_tm(M); t.export(path); return t
