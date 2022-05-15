import time
import random

from PIL import Image, ImageDraw, ImageFont, ImageOps

import characters

BACKGROUND = (0,0,0)


class Charm():
    def __init__(self):
        self.mario = characters.Mario()
        self.luigi = characters.Luigi()


    def random(self, image):
        mario = self.mario
        blank = Image.new('RGB',(64,16),BACKGROUND)
        rand = random.randint(0,100)
        if rand > 10:
            for i in range(20):
                image.paste(blank,(0,16))
                image.paste(mario.images[i%3+1], (i*4-16,16))
                time.sleep(0.15)
            image.paste(blank,(0,16))
        else:
            for i in range(12):
                image.paste(blank,(0,16))
                image.paste(mario.images[i%3+1], (i*4-16,16))
                time.sleep(0.15)
            for i in range(8):
                image.paste(blank,(0,16))
                image.paste(ImageOps.mirror(mario.images[4]), (31 + i * 3,16))
                time.sleep(0.15)
            for i in range(20):
                image.paste(blank,(0,16))
                image.paste(ImageOps.mirror(mario.images[i%3+1]), (55 - i*4,16))
                time.sleep(0.15)

