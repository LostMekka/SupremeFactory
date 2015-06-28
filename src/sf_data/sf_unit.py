from utils import *
import random as R
import pygame
from pygame.sprite import *
from images import *



def create_larva(team):
    return Unit(
        bf      = None,
        anim    = larva_anim(),
        move    = UnitMove(pos = 0, speed = 8),
        fight   = UnitFight(damage = 1, range = 0),
        team    = team,
        in_factory = True)



class UnitMove:

    def __init__(self, pos, speed):
        import random
        if isinstance(speed, tuple):
            self.speed = random.uniform(*speed)
        else:
            self.speed = speed
        self.pos = pos

    def update(self, dt, unit):
        direction   = 1 if unit.team == 1 else -1
        self.pos    = self.pos + self.speed * dt * direction
        
class UnitFight:

    def __init__(self, damage, range):
        import random
        self.range = range
        self.damage = damage
        self.delay  = 4
        self.__time = 0
        
    def update(self, dt, unit):
        self.__time = self.__time + dt
        while self.__time > self.delay:
            if self.range != 0:
                projectile = Projectile(
                    team        = unit.team,
                    damage      = self.damage,
                    start_xy    = unit.rect.center,
                    start_pos   = unit.move.pos)
                unit.bf.projectile_group.add(projectile)
            else:
                pass # TODO Nahkampf
            self.__time = self.__time - self.delay




class Unit(Sprite):

    # 
    # access .rect if you want to draw when .in_factory == True
    #

    def __init__(self, bf, anim, move, fight, team, in_factory = False):
        super(Unit, self).__init__()
        self.in_factory = in_factory
        self.bf     = bf
        self.anim   = anim
        self.move   = move
        self.fight  = fight
        self.team   = team
        self.image  = self.anim.image()
        if team == 2:
            self.anim.flip()
        self.rect   = self.image.get_rect()

    def update_in_factory(self, dt):
        self.anim.update(dt)
        self.image  = self.anim.image()
        self.rect.size = self.image.get_rect().size
    
    def update_on_battlefield(self, dt):
        self.anim.update(dt)
        self.fight.update(dt, self)
        self.move.update(dt, self)
        self.image  = self.anim.image()
        self.rect.x = self.move.pos + self.bf.rect.x
        self.rect.y = self.bf.floor_y() - self.rect.h
    
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

    def __init__(self, damage, start_xy, start_pos, team):
        super(Projectile, self).__init__()
        self.damage     = damage
        self.team       = team
        self.xy         = start_xy
        self.pos        = start_pos
        self.image      = projectile_image()
        self.rect       = self.image.get_rect()

    def update(self, dt):
        direction       = 1 if self.team == 1 else -1
        x, y            = self.xy
        self.xy         = (x + 180 * dt * direction, y)
        self.rect.topleft = self.xy



def load_projectile_image():
    from pygame.gfxdraw import filled_circle
    try:
        path    = "./assets/projectile.png"
        image   = pygame.image.load(path)
        return image
    except: # TODO put some PNG there
        flags   = pygame.HWSURFACE | pygame.SRCALPHA
        surf    = pygame.Surface((16, 16), flags)
        filled_circle(surf, 8, 8, 7, (255, 255, 255))
        return surf

def projectile_image():
    try:
        return projectile_image.cache
    except:
        projectile_image.cache = load_projectile_image()
        return projectile_image.cache
