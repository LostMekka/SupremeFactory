import pygame
from pygame.transform import *

#
# call load_arrows() and get a tuple with the for arrows right, up, left, down
#

def cached(f):
    def ff():
        try:
            return f.cache
        except:
            f.cache = f()
            return f.cache
    return ff

@cached
def load_arrow():
    path    = "./assets/arrow_top.png"
    return pygame.image.load(path)

@cached
def load_arrows():
    image = load_arrow()
    arrows  = (
        rotate(image, 270),
        image,
        rotate(image, 90),
        rotate(image, 180))
    return arrows

@cached
def load_elefant_surfaces():
    anim_paths  = ["./assets/friend"+str(i)+".png" for i in range(1,4)]
    anim_surfs  = [pygame.image.load(path) for path in anim_paths]
    return anim_surfs

@cached
def load_larva_surfaces():
    anim_paths  = ["./assets/larva"+str(i)+".png" for i in range(1,4)]
    anim_surfs  = [pygame.image.load(path) for path in anim_paths]
    return anim_surfs

if __name__ == "__main__":
    load_arrows()
    load_elefant_surfaces()
    load_larva_surfaces()
