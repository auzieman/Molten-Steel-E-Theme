#!/usr/bin/env python3
"""Stronger original native motion and liquid-metal menu on the checked baseline."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil

parser=argparse.ArgumentParser()
parser.add_argument('baseline',type=Path)
parser.add_argument('output',type=Path)
a=parser.parse_args()
if a.output.exists():parser.error('output must be new')
root=Path(__file__).resolve().parent
shutil.copytree(a.baseline,a.output)
variant=a.output/'Ami-Silver'
shutil.copy2(root/'assets/silver-wallpaper.png',variant/'ami-liquid-silver.png')
p=variant/'edc-dm/menu.edc';s=p.read_text();original=s
cut=s.index('group { name: "e/widgets/menu/default/separator";');g=s[:cut]
g=g.replace('   parts {','   images.image: "ami-liquid-silver.png" COMP;\n   parts {',1).replace('image.normal: "ami-panel.png";','image.normal: "ami-liquid-silver.png";',1)
needle='      part { name: "top";';assert needle in g
g=g.replace(needle,'''      part { name: "ami.menu.readability"; type: RECT; mouse_events: 0;
         description { state: "default" 0.0;
            rel1.relative: 0.14 0.08; rel2.relative: 0.88 0.995;
            color: 239 242 246 195;
         }
      }
'''+needle,1)
s=g+s[cut:]
# Visual additions must not change any menu input programs or content swallows.
def blocks(text):
    found=[]
    for m in re.finditer(r'programs\s*\{',text):
        i=m.end();depth=1
        while depth:
            if text[i]=='{':depth+=1
            elif text[i]=='}':depth-=1
            i+=1
        found.append(text[m.start():i])
    return found
assert blocks(original)==blocks(s)
assert re.findall(r'name: "(e.swallow.[^"]+)"',original)==re.findall(r'name: "(e.swallow.[^"]+)"',s)
p.write_text(s)
wp=a.output/'Ami-Silver-wallpaper'
shutil.copy2(root/'assets/silver-liquid-ripple.svg',wp/'silver-liquid-ripple.svg')
shutil.copy2(root/'molten-wallpaper.edc',wp/'wallpaper.edc')
# Distinct flame silhouettes change shape; no moving text or full-screen flash.
wp=a.output/'Ami-Ember-wallpaper'
for n in range(8):
    phase=n*math.tau/8
    shapes=[]
    for j in range(34):
        x=j*32-18
        tip=85+55*math.sin(phase+j*1.17)
        bend=16*math.sin(phase+j*.8)
        path=f'M{x-17} 256 C{x-32} 212 {x+18} 178 {x+bend} {tip:.2f} C{x+30} {tip+30:.2f} {x+45} 218 {x+20} 256Z'
        shapes.append(f'<path d="{path}" fill="url(#fire)"/>')
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="256" viewBox="0 0 1024 256"><defs><filter id="soft"><feGaussianBlur stdDeviation="2.0"/></filter><linearGradient id="fire" x1="0" y1="1" x2="0" y2="0"><stop stop-color="#fff1a1" stop-opacity=".5"/><stop offset=".28" stop-color="#ffad22" stop-opacity=".65"/><stop offset=".63" stop-color="#f24b08" stop-opacity=".65"/><stop offset="1" stop-color="#e92800" stop-opacity="0"/></linearGradient></defs><g filter="url(#soft)">'+''.join(shapes)+'</g></svg>'
    (wp/f'fire-motion-{n}.svg').write_text(svg)
images=' '.join(f'image: "fire-motion-{n}.svg" COMP;' for n in range(8))
states=[];programs=[]
for n in range(8):
    state='default' if n==0 else 'ripple'+str(n)
    states.append(f'description {{ state: "{state}" 0.0; image.normal: "fire-motion-{n}.svg"; rel1.relative: -0.02 0.65; rel2.relative: 1.02 1.04; color: 255 255 255 225; }}')
    trigger='signal: "load"; source: "";' if n==0 else ''
    nextstate='default' if n==7 else 'ripple'+str(n+1)
    programs.append(f'program {{ name: "liquid.{n}"; {trigger} in: {0.65 if n==0 else 0.18} 0.0; action: STATE_SET "{nextstate}" 0.0; target: "liquid"; after: "liquid.{(n+1)%8}"; }}')
stops=' '.join(f'target: "liquid.{n}";' for n in range(8))
programs+=['program { signal: "ami,pause"; source: "*"; action: ACTION_STOP; '+stops+' }','program { signal: "ami,resume"; source: "*"; after: "liquid.0"; }']
(wp/'wallpaper.edc').write_text('images { image: "scene.png" LOSSY 94; '+images+' }\ncollections { group { name: "e/desktop/background"; data { item: "style" "4"; }\nparts { part { name: "scene"; mouse_events: 0; description { state: "default" 0.0; image.normal: "scene.png"; } }\n#ifdef ANIMATED\npart { name: "liquid"; mouse_events: 0;\n'+'\n'.join(states)+' }\n#endif\n}\n#ifdef ANIMATED\nprograms {\n'+'\n'.join(programs)+' }\n#endif\n} }\n')
files={str(f.relative_to(a.output)):hashlib.sha256(f.read_bytes()).hexdigest() for f in a.output.rglob('*') if f.is_file() and f.name!='motion-source.json'}
(a.output/'motion-source.json').write_text(json.dumps({'profile':'Visible flame silhouettes, paired metal ripples, liquid Silver menus','files':files},indent=2)+'\n')
print('Menu programs/swallow contracts preserved; strong wallpaper sources prepared')
