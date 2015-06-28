import pygame
from pygame.transform import *

#
# call arrows() and get a tuple with the for arrows right, up, left, down
#

def load_arrow():
    path    = "./assets/arrow_top.png"
    return pygame.image.load(path)

def load_arrows():
    image = arrow()
    arrows  = (
        rotate(image, 270),
        image,
        rotate(image, 90),
        rotate(image, 180))
    return arrows

def arrow():
    try: return arrow.cache
    except:
        arrow.cache = load_arrow()
        return arrow.cache

def arrows():
    try: return arrows.cache
    except:
        arrows.cache = load_arrows()
        return arrows.cache

if __name__ == "__main__":
    arrows()
