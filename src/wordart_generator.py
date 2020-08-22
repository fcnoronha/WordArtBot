from PIL import Image, ImageOps, ImageFilter
from imgkit import from_string
from random import choice
import numpy as np
import os.path
import cv2
import sys
import os

def crop_white(file_path):
    '''
    Crop the white/empty portion of the image
    '''
    img = Image.open(file_path)
    img = img.filter(ImageFilter.MedianFilter(3))
    inverted_img = ImageOps.invert(img.convert('RGB'))
    crop_box = list(inverted_img.getbbox())
    crop_box[0] -= 20
    crop_box[1] -= 20
    crop_box[2] += 20
    crop_box[3] += 20
    img.crop(crop_box).save(file_path)

def wordart_to_image(text, file_path, style):
    '''
    Generate WordArt image directly from the HTML template 
    '''
    h_styles = [6,7,8,9,10,12,13,15,16,18,19,20,21,22,24,26,27,28]
    v_styles = [5,11,17,23,29]
    if style is None: style = choice(h_styles)
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

#def concatenate_images(img_list, file_path):
#    '''
#    Concatenate a list of images horizontally
#    '''
#    img_objs = [Image.open(i) for i in img_list]
#    min_shape = sorted([(np.sum(i.size), i.size) for i in img_objs])[0][1]
#    imgs_comb = np.vstack([np.asarray(i.resize(min_shape)) for i in img_objs])
#    imgs_comb = Image.fromarray(imgs_comb)
#    imgs_comb.save(file_path)

def concatenate_images(img_list, file_path):
    '''
    Concatenate a list of images horizontally
    '''
    img_objs = [cv2.imread(i) for i in img_list]
    w_min = min(img.shape[1] for img in img_objs) 
    img_rsz = [cv2.resize(img, (w_min, int(img.shape[0] * w_min / img.shape[1])), 
                        interpolation=cv2.INTER_CUBIC) for img in img_objs] 
    im_v = cv2.vconcat(img_rsz) 
    cv2.imwrite(file_path, im_v) 

def generate(text, final_file_path, style, n_layer):
    '''
    Generate a wordart image
    '''
    text = text.split(' ')
    n_layer = min([n_layer, len(text)])
    splited_text = [' '.join(x) for x in np.array_split(text, n_layer)]
    img_list = []
    for i in range(n_layer):
        text = splited_text[i]
        file_path = str(i)+final_file_path
        wordart_to_image(text, file_path, style)
        crop_white(file_path)
        img_list.append(file_path)
    concatenate_images(img_list, final_file_path)
    for i in img_list: os.remove(i)

generate('oi felipe meu', 'oi.png', None, 1)