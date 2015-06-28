from utils import *
from pygame.sprite import *
from sf_data.sf_unit import *
from pygame import Rect
from images import *



class Battlefield:

    def __init__(self, rect):
        self.size = 30
        self.first_unit_1 = None
        self.first_unit_2 = None
        self.rect               = Rect(rect)
        self.units_group        = LayeredDirty()
        self.projectile_group   = LayeredDirty()
        self.unit_count_1 = 0
        self.unit_count_2 = 0
        self.draw_offset = 0
        self.draw_scale = 60

    def create_some_units(self):
        for i in range(1):
            unit = self.create_elefant(team = 1)
            self.add_unit(unit)
        for i in range(1):
            unit = self.create_elefant(team = 2)
            self.add_unit(unit)

    def create_elefant(self, team):
        unit        = Unit(
            bf          = self,
            team        = team,
            move        = UnitMove(0, speed = 2),
            anim        = blubb_anim(),
            fight       = UnitFight(damage = 1, range = 5))
        return unit

    def add_unit(self, unit):
        if unit.team == 1:
            unit.move.pos = 0
        if unit.team == 2:
            unit.move.pos = self.size
        unit.bf = self
        self.units_group.add(unit)
    
    def on_kill(self, unit):
        if unit is self.first_unit_1:
            self.first_unit_1 = None
        if unit is self.first_unit_2:
            self.first_unit_2 = None
            unit.kill()
    
    def update(self, dt):
        max1 = -100
        max2 = self.size + 100
        self.first_unit_1 = None
        self.first_unit_2 = None
        self.unit_count_1 = 0
        self.unit_count_2 = 0
        for unit in self.units_group.sprites():
            if unit.team == 1:
                self.unit_count_1 += 1
                if unit.move.pos > max1:
                    max1 = unit.move.pos
                    self.first_unit_1 = unit
            if unit.team == 2:
                self.unit_count_2 += 1
                if unit.move.pos < max2:
                    max2 = unit.move.pos
                    self.first_unit_2 = unit
        
        for unit in self.units_group.sprites():
            unit.update_on_battlefield(dt)
        self.projectile_group.update(dt)

    def draw(self, surface):
        self.units_group.draw(surface)
        self.projectile_group.draw(surface)

    def get_width_percentage(self):
        return self.rect.w / self.draw_scale / self.size

    def get_offset_percentage(self):
        return self.draw_offset / self.size

    def set_window_center(self, c):
        w = self.rect.w / self.draw_scale
        self.draw_offset = min(self.size - w, max(0, c - w / 2))

