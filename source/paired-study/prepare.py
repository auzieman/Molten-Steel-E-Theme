#!/usr/bin/env python3
"""Adapt private DarkOs/SilverBlack reference inputs to the verified Ice baseline.
Requires Pillow; output directory must be new. Does not install or select themes.
"""
import argparse, hashlib, json, re, shutil
from pathlib import Path
from PIL import Image
from ilbm import load
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('baseline',type=Path);p.add_argument('references',type=Path);p.add_argument('output',type=Path)
a=p.parse_args()
if a.output.exists():p.error('Output must be new')
def block(text,name,change):
    start=text.index('      part { name: "'+name+'";');end=text.index('{',start)+1;depth=1
    while depth:
        depth+=(text[end]=='{')-(text[end]=='}');end+=1
    return text[:start]+change(text[start:end])+text[end:]
def hide(s):return re.sub(r'(description \{ state: [^;]+;)',r'\1 visible: 0;',s)
def contracts(s):
    return {k:re.findall(p,s) for k,p in {'signals':r'\bsignal\s*:[^;]+;','actions':r'\baction\s*:[^;]+;','targets':r'\btarget\s*:[^;]+;','swallows':r'part \{ name: "[^"\n]+"; type: SWALLOW;'}.items()}
def color(s,name,value):
    return re.sub(r'(color_class \{ name: "'+name+r'";\s*color: )[^;]+;',lambda m:m[1]+value+';',s,count=1)
