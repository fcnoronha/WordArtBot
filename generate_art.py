'''
    Python script for generating the WordArt. Use it as follows:
    $ python3 generate_art.py word_art_text filename.png 
'''

import sys
import os.path
from pythonWordArt import pyWordArt
from random import randint

TEXT = sys.argv[1]
FILE_PATH = sys.argv[2]

def main():
    
    # There are 30 available WordArt styles
    style = randint(0, 29)

    print('GENERATOR: starting')
    w = pyWordArt()
    w.transparentBackground = True
    print('GENERATOR: generating')
    w.WordArt(TEXT, style, 100)
    print('GENERATOR: saving')
    w.toFile(FILE_PATH)
    print('GENERATOR: saved')

if __name__ == "__main__":
    main()