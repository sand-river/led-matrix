import time
import random

from PIL import Image, ImageDraw, ImageFont, ImageOps

import characters
import smw

BACKGROUND = (0,0,0)


class Charm():
    def __init__(self):
        self.mario = characters.Mario()
        self.luigi = characters.Luigi()
        self.mario4 = smw.SuperMarioWorld()

    def random(self, image):
        mario = self.mario
        luigi = self.luigi
        mario4 = self.mario4
        blank = Image.new('RGB',(64,16),BACKGROUND)
        rand = random.randint(0,100)



        image.paste(blank,(0,16))
        if rand < 80:
            for i in range(20):
                image.paste(blank,(0,16))
                image.paste(mario.images[i%3+1], (i*4-16,16))
                time.sleep(0.15)
            image.paste(blank,(0,16))
        elif rand < 90:
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
        elif rand < 96:
            for i in range(20):
                image.paste(blank,(0,16))
                image.paste(luigi.images[i%3+1], (i*4-16,16))
                time.sleep(0.15)
            image.paste(blank,(0,16))
        elif rand < 98:
            for i in range(12):
                image.paste(blank,(0,16))
                image.paste(luigi.images[i%3+1], (i*4-16,16))
                time.sleep(0.15)
            for i in range(8):
                image.paste(blank,(0,16))
                image.paste(ImageOps.mirror(luigi.images[4]), (31 + i * 3,16))
                time.sleep(0.15)
            for i in range(20):
                image.paste(blank,(0,16))
                image.paste(ImageOps.mirror(luigi.images[i%3+1]), (55 - i*4,16))
                time.sleep(0.15)
        else:
            blank = Image.new('RGB',(64,32),BACKGROUND)
            f = 23
            for i in range(24):
                if f == 23:
                    f = 26
                elif f == 26:
                    f = 27
                else: 
                    f = 23
                image.paste(blank,(0,0))
                image.paste(mario4.images[f], (i*4-16,0))
                time.sleep(0.15)
