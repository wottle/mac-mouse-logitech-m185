import numpy as np, trimesh
from PIL import Image
def view_matrix(az,el):
    az,el=np.radians(az),np.radians(el)
    # camera looks at origin from direction (az around z, el above horizon); returns rows: right, up, toward-camera
    d=np.array([np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)])
    r=np.cross([0,0,1],d); r/=np.linalg.norm(r); u=np.cross(d,r)
    return np.array([r,u,d])
def render(items,az=-60,el=30,res=0.07,n_per_mm2=260,bg=(255,255,255),pad=3,light=(-0.35,0.45,0.82),size=None):
    """items: list of (trimesh, rgb). orthographic splat renderer."""
    V=view_matrix(az,el); P=[];N=[];C=[]
    for m,col in items:
        n=int(max(20000,m.area*n_per_mm2)); p,fi=trimesh.sample.sample_surface(m,n)
        P.append(p@V.T); N.append(m.face_normals[fi]@V.T); C.append(np.tile(np.array(col,float),(n,1)))
    P=np.vstack(P);N=np.vstack(N);C=np.vstack(C)
    lo=P[:,:2].min(0)-pad; hi=P[:,:2].max(0)+pad
    W=int((hi[0]-lo[0])/res)+1; H=int((hi[1]-lo[1])/res)+1
    ix=((P[:,0]-lo[0])/res).astype(int); iy=((hi[1]-P[:,1])/res).astype(int)
    o=np.argsort(P[:,2]); flat=iy*W+ix
    zb=np.full(W*H,-1e9); idx=np.full(W*H,-1)
    zb[flat[o]]=P[o,2]; idx[flat[o]]=o
    L=np.array(light,float); L/=np.linalg.norm(L)
    img=np.tile(np.array(bg,float),(W*H,1)); k=idx>=0
    nn=N[idx[k]]; nn=np.where(nn[:,2:3]<0,-nn,nn)
    sh=0.30+0.70*np.clip(nn@L,0,1)
    img[k]=C[idx[k]]*sh[:,None]
    img=img.reshape(H,W,3)
    # fill pinholes: simple 3x3 max-depth neighbour fill
    zb2=zb.reshape(H,W); hole=(zb2<-1e8)
    for dy,dx in ((0,1),(0,-1),(1,0),(-1,0)):
        sh_img=np.roll(img,(dy,dx),(0,1)); sh_h=np.roll(hole,(dy,dx),(0,1))
        fill=hole&~sh_h; img[fill]=sh_img[fill]; hole=hole&~fill
    im=Image.fromarray(np.clip(img,0,255).astype(np.uint8))
    if size: im.thumbnail(size,Image.LANCZOS)
    return im
def grid(ims,cols,bg=(255,255,255),labels=None):
    from PIL import ImageDraw
    w=max(i.width for i in ims); h=max(i.height for i in ims); rows=(len(ims)+cols-1)//cols
    out=Image.new('RGB',(cols*w,rows*h),bg); d=ImageDraw.Draw(out)
    for k,i in enumerate(ims):
        x=(k%cols)*w+(w-i.width)//2; y=(k//cols)*h+(h-i.height)//2; out.paste(i,(x,y))
        if labels: d.text(((k%cols)*w+8,(k//cols)*h+6),labels[k],fill=(40,40,40))
    return out
