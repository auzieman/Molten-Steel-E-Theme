#!/usr/bin/env python3
"""Check native capture pixels and export review movies (requires Pillow/ffmpeg)."""
import argparse,json,re,subprocess
from pathlib import Path
from PIL import Image,ImageChops,ImageStat
p=argparse.ArgumentParser();p.add_argument('results',type=Path);p.add_argument('output',type=Path);p.add_argument('--label',default='motion');p.add_argument('--cycle-seconds',type=float,default=14);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
def delta(first,last):
    with Image.open(first) as x,Image.open(last) as y:
        d=ImageChops.difference(x.convert('RGB'),y.convert('RGB'));return {'changed':d.getbbox() is not None,'mean_rgb_difference':sum(ImageStat.Stat(d).mean)/3}
evidence={}
for variant,slug in [('Ami-Ember','fire'),('Ami-Silver','molten-steel')]:
    frames=a.results/(variant+'-frames');first=frames/'frame-000.png';peak=max(frames.glob('frame-*.png'),key=lambda f:delta(first,f)['mean_rgb_difference'])
    paused=delta(frames/'paused-before.png',frames/'paused-after.png');resumed=delta(frames/'paused-after.png',frames/'resumed.png');motion=delta(first,peak)
    assert motion['changed'],variant+' animation did not change pixels'
    assert not paused['changed'],variant+' pause did not freeze pixels'
    assert resumed['changed'],variant+' resume did not restart motion'
    # Rotate the complete cycle so review starts shortly before the active phase.
    order=(list(range(48,84))+list(range(48))) if a.cycle_seconds==14 else list(range(84));listing=a.output/(slug+'-frames.txt')
    listing.write_text(''.join("file '"+str((frames/f'frame-{n:03d}.png').resolve())+"'\nduration 0.166666667\n" for n in order)+"file '"+str((frames/'frame-048.png').resolve())+"'\n")
    movie=a.output/(slug+'-'+a.label+'-20261026.mp4')
    subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)],check=True)
    listing.unlink()
    with Image.open(peak) as im:im.save(a.output/(slug+'-'+a.label+'-20261026.png'))
    log=(a.results/(variant+'-bench.log')).read_text();rows=re.findall(r'BENCH (animated|paused) wall=([0-9.]+) cpu=([0-9.]+) percent_one_core=([0-9.]+)',log)
    evidence[variant]={'cycle_seconds':a.cycle_seconds,'peak_frame':peak.name,'motion':motion,'pause':paused,'resume':resumed,'benchmark':{kind:{'wall_seconds':float(wall),'cpu_seconds':float(cpu),'percent_one_core':float(percent)} for kind,wall,cpu,percent in rows},'movie':movie.name}
(a.output/('ami-'+a.label+'-review-20261026.json')).write_text(json.dumps(evidence,indent=2)+'\n');print(json.dumps(evidence,indent=2))
