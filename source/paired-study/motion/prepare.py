#!/usr/bin/env python3
"""Generate a bounded native material-motion study; never changes desktop state."""
import argparse,hashlib,json,re,shutil,math
import cairosvg
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('baseline',type=Path);p.add_argument('output',type=Path);p.add_argument('--visible-motion',action='store_true',help='Shorter quiet interval and stronger motion highlights');a=p.parse_args()
if a.output.exists():p.error('output must be new')
root=Path(__file__).resolve().parent; a.output.mkdir(parents=True)
# These small code-native overlays supplement (rather than replace) raster metal.
ember='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="128" viewBox="0 0 512 128"><defs><linearGradient id="f" x1="0" y1="1" x2="0" y2="0"><stop stop-color="#f97918" stop-opacity=".7"/><stop offset="1" stop-color="#b72e08" stop-opacity="0"/></linearGradient></defs><g fill="none" stroke="url(#f)" stroke-width="2"><path d="M39 127 C118 114 64 99 97 78 C75 108 124 112 135 127"/><path d="M222 128 C295 116 260 99 306 64 C274 106 333 112 351 128"/><path d="M371 128 C433 115 402 106 434 85"/></g><g fill="#ed9b48" opacity=".65"><circle cx="130" cy="91" r=".8"/><circle cx="325" cy="83" r=".7"/><circle cx="443" cy="110" r=".9"/></g></svg>'''
silver='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="128" viewBox="0 0 512 128"><defs><linearGradient id="s"><stop stop-color="#ffffff" stop-opacity="0"/><stop offset=".4" stop-color="#ffffff" stop-opacity=".05"/><stop offset=".51" stop-color="#ffffff" stop-opacity=".8"/><stop offset=".63" stop-color="#8da1b0" stop-opacity=".16"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient></defs><path fill="url(#s)" d="M0 106 Q150 132 245 25 Q330 -12 512 12 L512 62 Q350 15 269 68 Q160 152 0 128Z"/></svg>'''
(root/'assets/ember-wisp.svg').write_text(ember);(root/'assets/silver-reflection.svg').write_text(silver)
for key in ['ember-wisp','silver-reflection']:
    cairosvg.svg2png(url=str(root/'assets'/(key+'.svg')),write_to=str(root/'assets'/(key+'.png')))
# Dedicated small titlebar sprites: the centre stays quiet behind live text.
def title_sprite(slug,phase):
    defs='<defs><linearGradient id="heat" x1="0" y1="1" x2="0" y2="0"><stop stop-color="#ffb13b"/><stop offset=".35" stop-color="#f56d12" stop-opacity=".85"/><stop offset="1" stop-color="#a92505" stop-opacity="0"/></linearGradient></defs>'
    shapes=[]
    if slug=='ember':
        for j,x in enumerate([12,35,61,88,118,149,362,393,421,448,477,500]):
            h=9+8*(.5+.5*math.sin(j*1.7+phase*.75));lean=4*math.sin(j+phase*.8)
            # Two curved edges make each flame taper and curl rather than form a triangle.
            shapes.append(f'<path fill="url(#heat)" d="M{x-9} 32 C{x-13} 27 {x+lean-5} {32-h+7} {x+lean} {32-h} C{x+lean-2} {32-h+10} {x+12} 26 {x+8} 32Z"/>')
            shapes.append(f'<path fill="none" stroke="#ffcc6b" stroke-opacity=".65" stroke-width=".65" d="M{x} 32 Q{x+4} 29 {x+lean} {35-h/2}"/>')
    else:
        for side in [0,350]:
            for band in range(3):
                points=[]
                for x in range(side,side+163,3):
                    y=12+band*5+2.8*math.sin((x-side)/29+phase*.38+band*.8)
                    points.append((x,y))
                path='M'+' L'.join(f'{x:.1f} {y:.2f}' for x,y in points)
                shapes.append(f'<path d="{path}" fill="none" stroke="#293943" stroke-opacity=".40" stroke-width="3.4"/>')
                path='M'+' L'.join(f'{x:.1f} {y-1.6:.2f}' for x,y in points)
                shapes.append(f'<path d="{path}" fill="none" stroke="#f8fcff" stroke-opacity=".85" stroke-width="1.8"/>')
    return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="32" viewBox="0 0 512 32">'+defs+''.join(shapes)+'</svg>'
for slug in ['ember','silver']:
    for phase in range(7):
        cairosvg.svg2png(bytestring=title_sprite(slug,phase).encode(),write_to=str(root/'assets'/f'{slug}-title-{phase}.png'))
def part(name,image,wall=False,index=0):
    # Each motion uses a smooth forward/backward trajectory: no visible reset jump.
    if wall:
        coords=(('-0.015','0.74','1.015','1.0'),('0.015','0.70','1.045','0.98')) if index==0 else (('0.55','0.57','0.92','1.0'),('0.56','0.54','0.93','0.98'))
        alpha=((60,110) if 'ember' in image else (70,130)) if a.visible_motion else ((28,48) if 'ember' in image else (42,80))
        anchor=''
    else:
        coords=(('0.0','0.0','1.0','1.0'),('0.0','0.0','1.0','1.0'));alpha=(190,220) if 'ember' in image else (120,155)
        if a.visible_motion: alpha=(220,255) if 'ember' in image else (185,235)
        anchor='rel1.to: "ami.motion.clip"; rel2.to: "ami.motion.clip";'
    c,d=coords
    states=''
    for n in range(7):
        t=n/6
        vals=[float(c[k])+(float(d[k])-float(c[k]))*t for k in range(4)]
        opacity=round(alpha[0]+(alpha[1]-alpha[0])*t)
        state='default' if n==0 else f'step{n}'
        value=0
        sprite=image if wall else image.replace('-0.png',f'-{n}.png')
        states+=f'''description {{ state: "{state}" {value}.0; image.normal: "{sprite}"; {anchor}
 rel1.relative: {vals[0]} {vals[1]}; rel2.relative: {vals[2]} {vals[3]}; color: 255 255 255 {opacity}; }}\n'''
    return f'part {{ name: "{name}"; mouse_events: 0; '+('clip_to: "ami.motion.clip";' if not wall else '')+states+'}\n'

