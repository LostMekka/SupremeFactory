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
        rotate(image, 270), # right
        image,              # up
        rotate(image, 90),  # left
        rotate(image, 180)) # down
    return arrows

@cached
def load_elefant_surfaces():
    paths  = ["./assets/friend"+str(i)+".png" for i in range(1,4)]
    surfs  = [pygame.image.load(path) for path in paths]
    return surfs

@cached
def load_larva_surfaces():
    paths  = ["./assets/larva"+str(i)+".png" for i in range(1,4)]
    surfs  = [pygame.image.load(path) for path in paths]
    surfs.append(surfs[1])
    return surfs

@cached
def load_blubb_surfaces():
    paths  = ["./assets/blubb"+str(i)+".png" for i in range(1,6)]
    surfs  = [pygame.image.load(path) for path in paths]
    surfs.append(surfs[1])
    return surfs

@cached
def load_empty():
    return pygame.image.load("./assets/empty_blank.png")

@cached
def load_speed():
    return pygame.image.load("./assets/speed_blank.png")

@cached
def load_attack():
    return pygame.image.load("./assets/swords_blank.png")

@cached
def load_hp():
    return pygame.image.load("./assets/heart_blank.png")

@cached
def load_range():
    return pygame.image.load("./assets/range_blank.png")
    return load_empty()

@cached
def load_generator():
    return pygame.image.load("./assets/power_blank.png")



class Anim:

    def __init__(self, surfs, delay):
        self.surfs  = surfs
        self.index  = 0
        self.delay  = 0.2
        self.__time = 0

    def update(self, dt):
        self.__time = self.__time + dt
        while self.__time > self.delay:
            self.index = (self.index + 1) % len(self.surfs)
            self.__time = self.__time - self.delay

    def image(self):
        return self.surfs[self.index % len(self.surfs)]
    
    def flip(self):
        from pygame.transform import flip
        self.surfs = [flip(surf, True, False) for surf in self.surfs]

def larva_anim():
    return Anim(
        surfs   = load_larva_surfaces(),
        delay   = 0.2)

def elefant_anim():
    return Anim(
        surfs   = load_elefant_surfaces(),
        delay   = 0.8)

def blubb_anim():
    return Anim(
        surfs   = load_blubb_surfaces(),
        delay   = 0.5)



if __name__ == "__main__":
    load_arrows()
    load_elefant_surfaces()
    load_larva_surfaces()
