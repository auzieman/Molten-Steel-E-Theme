#!/usr/bin/env python3
"""Prepare nearly transparent shelf materials from the Ami motion candidates."""
import argparse,shutil,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('baseline',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
if a.output.exists():p.error('output must be new')
out=a.output;shutil.copytree(a.baseline,out)
for variant in ['Ami-Ember','Ami-Silver']:
 p=out/variant/'edc-dm/shelf.edc';s=p.read_text();start=s.index('      part { name: "bg";');end=s.index('      part { name: "bevel";',start)
 b=s[start:end];b=b.replace('color_class: "shelf_base";','color: 255 255 255 32;');s=s[:start]+b+s[end:]
 s=s.replace('   images.image: "ami-rail-active.png" COMP;','   images.image: "ami-shelf-rim.svg" COMP;\n   images.image: "ami-rail-active.png" COMP;',1)
 rim='''      part { name: "ami.rim"; mouse_events: 0;
         description { state: "default" 0.0; image.normal: "ami-shelf-rim.svg";
            image.border: 10 10 10 10; image.middle: 0; color: 255 255 255 145; }
      }
'''
 s=s.replace('      part { name: "bevel";',rim+'      part { name: "bevel";',1);p.write_text(s)
 accent='#dc9c53' if variant=='Ami-Ember' else '#d5e3ed'
 (out/variant/'ami-shelf-rim.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64"><rect x="1" y="1" width="62" height="62" rx="9" fill="none" stroke="{accent}" stroke-opacity=".65"/><path d="M10 2H54" stroke="#fff" stroke-opacity=".4"/></svg>')
manifest={str(f.relative_to(out)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(out.rglob('*')) if f.is_file() and f.name!='motion-source.json'}
(out/'motion-source.json').write_text(json.dumps({'purpose':'Nearly transparent shelf with passive warm/cool metallic rim','files':manifest},indent=2)+'\n')
