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
    
        