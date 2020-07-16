#!/usr/bin/python
import sys
import math
from PIL import Image
import io
import struct
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('--height',dest="height",type=int,default=1)
parser.add_argument('--width',dest="width",type=int,default=-1)
parser.add_argument('--output',dest="output",required=True)
args = parser.parse_args()

frame_count = 0
output_image = Image.new('RGB', (1024*1024*16, 1), color = 'black')
next_print_time = time.time()
while True:
  png = io.BytesIO()
  header = sys.stdin.read(8)
  if not header: break
  assert header.encode("hex") == "89504e470d0a1a0a"
  chunks_exist = True
  png.write(header)
  while chunks_exist:
    chunk_header = sys.stdin.read(8)
    png.write(chunk_header)
    (chunk_len,chunk_type) = struct.unpack(">L4s",chunk_header)
    
    png.write(sys.stdin.read(chunk_len))
    png.write(sys.stdin.read(4)) #CRC
    if chunk_type == "IEND": chunks_exist = False
  png.seek(0)
  frame_count += 1
  im = Image.open(png)
  (avg_r,avg_g,avg_b) = (0,0,0)
  pixel_count = im.size[0] * im.size[1]
  for w in xrange(im.size[0]):
    for h in xrange(im.size[1]):
      (r,g,b) = im.getpixel((w,h))
      avg_r += (r*r)
      avg_g += (g*g)
      avg_b += (b*b)
  avg_r = int(math.sqrt(avg_r / pixel_count))
  avg_g = int(math.sqrt(avg_g / pixel_count))
  avg_b = int(math.sqrt(avg_b / pixel_count))
  frame_color = (avg_r,avg_g,avg_b)

  output_image.putpixel((frame_count-1,0),frame_color)
  if time.time() > next_print_time:
    print frame_count,frame_color,pixel_count
    next_print_time = time.time() + 1

output_image = output_image.crop((0,0,frame_count,1))

if args.width > 0:
  output_image = output_image.resize((args.width,output_image.size[1]),resample=Image.BICUBIC)

if args.height > 1:
  output_image = output_image.resize((output_image.size[0],args.height),resample=Image.BICUBIC)

output_image.save(args.output)
