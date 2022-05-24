import time
import random

from PIL import Image, ImageDraw, ImageFont, ImageOps

import characters
import smw

BACKGROUND = (0,0,0)


class Charm():
    
    def __init__(self, width=64, height=32):
        self.width = width
        self.height = height
        self.mario = characters.Mario()
        self.luigi = characters.Luigi()
        self.mario4 = smw.SuperMarioWorld()
        self.blank = Image.new('RGB',(self.width,self.height),BACKGROUND)

    def walk_through(self, image, character=None):
        if character is None:
            character = self.mario
        for i in range(int((self.width + 16) / 4)):
            image.paste(self.blank,(0,16))
            x = i * 4 - 16
            image.paste(character.images[i%3+1], (x,16))
            time.sleep(0.15)
        image.paste(self.blank,(0,16))
        return True
        

    def turn_back(self, image, character=None):
        if character is None:
            character = self.mario
        for i in range(int((self.width - 16) / 4)):
            image.paste(self.blank,(0,16))
            x = i * 4 - 16
            image.paste(character.images[i%3+1], (x,16))
            time.sleep(0.15)
        _x = x
        for i in range(8):
            image.paste(self.blank,(0,16))
            x = _x + i * 3
            image.paste(ImageOps.mirror(character.images[4]), (x,16))
            time.sleep(0.15)
        _x = x
        for i in range(int((self.width + 16) / 4)):
            image.paste(self.blank,(0,16))
            x = _x - i * 4
            image.paste(ImageOps.mirror(character.images[i%3+1]), (x,16))
            time.sleep(0.15)
        return True

    def random(self, image):
        mario4 = self.mario4

        rand = random.randint(0,100)

        image.paste(self.blank,(0,16))
        if rand < 80:
            self.walk_through(image, self.mario)
        elif rand < 90:
            self.turn_back(image, self.mario)
        elif rand < 96:
            self.walk_through(image, self.luigi)
        elif rand < 98:
            self.turn_back(image, self.luigi)
        else:
            f = 23
            for i in range(int((self.width + 32) / 4)):
                if f == 23:
                    f = 26
                elif f == 26:
                    f = 27
                else: 
                    f = 23
                image.paste(self.blank,(0,0))
                image.paste(mario4.images[f], (i*4-16,0))
                time.sleep(0.15)