for variant,folder in [('Ami-Ember','darkos/DarkOS/Bitmaps'),('Ami-Silver','silverblack/Bitmaps')]:
    out=a.output/variant;shutil.copytree(a.baseline,out);ref=a.references/folder;dark=variant=='Ami-Ember'
    source_inputs={}
    def read(name):
        f=ref/name;source_inputs[name]=hashlib.sha256(f.read_bytes()).hexdigest();return load(f)
    title=read('Titlebar/25' if dark else 'Titlebar/default')
    if dark:
        mask=read('Titlebar/25.mask').convert('L')
    for state,y in [('active',0),('inactive',25)]:
        rail=title.crop((0,y,120,y+25)) if dark else title.crop((204,y,284,y+25))
        if dark:rail.putalpha(mask)
        rail.save(out/('ami-rail-'+state+'.png'))
        if not dark:title.crop((107,y,203,y+25)).save(out/('ami-tab-'+state+'.png'))
    rail=Image.open(out/'ami-rail-active.png');rail.transpose(Image.Transpose.ROTATE_90).save(out/'ami-rail-vertical.png')
    # Gadget states are horizontal: active, active pressed, inactive, inactive pressed.
    for symbol,folder in [('close','Close'),('up','Zoom'),('down','Iconify')]:
        im=read(folder+('/Default' if dark else '/25'));w=im.width//4
        if dark:im.putalpha(read(folder+'/Default.amap').convert('L'))
        for state,index in [('active',0),('active-pressed',1),('inactive',2),('inactive-pressed',3)]:
            im.crop((index*w,0,(index+1)*w,im.height)).save(out/f'ami-{symbol}-{state}.png')
    buttons=read('Frames/Button')
    if dark:
        texture=read('Textures/fondbouton')
        for state,x in [('normal',0),('clicked',16)]:
            im=texture.resize((120,30));rim=buttons.crop((x,0,x+16,16))
            for xx,xw,dx,dw in [(0,4,0,4),(4,8,4,112),(12,4,116,4)]:
                for yy,yh,dy,dh in [(0,4,0,4),(4,8,4,22),(12,4,26,4)]:
                    if xx==4 and yy==4:continue
                    patch=rim.crop((xx,yy,xx+xw,yy+yh)).resize((dw,dh));im.alpha_composite(patch,(dx,dy))
            im.save(out/f'ami-button-{state}.png')
        read('Textures/Window').save(out/'ami-panel.png')
    else:
        buttons.crop((0,0,120,30)).save(out/'ami-button-normal.png');buttons.crop((0,30,120,60)).save(out/'ami-button-clicked.png')
        Image.new('RGBA',(4,4),(216,217,219,255)).save(out/'ami-panel.png')
    original=(out/'edc-dm/border.edc').read_text();border=original
    images=list(out.glob('ami-*.png'))
    declarations='\n'.join('   images.image: "'+f.name+'" COMP;' for f in images)
    border=border.replace('group { name: "e/widgets/border/default/border";', 'group { name: "e/widgets/border/default/border";\n'+declarations,1)
    border=block(border,'top',lambda s:s.replace('vgrad_med_lighter.png','ami-rail-inactive.png').replace('vgrad_med_dark_color.png','ami-rail-active.png').replace('TILED_HORIZ(120)','image.border: 7 7 4 4;' if dark else 'image.border: 2 2 4 4;').replace('fill.smooth: 0','fill.smooth: 1'))
    border=block(border,'bevel',hide)
    for titlepart in ['e.text.title','title2']:
        border=block(border,titlepart,lambda s:s.replace('text { font: FNBD; size: 10;', 'min: 0 25;\n            text { font: FN; size: 12;').replace('effect: SHADOW BOTTOM;','effect: NONE;').replace('effect: SOFT_SHADOW BOTTOM;','effect: NONE;'))
    if not dark:
        tab='''      part { name: "ami.tab"; mouse_events: 0;
         description { state: "default" 0.0;
            image.normal: "ami-tab-inactive.png"; image.border: 10 10 3 3;
            rel1.to_y: "top"; rel2.to_y: "top";
            rel1.to_x: "e.text.title"; rel2.to_x: "e.text.title";
            rel1.relative: 0.5 0.0; rel2.relative: 0.5 1.0;
            min: 220 0; max: 220 9999; fixed: 1 0;
         }
         description { state: "focused" 0.0; inherit: "default" 0.0;
            image.normal: "ami-tab-active.png";
         }
      }
'''
        border=border.replace('      part { name: "e.text.title";',tab+'      part { name: "e.text.title";',1)
        # Use existing focus transitions, adding only the passive decoration target.
        end=border.index('group { name: "e/widgets/border/sparkle/border";')
        border=border[:end].replace('target: "top";', 'target: "top"; target: "ami.tab";')+border[end:]
    for symbol in ['close','up','down']:
        for old,state in [('dark','inactive'),('light','active')]:
            for mode,new in [('normal',state),('selected',state+'-pressed')]:
                border=border.replace(f'sym_{symbol}_{old}_{mode}.png',f'ami-{symbol}-{new}.png')
    for name in ['close1','close2','max1','max2','min1','min2']:
        border=block(border,name,lambda s:s.replace('min: 15 15;','min: 21 21;' if dark else 'min: 19 19;').replace('max: 15 15;','max: 21 21;' if dark else 'max: 19 19;'))
    # Native actions stay on their original hit rectangles in this first slice.
    expected=contracts(original);actual=contracts(border)
    if not dark:actual['targets']=[v for v in actual['targets'] if v!='target: "ami.tab";']
    assert actual==expected,'Border action/swallow contract changed'
    (out/'edc-dm/border.edc').write_text(border)
    shelf=(out/'edc-dm/shelf.edc').read_text()
    shelf=shelf.replace('   images.image: "vgrad_med.png" COMP;', '   images.image: "ami-rail-active.png" COMP;\n   images.image: "ami-rail-vertical.png" COMP;\n   images.image: "vgrad_med.png" COMP;',1)
    shelf=block(shelf,'bg',lambda s:s.replace('vgrad_med.png','ami-rail-active.png').replace('vgrad_tall.png','ami-rail-vertical.png').replace('TILED_HORIZ(120)','image.border: 7 7 4 4;').replace('TILED_HORIZ(40)','image.border: 4 4 7 7;').replace('fill.smooth: 0','fill.smooth: 1'))
    for name in ['bevel','shine','dots_start','dots_end']:shelf=block(shelf,name,hide)
    shelf=shelf.replace('//      item: "shaped" "1";','      item: "shaped" "1";')
    assert contracts(shelf)==contracts((a.baseline/'edc-dm/shelf.edc').read_text())
    (out/'edc-dm/shelf.edc').write_text(shelf)
    button=(out/'edc-dm/elm/button.edc').read_text().replace('button_normal.png','ami-button-normal.png').replace('button_clicked.png','ami-button-clicked.png').replace('image.border: 4 4 3 5;','image.border: 10 10 10 10;').replace('image.border: 5 5 4 6;','image.border: 10 10 10 10;')
    (out/'edc-dm/elm/button.edc').write_text(button)
    colors=(out/'colorclasses-dm.edc').read_text()
    for key,value in {'border_title':'200 200 200 255' if dark else '45 45 48 255','border_title_active':'245 245 245 255' if dark else '20 24 28 255','border_bottom':'48 48 48 255' if dark else '100 105 110 255','button_text':'24 24 24 255','button_text_pressed':'24 24 24 255'}.items():colors=color(colors,key,value)
    (out/'colorclasses-dm.edc').write_text(colors)
    fixture='''group { name: "ami/preview-panel";
 images.image: "ami-panel.png" COMP;
 parts { part { name: "panel"; mouse_events: 0;
 description { state: "default" 0.0; image.normal: "ami-panel.png";
 fill { size { relative: 0 0; offset: 12 32; } } } } }
}
'''
    (out/'ami-preview.edc').write_text(fixture)
    entry=(out/'source.edc').read_text();pos=entry.rfind('}');entry=entry[:pos]+'#include "ami-preview.edc"\n'+entry[pos:];(out/'source.edc').write_text(entry)
    manifest={'variant':variant,'reference_files':source_inputs,'contracts':'border and shelf action/signal/swallow declarations preserved; passive tab follows focus','files':{str(f.relative_to(out)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(out.rglob('*')) if f.is_file()}}
    (out/'ami-source.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Prepared both Ami candidates; native border/shelf contracts preserved.')
