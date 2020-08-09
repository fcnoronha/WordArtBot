'''
    Python script for generating the WordArt. Use it as follows:
    $ python3 generate_art.py 'word_art_text' filename.png is_rainbow_flag
'''

from imgkit import from_string
from random import choice
from PIL import Image, ImageOps
import numpy as np
import os.path
import sys
import cv2

TEXT = sys.argv[1]
FILE_PATH = sys.argv[2]
IS_RAINBOW = len(sys.argv) == 4

def format():
    img = Image.open(FILE_PATH)
    inverted_img = ImageOps.invert(img.convert('RGB'))
    crop_box = list(inverted_img.getbbox())
    crop_box[0] -= 20
    crop_box[1] -= 20
    crop_box[2] += 20
    crop_box[3] += 20
    img.crop(crop_box).save(FILE_PATH)

def wordart_to_image():
    
    h_styles = [6,7,8,9,10,12,13,15,16,18,19,20,21,22,24,26,27,28]
    v_styles = [5,11,17,23,29]
    style = choice(h_styles)
    
    # A FUCKING RAINBOW WORDART
    if IS_RAINBOW: style = 15

    width = max([1000, len(TEXT)*200])
    options = {
        'format': 'png',
        'encoding': "UTF-8",
        'crop-h': '600',
        'crop-w': width,
        'quality': '60',
        'quiet': '',
    }

    with open('template.html', 'r', encoding='utf-8') as template:
        t = template.read()
        t = t.replace('$$STYLE$$', str(style))
        t = t.replace('$$WIDTH$$', str(width))
        t = t.replace('$$TEXT$$', str(TEXT))
        from_string(t, FILE_PATH, options=options)

if __name__ == "__main__":
    wordart_to_image()
    format()