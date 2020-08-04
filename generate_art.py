'''
    Python script for generating the WordArt. Use it as follows:
    $ python3 generate_art.py 'word_art_text' filename.png is_rainbow_flag
'''

from imgkit import from_string
from random import choice
from PIL import Image
import numpy as np
import os.path
import sys
import cv2

TEXT = sys.argv[1]
FILE_PATH = sys.argv[2]
IS_RAINBOW = len(sys.argv) == 4

def format():
    img = cv2.imread(FILE_PATH, -1)
    # remove white backgroung and get bounderies
    mny = mnx = 100000
    mxy = mxx = 0
    for i in range(len(img)):
        for j in range(len(img[i])):
            if (sum(img[i][j]) > 900):
                img[i][j][3] = 0
            elif (sum(img[i][j]) < 1020):
                mxy = max([mxy, i])
                mxx = max([mxx, j])
                mny = min([mny, i])
                mnx = min([mnx, j])
    # offset for framming
    mny = max([0, mny-20])
    mnx = max([0, mnx-20])
    mxy = min([len(img), mxy+20])
    mxx = min([len(img[0]), mxx+20])
    # crop
    img = img[mny:mxy, mnx:mxx]
    # save it
    cv2.imwrite(FILE_PATH, img)

def wordart_to_image():
    
    h_styles = [0,1,2,6,7,8,9,10,12,13,15,16,18,19,20,21,22,24,26,27,28]
    v_styles = [5,11,17,23,29]
    style = choice(h_styles)
    
    # A FUCKING RAINBOW WORDART
    if IS_RAINBOW: style = 15

    width = len(TEXT)*200
    options = {
        'format': 'png',
        'encoding': "UTF-8",
        'crop-h': '700',
        'crop-w': str(width),
        'quality': '60',
        'quiet': ''
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