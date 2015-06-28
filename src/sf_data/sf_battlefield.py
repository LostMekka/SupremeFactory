from utils import *
from pygame.sprite import *
from sf_data.sf_unit import *
from pygame import Rect
from images import *



class Battlefield:

    def __init__(self, rect):
        self.rect           = Rect(rect)
        self.units_group    = Group()
        self.projectile_group = Group()

    def create_some_units(self):
        for i in range(1):
            unit = self.create_elefant(team = 1)
            self.units_group.add(unit)
        for i in range(1):
            unit = self.create_elefant(team = 2)
            self.units_group.add(unit)

    def create_elefant(self, team):
        start_pos = self.team_start_pos(team)
        unit        = Unit(
            bf          = self,
            team        = team,
            anim        = elefant_anim(),
            move        = UnitMove(start_pos, speed = (8, 12)),
            fight       = UnitFight((5,8), range = 5))
        return unit

    def update(self, dt):
        self.units_group.update(dt)
        self.projectile_group.update(dt)

    def draw(self, surface):
        self.units_group.draw(surface)
        self.projectile_group.draw(surface)

    def floor_y(self):
        return self.rect.y + self.rect.h * 0.9
    
    def team_start_x(self, team):
        return self.rect.x + self.team_start_pos(team)
    
    def team_start_pos(self, team):
        return 0 if team == 1 else 400


'''
First sketch

class BattleField:
    
    def __init__(self):
        self.units = []
        self.size = 1000
        self.fist_unit_1 = None
        self.fist_unit_2 = None
        self.unit_count_1 = 0
        self.unit_count_2 = 0
    
    def add_unit(self, unit):
        self.units.append(unit)
        if unit.team == 1:
            unit.pos = 0
        if unit.team == 2:
            unit.pos = self.size
    
    def remove_unit(self, unit):
        unit.hp = 0
        
    
    def update(self, time):
        for unit in units:
            unit.update(time)
        units[:] = [unit for unit in units if unit.hp <= 0]
        max1 = -100
        max2 = self.size + 100
        self.fist_unit_1 = None
        self.fist_unit_2 = None
        self.unit_count_1 = 0
        self.unit_count_2 = 0
        for unit in units:
            if unit.team == 1:
                self.unit_count_1 += 1
                if unit.pos > max1:
                    max1 = unit.pos
                    self.fist_unit_1 = unit
            if unit.team == 2:
                self.unit_count_2 += 1
                if unit.pos < max2:
                    max2 = unit.pos
                    self.fist_unit_2 = unit
'''
