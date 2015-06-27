from utils import *
import random as R
import pygame
from pygame.sprite import *



def unit_stuff():
    anim_paths  = ["../assets/friend"+str(i)+".png" for i in range(1,4)]
    anim_surfs  = [pygame.image.load(path) for path in anim_paths]
    group       = Group()
    for i in range(10):
        sprite          = BfUnit(
            anim    = Anim(anim_surfs),
            move    = UnitMove((8, 12)))
        group.add(sprite)
    return group



class Anim:

    def __init__(self, surfs):
        self.surfs  = surfs
        self.index  = 0
        self.delay  = 0.9
        self.__time = 0

    def update(self, dt):
        self.__time = self.__time + dt
        while self.__time > self.delay:
            self.index = (self.index + 1) % len(self.surfs)
            self.__time = self.__time - self.delay

    def image(self):
        return self.surfs[self.index % len(self.surfs)]



class UnitMove:

    def __init__(self, speed):
        import random
        if isinstance(speed, tuple):
            self.speed = random.uniform(*speed)
        else:
            self.speed = speed
        self.pos = 0

    def update(self, dt):
        self.pos = self.pos + self.speed * dt



class BfUnit(Sprite):

    def __init__(self, anim, move):
        super(BfUnit, self).__init__()
        self.anim   = anim
        self.move   = move
        self.image  = self.anim.image()
        self.rect   = self.image.get_rect()

    def update(self, dt):
        self.anim.update(dt)
        self.move.update(dt)
        self.image  = self.anim.image()
        self.rect.x = self.move.pos

    def add_speed(self, v):
        self.move.speed += v

    def add_hp(self, v):
        # TODO do stuff
        pass

    def add_attack(self, v):
        # TODO do stuff
        pass

    def add_range(self, v):
        # TODO do stuff
        pass

class Unit:

    def __init__(self):
        self.pos = 0
        self.speed = 0
        self.hp = 10
        self.attack = 1
        self.range = 0
    
    def update(self, time):
        pass
