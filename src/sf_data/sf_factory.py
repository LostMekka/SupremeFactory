from utils import *
from sf_data.sf_module import Module

class Factory:
    
    _module_count_x = 4
    _module_count_y = 3
    _unit_creation_time = 5000
    _unit_creation_pos = (0, _module_count_y - 1)
    
    def __init__(self, team, put_unit_callback, screen_rect):
        self.team = team
        self.put_unit_callback = put_unit_callback
        self.unit_count = 0
        self.max_unit_count = 10
        self.modules = []
        self.timer = Factory._unit_creation_time
        w = screen_rect[2] / Factory._module_count_x
        h = screen_rect[3] / Factory._module_count_y
        for y in range(0, Factory._module_count_y-1):
            for x in range(0, Factory._module_count_x-1):
                r = (x*w, y*h, w, h)
                self.modules.append(Module((x, y), self.pass_unit_callback, r))
    
    def pass_unit_callback(self, module, unit, dir):
        if module.pos[1] >= Factory._module_count_x - 1:
            unit.team = self.team
            self.put_unit_callback(unit)
            return True
        next = self.get_adjacent_module(pos, dir)
        if not next or not next.is_idle():
            return False
        next.receive_unit(unit, dir)
        return True
    
    def get_module(self, pos):
        return self.modules[pos[0] + Factory._module_count_x * pos[1]]
    
    def get_adjacent_module(self, pos, dir):
        newpos = get_adjacent_pos(pos, dir)
        if newpos[0] < 0 or pos[1] < 0 or pos[1] >= Factory.module_count_y:
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
                unit = create_larva()
                inmod.receive_unit(unit, 0)
    