def programs(names,wall):
    targets=' '.join('target: "'+n+'";' for n in names)
    start='load' if wall else 'e,state,focused';source='' if wall else 'e'
    seq=[1,2,3,4,5,6,5,4,3,2,1,0]
    result=''
    for i,n in enumerate(seq):
        name='ami.flow' if i==0 else f'ami.step{i}'
        nxt=f'ami.step{i+1}' if i<11 else 'ami.flow'
        trigger=f'signal: "{start}"; source: "{source}";' if i==0 else ''
        wait=(1.5 if i==0 else .18) if a.visible_motion else (10.15 if i==0 else .35)
        state='default' if n==0 else f'step{n}';value=0
        result+=f'program {{ name: "{name}"; {trigger} in: {wait} 0.0; action: STATE_SET "{state}" {value}.0; {targets} after: "{nxt}"; }}\n'
    stops='target: "ami.flow"; '+' '.join(f'target: "ami.step{i}";' for i in range(1,12))
    result+=f'''program {{ name: "ami.pause"; signal: "ami,pause"; source: "*"; action: ACTION_STOP; {stops} }}
 program {{ name: "ami.resume"; signal: "ami,resume"; source: "*"; after: "ami.flow"; }}
'''
    if not wall:result+=f'''program {{ name: "ami.unfocus"; signal: "e,state,unfocused"; source: "e";
 action: ACTION_STOP; {stops} after: "ami.rest"; }}
 program {{ name: "ami.rest"; action: STATE_SET "default" 0.0; {targets} }}\n'''
    return result

for variant,slug in [('Ami-Ember','ember'),('Ami-Silver','silver')]:
    out=a.output/variant;shutil.copytree(a.baseline/variant,out)
    overlay=slug+('-wisp.png' if slug=='ember' else '-reflection.png')
    shutil.copy2(root/'assets'/overlay,out/overlay)
    for sprite in (root/'assets').glob(slug+'-title-*.png'):shutil.copy2(sprite,out/sprite.name)
    border=(out/'edc-dm/border.edc').read_text();start=border.index('group { name: "e/widgets/border/default/border";');end=border.index('group { name: "e/widgets/border/sparkle/border";',start)
    g=border[start:end];original=g
    declarations='\n'.join(f'   images.image: "{slug}-title-{n}.png" COMP;' for n in range(7))
    g=g.replace('   parts {',declarations+'\n   parts {',1)
    clip='''part { name: "ami.motion.clip"; type: RECT; mouse_events: 0;
 description { state: "default" 0.0; rel1.to: "top"; rel2.to: "top";
 rel1.offset: 36 3; rel2.offset: -100 -2; color: 255 255 255 255; } }
'''
    g=g.replace('      part { name: "e.text.title";',clip+part('ami.material',slug+'-title-0.png')+'      part { name: "e.text.title";',1)
    g=g.replace('   programs {','   programs {\n'+programs(['ami.material'],False),1)
    assert 'name: "ami.flow"' in g
    # All preexisting action programs remain byte-for-byte in the generated group.
    assert original[original.index('   programs {')+len('   programs {'):] in g
    (out/'edc-dm/border.edc').write_text(border[:start]+g+border[end:])
    wp=a.output/(variant+'-wallpaper');wp.mkdir();shutil.copy2(root/'assets'/(slug+'-wallpaper.png'),wp/'scene.png');shutil.copy2(root/'assets'/overlay,wp/overlay)
    edc=f'''images {{ image: "scene.png" LOSSY 94; image: "{overlay}" COMP; }}
 collections {{ group {{ name: "e/desktop/background"; data {{ item: "style" "4"; }}
 parts {{ part {{ name: "scene"; mouse_events: 0; description {{ state: "default" 0.0; image.normal: "scene.png"; }} }}
#ifdef ANIMATED
'''+part('material',overlay,True)+part('detail',overlay,True,1)+'''#endif
 }
#ifdef ANIMATED
 programs { '''+programs(['material','detail'],True)+''' }
#endif
 } }
'''
    (wp/'wallpaper.edc').write_text(edc)
manifest={str(f.relative_to(a.output)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(a.output.rglob('*')) if f.is_file()}
(a.output/'motion-source.json').write_text(json.dumps({'cycle_seconds':3.48 if a.visible_motion else 14,'mechanism':'native stepped overlays; 1.5 second quiet interval; stronger highlights; focus-gated border loop' if a.visible_motion else 'two native stepped overlays; 10.15 second quiet interval; focus-gated border loop','files':manifest},indent=2)+'\n')
print('Prepared focused-border motion and animated/still wallpapers.')
