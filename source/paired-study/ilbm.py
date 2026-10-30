"""Decode the indexed ILBM reference bitmaps without external Amiga tools."""
import struct
from PIL import Image

def load(path):
    data=path.read_bytes()
    if data[:4]!=b'FORM' or data[8:12]!=b'ILBM':
        return Image.open(path).convert('RGBA')
    chunks={}; pos=12
    while pos+8<=len(data):
        key=data[pos:pos+4]; size=int.from_bytes(data[pos+4:pos+8],'big')
        chunks[key]=data[pos+8:pos+8+size]; pos+=8+size+(size&1)
    w,h,x,y,planes,mask,compression,pad,transparent,xa,ya,pw,ph=struct.unpack('>HHhhBBBBHBBhh',chunks[b'BMHD'])
    assert (planes<=8 or planes==24) and compression in (0,1), (path,planes,compression)
    body=chunks[b'BODY']; raw=bytearray(); pos=0
    if compression:
        while pos<len(body):
            n=body[pos];pos+=1
            if n<128:raw.extend(body[pos:pos+n+1]);pos+=n+1
            elif n>128:raw.extend(body[pos:pos+1]*(257-n));pos+=1
    else:raw=body
    stride=((w+15)//16)*2; count=planes+(8 if mask==4 else (mask==1))
    assert len(raw)>=stride*count*h
    palette=chunks.get(b'CMAP',b'\0\0\0\xff\xff\xff'); colors=[tuple(palette[i:i+3]) for i in range(0,len(palette),3)]
    pixels=[]
    for yy in range(h):
        for xx in range(w):
            index=sum(((raw[(yy*count+p)*stride+xx//8]>>(7-xx%8))&1)<<p for p in range(planes))
            alpha=255
            if mask==4:alpha=sum(((raw[(yy*count+planes+p)*stride+xx//8]>>(7-xx%8))&1)<<p for p in range(8))
            elif mask==1:alpha=255*((raw[(yy*count+planes)*stride+xx//8]>>(7-xx%8))&1)
            elif mask==2 and index==transparent:alpha=0
            pixels.append((index & 255, (index>>8)&255, (index>>16)&255,alpha) if planes==24 else (*colors[index],alpha))
    image=Image.new('RGBA',(w,h));image.putdata(pixels);return image
