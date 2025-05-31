from random import randint


RANDOM = -1
RED = 255


def random_color():
    B = randint(0, 255)
    G = randint(0, 255)
    R = randint(0, 255)
    return B * 65536 + G * 256 + R
