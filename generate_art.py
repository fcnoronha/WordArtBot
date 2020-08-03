'''
    Python script for generating the WordArt. Use it as follows:
    $ python3 generate_art.py word_art_text filename.png 
'''

import sys
import cv2
import os.path
import numpy as np
from PIL import Image
from random import randint
from imgkit import from_string

TEXT = sys.argv[1]
FILE_PATH = sys.argv[2]

def format():
    
    img = cv2.imread(FILE_PATH, -1)
    # removing white bg and getting bounderies
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
    img = img[mny:mxy, mnx:mxx]

    # save it
    cv2.imwrite(FILE_PATH, img)

def main():
    
    # there are 30 available WordArt styles
    style = randint(0, 29)
 
    options = {
        'format': 'png',
        'encoding': "UTF-8",
        'crop-h': '400',
        'crop-w': '1000',
        'quality': '100',
        'custom-header' : [
            ('Accept-Encoding', 'gzip')
        ]
    }

    with open('template.html', 'r', encoding='utf-8') as template:
        t = template.read()
        t = t.replace('$$STYLE$$', str(style))
        t = t.replace('$$TEXT$$', str(TEXT))
        from_string(t, FILE_PATH, options=options)

    format()

if __name__ == "__main__":
    main()