import cv2
import glob
import numpy
import ntpath
from PIL import Image

IMAGES = ['S3RZX.png', 'HF482.png', 'YMMR9.png']
symbols = glob.glob('lib/*.png')


def guess_captcha(image):
    image = Image.open(image)
    pixels = image.load()
    size = image.size

    # Cleanup background noises from captcha
    for x in range(size[0]):
        for y in range(size[1]):
            if pixels[x, y][0] < 120:
                pixels[x, y] = (0, 0, 0)
            else:
                pixels[x, y] = (255, 255, 255)

    # Search symbols in captcha
    image = numpy.array(image)
    result = []
    for symbol in symbols:
        img_symbol = cv2.imread(symbol)
        match = cv2.matchTemplate(img_symbol, image, cv2.TM_CCOEFF_NORMED)
        if len(match):
            _, quality, _, location = cv2.minMaxLoc(match)
            if quality > 0.8:
                result.append({'x': location[0], 'symbol': ntpath.basename(symbol).replace('.png', '')})
    result = sorted(result, key=lambda k: k['x'])
    return ''.join([x['symbol'] for x in result])


for img in IMAGES:
    print('{} -> {}'.format(img, guess_captcha(img)))