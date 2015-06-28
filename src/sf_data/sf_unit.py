from utils import *
import random as R
import config
import pygame
from pygame.sprite import *
from images import *



def create_larva(team):
    return Unit(
        bf      = None,
        anim    = larva_anim(),
        move    = UnitMove(pos = 0, speed = 0.3),
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
        self.stand = False
    
    def update(self, dt, unit):
        self.__time = max(0, self.__time - dt)
        target = unit.bf.first_unit_2 if unit.team == 1 else unit.bf.first_unit_1
        d = abs(unit.move.pos - target.move.pos) if target else (
                unit.bf.size-unit.move.pos if unit.team == 1 else unit.move.pos)
        mr = 1
        stand_melee = self.range == 0 and d <= mr
        stand_ranged = self.range > 0 and (self.range > d or self.__time > 0)
        self.stand = stand_melee or stand_ranged
        if self.__time == 0 and target:
            if stand_ranged:
                projectile = Projectile(
                    team        = unit.team,
                    damage      = self.damage,
                    start_pos   = unit.move.pos,
                    target      = target,
                    battlefield = unit.bf)
                unit.bf.projectile_group.add(projectile)
                self.__time = self.delay
            elif stand_ranged:
                target.damage(self.damage)
                self.__time = self.delay




class Unit(DirtySprite):

    # 
    # access .rect if you want to draw when .in_factory == True
    #

    def __init__(self, bf, anim, move, fight, team, in_factory = False):
        super(Unit, self).__init__()
        self.in_factory = in_factory
        self.hp     = 10
        self.bf     = bf
        self.anim   = anim
        self.move   = move
        self.drop   = None
        self.fight  = fight
        self.team   = team
        self.dirty = 2
        self.image  = self.anim.image()
        if team == 2:
            self.anim.flip()
        self.rect   = self.image.get_rect()

    def update_in_factory(self, dt):
        self.anim.update(dt)
        self.image  = self.anim.image()
        self.rect.size = self.image.get_rect().size
    
    def update_while_dropping(self, dt):
        self.anim.update(dt)
        self.image  = self.anim.image()
        self.rect.size = self.image.get_rect().size
    
    def update_on_battlefield(self, dt):
        self.anim.update(dt)
        self.fight.update(dt, self)
        if not self.fight.stand:
            self.move.update(dt, self)
        self.image  = self.anim.image()
        self.rect.center = (
            self.bf.rect.x + (self.move.pos - self.bf.draw_offset) * self.bf.draw_scale,
            self.bf.rect.bottom - config.app.floor_height - self.rect.h / 2 + 10
        )
        
    def center(self):
        return self.rect.center
    
    def damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.bf.on_kill(self)
    
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


class Projectile(DirtySprite):

    def __init__(self, damage, start_pos, target, team, battlefield):
        super(Projectile, self).__init__()
        self.bf         = battlefield
        self.damage     = damage
        self.team       = team
        self.pos        = start_pos
        self.start_pos  = start_pos
        self.target     = target
        self.dirty      = 2
        self.image      = projectile_image()
        if team == 2:
            self.image      = pygame.transform.flip(self.image, True, False)
        self.rect       = self.image.get_rect()

    def update(self, dt):
        direction       = 1 if self.team == 1 else -1
        move = 4 * dt
        s = self.pos - self.target.move.pos
        d = self.start_pos - self.target.move.pos
        h = (-s * s / d + s) * direction
        if s * d <= 0:
            self.target.damage(self.damage)
            self.kill()
        self.pos += move * direction
        self.rect.center = (
            self.bf.rect.x + (self.pos - self.bf.draw_offset) * self.bf.draw_scale,
            self.bf.rect.bottom - config.app.floor_height + h*self.bf.draw_scale - 30
        )



def load_projectile_image():
    from pygame.gfxdraw import filled_circle
    try:
        path    = "./assets/projectile2.png"
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
