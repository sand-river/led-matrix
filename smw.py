import numpy as np
from PIL import Image 

class SuperMarioWorld():
    palette = [0, 0, 0, 41, 41, 41, 140, 90, 24, 255, 255, 255, 80, 0, 0, 255, 115, 107, 143, 88, 31, 33, 49, 140, 255, 66, 115, 66, 132, 156, 255, 64, 112, 132, 222, 206, 255, 248, 255, 32, 48, 143, 181, 41, 99, 255, 214, 198, 176, 40, 96, 255, 255, 0, 128, 216, 207, 255, 112, 111, 64, 128, 159, 255, 208, 192, 255, 222, 115, 222, 165, 57, 74, 74, 74, 255, 115, 24, 66, 0, 0, 255, 0, 0, 189, 0, 0, 222, 222, 173, 255, 216, 112, 136, 88, 24, 32, 48, 136, 255, 255, 156, 223, 160, 63, 248, 248, 248, 248, 112, 104, 0, 24, 33, 255, 222, 0, 41, 49, 74, 239, 0, 181, 248, 216, 112, 8, 16, 0, 216, 160, 56, 99, 105, 123, 24, 40, 66, 156, 148, 66, 0, 0, 0]

    def __init__(self):
        characters = np.load('./mario.npy', allow_pickle=True)
        images = [(Image.fromarray((character).astype(np.uint8), mode='P')) for character in characters]
        for image in images:
            image.putpalette(self.palette)
        self.images = images


if __name__ == '__main__':
    smw = SuperMarioWorld()
    print(smw.images[1])
