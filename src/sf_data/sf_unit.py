from utils import *
import random as R
import pygame
from pygame.sprite import *



def unit_stuff():
    anim_paths  = ["../assets/friend"+str(i)+".png" for i in range(1,4)]
    anim_surfs  = [pygame.image.load(path) for path in anim_paths]
    unit_group       = Group()
    for i in range(10):
        sprite          = BfUnit(
            anim    = Anim(anim_surfs),
            move    = UnitMove((8, 12)),
            fight   = UnitFight((5,8), range))
        unit_group.add(sprite)
    return unit_group



def elefant_surfaces():
    anim_paths  = ["../assets/friend"+str(i)+".png" for i in range(1,4)]
    anim_surfs  = [pygame.image.load(path) for path in anim_paths]
    return anim_surfs

elefant_surfaces = elefant_surfaces()



def create_larva():
    return create_elefant()


def create_elefant():
    sprite          = BfUnit(
        anim    = Anim(elefant_surfaces),
        move    = UnitMove(5))
    return sprite


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
        
class UnitFight:
    delay  = 4.9
    __time = 0
    projectile_group = Group()
    
    def __init__(self, damage, range):
        import random
        self.range = range
        if isinstance(damage, tuple):
            self.damage = random.uniform(*damage)
        else:
            self.damage = damage
        
    def update(self, dt, unit):
        self.__time = self.__time + dt
        while self.__time > self.delay:
            if(self.range != 0):
                projectile = Projectile(self.damage, unit.move.pos, 820)
                self.projectile_group.add(projectile)
            else:
                pass 
            # TODO Nahkampf
            self.__time = self.__time - self.delay
            


class Unit(Sprite):

    def __init__(self, anim, move, fight):
        super(BfUnit, self).__init__()
        self.anim   = anim
        self.move   = move
        self.fight  = fight
        self.image  = self.anim.image()
        self.rect   = self.image.get_rect()

    def update(self, dt):
        self.anim.update(dt)
        self.fight.update(dt, self)
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


class Projectile(Sprite):
    
    def __init__(self, damage, start, dest):
        super(Projectile, self).__init__()
        self.damage = damage
        self.start = start
        self.dest=dest
        self.img_path = "../assets/projectile.png"
        self.img = pygame.image.load(self.img_path)
        self.rect=self.img.get_rect()
  
