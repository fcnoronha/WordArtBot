from PIL import Image, ImageOps
from imgkit import from_string
from random import choice
import os.path
import sys

def crop_white(file_path):
    '''
    Crop the white/empty portion of the image
    '''
    img = Image.open(file_path)
    inverted_img = ImageOps.invert(img.convert('RGB'))
    crop_box = list(inverted_img.getbbox())
    crop_box[0] -= 20
    crop_box[1] -= 20
    crop_box[2] += 20
    crop_box[3] += 20
    img.crop(crop_box).save(file_path)

def wordart_to_image(text, file_path, is_rainbow):
    '''
    Generate WordArt image directly from the HTML template 
    '''
    h_styles = [6,7,8,9,10,12,13,15,16,18,19,20,21,22,24,26,27,28]
    v_styles = [5,11,17,23,29]
    style = choice(h_styles)
    
    # A FUCKING RAINBOW WORDART
    if is_rainbow: style = 15

    width = max([1000, len(text)*200])
    options = {
        'format': 'png',
        'encoding': "UTF-8",
        'crop-h': '1300',
        'crop-w': width,
        'quality': '60',
        'quiet': '',
    }

    absolute_path = os.getcwd()
    with open('assets/template.html', 'r', encoding='utf-8') as template:
        t = template.read()
        t = t.replace('$$ABS_PATH$$', str(absolute_path))
        t = t.replace('$$STYLE$$', str(style))
        t = t.replace('$$WIDTH$$', str(width))
        t = t.replace('$$TEXT$$', str(text))
        from_string(t, file_path, options=options)

def generate(text, file_path, is_rainbow):
    wordart_to_image(text, file_path, is_rainbow)
    crop_white(file_path)
