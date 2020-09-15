#!/usr/bin/python3

import ghostscript
import locale
import fnmatch
import os
import re
import sys
import warnings
import logging 

from PIL import Image, ImageOps, ImageChops
from pdf2image import convert_from_path

def findFiles(which, where='.'):
    '''Returns list of filenames from `where` path matched by 'which'
       shell pattern. Matching is case-insensitive.'''
    
    # TODO: recursive param with walk() filtering
    rule = re.compile(fnmatch.translate(which), re.IGNORECASE)
    return [name for name in os.listdir(where) if rule.match(name)]

def ai2jpegGs(pdf_input_path, jpeg_output_path):
    args = ["pdf2jpeg", # actual value doesn't matter
            "-dNOPAUSE",
            "-sDEVICE=jpeg",
            "-r144",
            "-sOutputFile=" + jpeg_output_path,
            pdf_input_path]

    encoding = locale.getpreferredencoding()
    args = [a.encode(encoding) for a in args]

    ghostscript.Ghostscript(*args)

    
def ai2JpegCairo(inputFolder, outputFolder):
    files2Convert = findFiles('*.ai', inputFolder)

    for file2Convert in files2Convert:
        print('Working on ' + file2Convert)
        img = convert_from_path(inputFolder + '/' + file2Convert, use_pdftocairo=True, single_file=True)
        baseFilename  =  os.path.splitext(os.path.basename(file2Convert))[0] + '.jpg'
        img[0].save(outputFolder + '/' + baseFilename, 'JPEG')


def mirrorImg(img):
    img_mirror = ImageOps.mirror(img)
    return img_mirror;

def cropImg(img, border=100, color='white'):
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return ImageOps.expand(img.crop(bbox), border = border, fill= color)

def convertMirrorCropBatch(inputFolder, outputFolder):
    files2Convert = findFiles('*.ai', inputFolder)

    for file2Convert in files2Convert:
        try:
            print('Working on ' + file2Convert)
            img = convert_from_path(inputFolder + '/' + file2Convert, use_pdftocairo=True, single_file=True)
            baseFilename  =  os.path.splitext(os.path.basename(file2Convert))[0] + '.jpg'
            #img[0].save(outputFolder + '/' + baseFilename, 'JPEG')
            imgMirror = mirrorImg(img[0])
            imgCrop = cropImg(imgMirror)
            imgMirror.save(outputFolder + '/' + baseFilename, quality=95)
            imgCrop.save(outputFolder + '/cropped-mirror/' + baseFilename, quality=95)
        except:
            pass


def main(inputFolder, outputFolder):
    print ('Converting *.ai files...')
    convertMirrorCropBatch(inputFolder, outputFolder)

warnings.simplefilter('ignore', Image.DecompressionBombWarning)
logging.basicConfig(filename="ai2jpeg.log", format='%(asctime)s %(message)s', filemode='w') 
logger=logging.getLogger() 
  
#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    try:
        inputFolder = sys.argv[1]
        outputFolder = sys.argv[2]
    except:
        inputFolder = './input'
        outputFolder = './output'
        
    main(inputFolder, outputFolder)

#ai2JpegCairo('./input', './output')

#print ('Mirroring and cropping JPG images...')
#for entry in os.scandir('./output'):
#    if (entry.path.endswith(".jpg") or entry.path.endswith(".jpeg")) and entry.is_file():
#        img = Image.open(entry.path)
#        imgMirror = mirrorImg(img)
#        imgCrop = cropImg(imgMirror)
#        imgMirror.save('./output/' + entry.name, quality=95)
#        imgCrop.save('./output/cropped-mirror/' + entry.name, quality=95)


