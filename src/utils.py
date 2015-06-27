'''
from utils import *
'''

def get_adjacent_pos(pos, dir):
    return {
            0 : (pos[0] + 1, pos[1]),
            1 : (pos[0], pos[1] - 1),
            2 : (pos[0] - 1, pos[1]),
            3 : (pos[0], pos[1] + 1),
        }[dir]

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
