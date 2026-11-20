"""Regenerate every STL in models/ and images/preview.png from the source meshes in source/, then run the fit checks.
Run:  python3 scripts/build_models.py

models/common  everything except the upper shell (the same however you print)
models/fdm     upper_shell.stl with straightened, planed sides, to print on a side
models/resin   upper_shell.stl with the original's leaning sides"""
from geo import *
from build_top import *
from build_lower import build_lower
from smooth_front import *
import os, math, fits as check
from lisa_solid import make_lisa_solid
from render import render, grid
R=ROOT
if not os.path.exists(LISA_SOLID): make_lisa_solid()
low,_,_=build_lower(); low=smooth_lower(low).simplify(0.002)
U0=smooth_upper(build_upper()); U=deepen_logo(U0); P=build_plate(); Lh,Rh=build_buttons()
Ur=deepen_logo(smooth_upper(build_upper(fdm=False),fdm=False))
LG=logo_plate(U0)
parts={'common/logo_plate_blank':LG,'common/lower_shell':low,'fdm/upper_shell':U,'resin/upper_shell':Ur,'common/button_left':Lh.simplify(0.0005),'common/button_right':Rh.simplify(0.0005),'common/button_retainer':P}
tm={}
for n,M in parts.items():
    os.makedirs(os.path.dirname(f'{R}/models/{n}.stl'),exist_ok=True)
    to_tm(M).export(f'{R}/models/{n}.stl'); t2=trimesh.load(f'{R}/models/{n}.stl')
    if not t2.is_watertight:
        to_tm(to_man(t2).simplify(0.0005)).export(f'{R}/models/{n}.stl'); t2=trimesh.load(f'{R}/models/{n}.stl')
    tm[n.split('/')[1] if n.startswith('fdm/') or n.startswith('common/') else n]=t2; print(f'{n:24s} {len(t2.faces):7d} tris  watertight {t2.is_watertight} bodies {len(M.decompose())} {np.round(t2.extents,1)} mm')
tm['upper_shell_resin']=tm.pop('resin/upper_shell')
bad=0
for variant,upn in (('fdm','upper_shell'),('resin','upper_shell_resin')):
  print(f'=== {variant} upper shell')
  Pm={k:to_man(tm[v]) for k,v in {'lower':'lower_shell','upper':upn,'plate':'button_retainer','button_left':'button_left','button_right':'button_right'}.items()}
  names=list(Pm)
  for i in range(len(names)):
      for j in range(i+1,len(names)):
          v=(Pm[names[i]]^Pm[names[j]]).volume(); g=Pm[names[i]].min_gap(Pm[names[j]],2) if v<1e-6 else 0
          print(f'  {names[i]:13s} x {names[j]:13s} overlap {v:6.3f}  gap {g:.2f}'); bad+=v>0.02
  for n in names:
      for k,pv in check.prox.items():
          if n=='lower' and k in('pcb','AA'): continue
          v=(Pm[n]^pv).volume(); g=Pm[n].min_gap(pv,2) if v<1e-6 else 0
          if v>0.02 or g<0.5: print('  near/clash',n,k,'overlap',round(v,3),'gap',round(g,2))
  # corner posts vs a full-rectangle PCB is pessimistic; test against the PCB minus its chamfered corners instead
  for deg in (1.5,3,4.5):
      for n in ('button_left','button_right'):
          B=check.rot_about_axle(Pm[n],-deg)
          for o in names:
              if o!=n and (B^Pm[o]).volume()>0.02: print('  CLASH pressed',deg,n,o); bad+=1
print('printed-part problems:',bad)
beige=(222,214,190); blue=(90,140,220); org=(230,150,70); grn=(110,190,120); dk=(150,145,130)
os.makedirs(R+'/images',exist_ok=True)
asm=[(tm['upper_shell'],beige),(tm['button_left'],dk),(tm['button_right'],dk),(tm['lower_shell'],beige)]
ims=[render(asm,az=60,el=25,size=(900,800)),render(asm,az=90,el=6,size=(900,800)),render(asm,az=-125,el=32,size=(900,800)),
     render([(tm['lower_shell'],beige)],az=70,el=50,size=(900,800)),render([(tm['lower_shell'],beige)],az=-90,el=-89.9,size=(900,800)),
     render([(tm['upper_shell'],beige),(tm['button_left'],blue),(tm['button_right'],org),(tm['button_retainer'],grn)],az=-65,el=-60,size=(900,800))]
grid(ims,3,labels=['assembled, front','front, straight on','assembled, rear','lower shell: front-corner screw posts','underside','upper shell inside']).save(R+'/images/preview.png')
