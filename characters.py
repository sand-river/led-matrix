from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np

class Character():
    images = []
    dot_chars = []
    colors = {}

    def __init__(self):
#        for dot_char in self.dot_chars:
#            arr = np.array(self.conv(dot_char, self.colors))
#            self.images.append(
#                Image.fromarray((arr * 255).astype(np.uint8))
#            )
        self.images = [
            Image.fromarray(
                (np.array(
                    self.conv(dot_char, self.colors)
                ) * 255).astype(np.uint8)
            ) for dot_char in self.dot_chars
        ]



    def conv(self, dot, colors):
        return list(map(
            lambda x: list(map(
                lambda x: eval(x, None, colors), list(x)
            )), dot.split()
        ))

class Mario(Character):
    colors = {
        'R': (128,255,255),
        'G': (255,192,255),
        'O': (96,160,224),
        'N': (0,0,0)
    }

    dot_chars = [
'\
NNNNNRRRRRNNNNNN \
NNNNRRRRRRRRRNNN \
NNNNGGGOOGONNNNN \
NNNGOGOOOGOOONNN \
NNNGOGGOOOGOOONN \
NNNGGOOOOGGGGNNN \
NNNNNOOOOOOONNNN \
NNNNGGRGGGNNNNNN \
NNNGGGRGGRGGGNNN \
NNGGGGRRRRGGGGNN \
NNOOGRORRORGOONN \
NNOOORRRRRROOONN \
NNOORRRRRRRROONN \
NNNNRRRNNRRRNNNN \
NNNGGGNNNNGGGNNN \
NNGGGGNNNNGGGGNN\
',
'\
NNNNNRRRRRNNNNNN \
NNNNRRRRRRRRRNNN \
NNNNGGGOOGONNNNN \
NNNGOGOOOGOOONNN \
NNNGOGGOOOGOOONN \
NNNGGOOOOGGGGNNN \
NNNNNOOOOOOONNNN \
NNGGGGRRGGNNNNNN \
OOGGGGRRRGGGOOON \
OOOGGGRORRRGGOON \
OONNRRRRRRRNNGNN \
NNNRRRRRRRRRGGNN \
NNRRRRRRRRRRGGNN \
NGGRRRNNNRRRGGNN \
NGGGNNNNNNNNNNNN \
NNGGGNNNNNNNNNNN\
',
'\
NNNNNNNNNNNNNNNN \
NNNNNNRRRRRNNNNN \
NNNNNRRRRRRRRRNN \
NNNNNGGGOOGONNNN \
NNNNGOGOOOGOOONN \
NNNNGOGGOOOGOOON \
NNNNGGOOOOGGGGNN \
NNNNNNOOOOOOONNN \
NNNNNGGGGRGNONNN \
NNNNOGGGGGGOOONN \
NNNOORGGGGGOONNN \
NNNGGRRRRRRRNNNN \
NNNGRRRRRRRRNNNN \
NNGGRRRNRRRNNNNN \
NNGNNNNGGGNNNNNN \
NNNNNNNGGGGNNNNN\
',
'\
NNNNNNRRRRRNNNNN \
NNNNNRRRRRRRRRNN \
NNNNNGGGOOGONNNN \
NNNNGOGOOOGOOONN \
NNNNGOGGOOOGOOON \
NNNNGGOOOOGGGGNN \
NNNNNNOOOOOOONNN \
NNNNNGGRGGGNNNNN \
NNNNGGGGRRGGNNNN \
NNNNGGGRRORRONNN \
NNNNGGGGRRRRRNNN \
NNNNRGGOOORRRNNN \
NNNNNRGOORRRNNNN \
NNNNNRRRGGGNNNNN \
NNNNNGGGGGGGNNNN \
NNNNNGGGGNNNNNNN\
',
'\
NNNNNRRRRRNNNNNN \
NNNGRRRRRRRRNNNN \
NNGGGGGGOGONNNNN \
NOOGOOGOOOOOONNN \
NOOGOOGGOOGGOONN \
NNOOGOOOOOOGGNNN \
NNNRRRGGGROONNNN \
NNRROOOGRRGGGNNN \
NNRGOOOGGGGGGNNN \
NNRRROOGGGGGGNNN \
NNNRRRRRGGGGNNNN \
NNNRGGGRRRRNNNNN \
NNNNGGGGRRRNNNNN \
NGNGRRGGGRNNNNNN \
NGGGGGRNNNNNNNNN \
NNGGGGNNNNNNNNNN\
'
]

class Luigi(Mario):
    colors = {
        'R': (32,32,32),
        'G': (255,64,255),
        'O': (96,160,224),
        'N': (0,0,0)
    }

if __name__ == '__main__':
    mario = Mario()
