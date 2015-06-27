'''
from utils import *
'''


class Duct(dict):
    '''
    duck = Duct(voice = "quack", mass = 0.6)
    assert duck.voice, "quack"
    duck.spam = "ham"
    '''

    def __getattr__(self, k):
        return self[k]

    def __setattr__(self, k, v):
        self[k] = v


Colors = Duct(
    white=(255, 255, 255),
    light_gray=(200, 200, 200),
    gray=(150, 150, 150),
    black = (0, 0, 0),
    red = (255, 0, 0),
    blue = (0, 0, 255),
    dark_gray=(50, 50, 50),
    green=(20, 200, 20)
)
