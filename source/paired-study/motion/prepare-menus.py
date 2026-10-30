#!/usr/bin/env python3
"""Reskin native menu and start gadget while retaining their input programs."""
import argparse,hashlib,json,re,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('baseline',type=Path);p.add_argument('icons',type=Path);p.add_argument('output',type=Path);p.add_argument('--drawer-theme',type=Path);a=p.parse_args()
if a.output.exists():p.error('output must be new')
shutil.copytree(a.baseline,a.output)
def editpart(s,name,fn):
 match=re.search(r'part\s*\{\s*name:\s*"'+re.escape(name)+r'";',s);assert match,name
 start=match.start();pos=s.index('{',start);depth=1;i=pos+1
 while depth:
  if s[i]=='{':depth+=1
  elif s[i]=='}':depth-=1
  i+=1
 return s[:start]+fn(s[start:i])+s[i:]
def programs(s):
 # Includes original macro-based start gadget programs verbatim.
 result=[]
 for m in re.finditer(r'programs\s*\{',s):
  i=m.end();depth=1
  while depth:
   if s[i]=='{':depth+=1
   elif s[i]=='}':depth-=1
   i+=1
  result.append(s[m.start():i])
 return result
for variant,warm in [('Ami-Ember',True),('Ami-Silver',False)]:
 out=a.output/variant;path=out/'edc-dm/menu.edc';s=path.read_text();original=s
 s=s.replace('   parts {','   images.image: "ami-panel.png" COMP;\n   images.image: "ami-rail-active.png" COMP;\n   images.image: "ami-button-clicked.png" COMP;\n   parts {',1)
 cut=s.index('group { name: "e/widgets/menu/default/separator";');background=s[:cut];tail=s[cut:]
 background=editpart(background,'base',lambda b:b.replace('type: RECT;','').replace('color_class: "menu_base";','image.normal: "ami-panel.png";').replace('color: 197 196 196 255;','color: 255 255 255 255;'))
 background=editpart(background,'top',lambda b:b.replace('image.normal: "vgrad_med_lighter.png";','image.normal: "ami-rail-active.png"; image.border: 12 12 5 5;').replace('TILED_HORIZ(120)','').replace('color_class: "menu_base";','color: 255 255 255 255;'))
 background=editpart(background,'bevel',lambda b:b.replace('image.normal: "bevel_out.png";','image.normal: "ami-rail-active.png";').replace('image.border: 1 1 1 1;','image.border: 5 5 5 5;'))
 background=editpart(background,'shine',lambda b:b.replace('state: "default" 0.0;','state: "default" 0.0; visible: 0;',1))
 s=background+tail
 # Scope selection artwork to item group; preserve its state programs verbatim.
 start=s.index('group { name: "e/widgets/menu/default/item_bg";');end=s.index('group { name: "e/widgets/menu/default/icon";',start);g=s[start:end]
 g=g.replace('   parts {','   images.image: "ami-button-clicked.png" COMP;\n   parts {',1)
 g=editpart(g,'base',lambda b:b.replace('image.normal: "vgrad_med_dark_color.png";','image.normal: "ami-button-clicked.png"; image.border: 6 6 6 6;').replace('TILED_HORIZ(120)',''))
 g=editpart(g,'shine',lambda b:b.replace('visible: 1;','visible: 0;'))
 s=s[:start]+g+s[end:]
 colors={'menu_title':'255 224 175 255' if warm else '235 246 255 255','menu_item':'235 238 242 255' if warm else '32 38 46 255','menu_item_disabled':'125 134 146 255' if warm else '100 107 116 255','menu_item_active':'255 236 198 255' if warm else '25 31 39 255'}
 for name,value in colors.items():s=s.replace('color_class: "'+name+'";','color: '+value+';')
 s=s.replace('color3: 255 255 255 255;','color3: 0 0 0 170;').replace('color2: 255 255 255 255;','color2: 0 0 0 100;')
 # Silver's light panel needs dark ink without the inherited light-text glow.
 if not warm:
  label_start=s.index('group { name: "e/widgets/menu/default/label";')
  label_end=s.index('group { name: "e/widgets/menu/default/submenu";',label_start)
  label=s[label_start:label_end].replace('effect: SHADOW BOTTOM;','effect: NONE;').replace('effect: GLOW;','effect: NONE;')
  s=s[:label_start]+label+s[label_end:]
 # Menu program bodies and every swallowed content name remain unchanged.
 assert programs(original)==programs(s)
 assert re.findall(r'name: "(e.swallow.[^"]+)"',s)==re.findall(r'name: "(e.swallow.[^"]+)"',original)
 path.write_text(s)
 path=out/'edc-dm/start.edc';s=path.read_text();original=s
 shutil.copy2(a.icons/'system-file-manager.png',out/'ami-start-drawer.png')
 s=s.replace('   max: 128 128;','   images.image: "ami-start-drawer.png" COMP;\n   min: 28 28;\n   max: 64 64;')
 s=editpart(s,'shadow',lambda b:b.replace('state: "default" 0.0;','state: "default" 0.0; visible: 0;',1))
 s=editpart(s,'arrow',lambda b:re.sub(r'image.normal: "big_arrow_[^"]+";','image.normal: "ami-start-drawer.png";',re.sub(r'aspect: \([^;]+;','aspect: 1.0 1.0;',re.sub(r'max: (17 14|14 17);','max: 48 48;',b))))
 assert programs(original)==programs(s)
 path.write_text(s)
# Remap existing icon image slots: group names, aliases and behavior stay intact.
if a.drawer_theme:
 slots={
  'icon_efm_folder.png':'places/folder',
  'icon_efm_home.png':'places/user-home',
  'icon_efm_desktop.png':'places/user-desktop',
  'icon_config.png':'apps/preferences-system',
  'icon_efm_hdd.png':'devices/drive-harddisk',
  'icon_efm_cd.png':'devices/drive-optical',
 }
 for variant in ['Ami-Ember','Ami-Silver']:
  manifest={}
  for slot,relative in slots.items():
   target=a.output/variant/'O'/slot;assert target.is_file(),target
   source=a.drawer_theme/'64x64'/(relative+'.png');assert source.is_file(),source
   manifest[slot]={'prior_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'source':relative,'replacement_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
   shutil.copy2(source,target)
  fdo={'preferences-applications':'places/folder-applications','preferences-system':'apps/preferences-system','preferences-desktop':'apps/preferences-desktop','folder-pictures':'places/folder-pictures','folder-documents':'places/folder-documents','folder-download':'places/folder-download','folder-music':'places/folder-music','folder-videos':'places/folder-videos','folder-open':'places/folder-open'}
  for name,relative in fdo.items():
   for target in (a.output/variant/'fdo').rglob(name+'.png'):
    size=16 if target.parent.name=='16' else 64
    source=a.drawer_theme/f'{size}x{size}'/(relative+'.png');assert source.is_file(),source
    key=str(target.relative_to(a.output/variant))
    manifest[key]={'prior_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'source':relative,'replacement_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
    shutil.copy2(source,target)
  (a.output/variant/'ami-menu-icon-slots.json').write_text(json.dumps(manifest,indent=2)+'\n')
files={str(f.relative_to(a.output)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(a.output.rglob('*')) if f.is_file() and f.name!='motion-source.json'}
(a.output/'motion-source.json').write_text(json.dumps({'profile':'visible motion, metallic main menus, drawer start gadget','files':files},indent=2)+'\n')
print('Menu/start action programs and swallow contracts preserved for both variants.')
