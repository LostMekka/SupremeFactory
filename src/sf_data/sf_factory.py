from utils import *
import sf_data.sf_module
import pygame
import math

class Factory:
    
    _module_count_x = 4
    _module_count_y = 3
    _unit_creation_time = 3
    _unit_creation_pos = (0, _module_count_y - 1)
    
    def __init__(self, team, put_unit_callback, module_change_callback, screen_rect):
        self.team = team
        self.put_unit_callback = put_unit_callback
        self.screen_rect = screen_rect
        self.hp = 1000
        self.unit_count = 0
        self.max_unit_count = 10
        self.modules = []
        self.timer = Factory._unit_creation_time
        self.timer = 0
        w = screen_rect[2] / Factory._module_count_x
        h = screen_rect[3] / Factory._module_count_y
        for y in range(0, Factory._module_count_y):
            for x in range(0, Factory._module_count_x):
                rx1 = math.floor(screen_rect[0] + x * w)
                ry1 = math.floor(screen_rect[1] + y * h)
                rx2 = math.floor(screen_rect[0] + (x + 1) * w)
                ry2 = math.floor(screen_rect[1] + (y + 1) * h)
                r = (rx1, ry1, rx2-rx1, ry2-ry1)
                self.modules.append(sf_data.sf_module.Module((x, y), 
                        self.pass_unit_callback,  module_change_callback, r))
    
    def pass_unit_callback(self, module, unit, dir):
        if module.pos[0] >= Factory._module_count_x - 1 and dir == 0:
            self.put_unit_callback(unit)
            return True
        next = self.get_adjacent_module(module.pos, dir)
        if not next or not next.is_idle():
            return False
        next.receive_unit(unit, dir)
        return True
    
    def get_module(self, pos):
        return self.modules[pos[0] + Factory._module_count_x * pos[1]]
    
    def get_adjacent_module(self, pos, dir):
        newpos = get_adjacent_pos(pos, dir)
        if newpos[0] < 0 or newpos[1] < 0 or \
                newpos[0] >= Factory._module_count_x or \
                newpos[1] >= Factory._module_count_y:
            return None
        return self.get_module(newpos)
    
    def get_unit_list(self):
        units = []
        for module in self.modules:
            if module.unit:
                units.append(module.unit)
        return units
    
    def get_unit_pos(self, unit):
        for module in self.modules:
            if module.unit and module.unit is unit:
                if(not module.is_waiting()):
                    return module.pos
                dir = get_adjacent_pos((0, 0), module.input_dir)
                p = module.get_input_progress() - 1
                return (module.pos[0] + dir[0] * p, module.pos[1] + dir[1] * p)
        return None
    
    def update(self, time):
        for module in self.modules:
            module.update(time)
        if self.timer > 0:
            self.timer -= time
        if self.timer <= 0 and self.unit_count < self.max_unit_count:
            inmod = self.get_module(Factory._unit_creation_pos)
            if inmod.is_idle():
                self.timer += Factory._unit_creation_time
                unit = sf_data.sf_unit.create_larva(self.team)
                inmod.receive_unit(unit, 0)
    
    def draw(self, surface):
        pygame.draw.rect(surface, (35, 35, 40), self.screen_rect, 0)
        for m in self.modules:
            m.draw_non_sprites(surface)
        for m in self.modules:
            m.draw(surface)
    
