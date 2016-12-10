#!/usr/bin/env python
# Author: ZhouZhuo

from config import *
import sys
import struct
import numpy as np
from PIL import Image

def RGBAtoRGB(rgb):
    bg = Image.new('RGB', rgb.size, bgColor)
    bg.paste(rgb, mask=rgb.split()[3])
    return bg

toRGB = {
        'RGBA': RGBAtoRGB,
        'RGB': lambda x: x,
        }

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: %s /path/to/image" % sys.argv[0])
        sys.exit(-1)
    im = Image.open(sys.argv[1])
    im = toRGB[imageType](im)
    # paste source image into target size image
    bg = Image.new('RGB', targetSize, bgColor)
    leftOff = (targetSize[0] - im.size[0]) / 2
    upperOff = (targetSize[1] - im.size[1]) / 2
    bg.paste(im, box=(leftOff, upperOff))
    # transfer it to splash.img binary format
    imArry = np.asarray(bg, dtype=np.uint8).reshape(1,-1)
    outImg = splashMagic
    outImg += struct.pack('III', targetSize[0], targetSize[1], targetOffset)
    reserved = 512 - len(outImg)
    outImg += b'\x00' * reserved
    for n in range(imArry.size):
        outImg += struct.pack('B', imArry[0, n])
    # write it out
    fo = open('splash.img', mode='w+b')
    fo.write(outImg)
    fo.close()
