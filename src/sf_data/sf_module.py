class Module:

    type_empty = 0
    type_generator = 1
    type_hp = 2
    type_attack = 3
    type_range = 4

    names = ["empty", "generator", "hp", "attack", "range"]
    workTimes = [0, 0, 1000, 1000, 1000]
    buildTimes = [2000, 10000, 10000, 10000, 10000]
    buildCosts = [0, 10, 100, 100, 100]
    actions = [_action_empty, _action_empty, _action_hp, _action_attack, _action_range]
    maxLevel = [1, 10, 10, 10, 10]
    inputTime = 800
    
    def _action_empty(self, unit):
        pass
    
    def _action_hp(self, unit):
        unit.hp += 10 * self.level
    
    def _action_attack(self, unit):
        unit.attack += 1 * self.level
    
    def _action_range(self, unit):
        unit.range += 5 * self.level
    
    @staticmethod
    def get_build_cost(type):
        return buildCosts[type]
    
    def __init__(self, pos, giveUnitCallback):
        self.pos = pos
        self.giveUnitCallback = giveUnitCallback
        self._dirs = [True, False, False, False]
        self._dirCount = 1
        self._currDir = 0
        self.unit = None
        self.type = 0
        self.buildTimer = 0
        self.workTimer = 0
        self.inputTimer = 0
        self.buildTimerMax = 1
        self.workTimerMax = 1
        self.inputDir = 0
        self.level = 0
    
    def get_type_name(self):
        return Module.names[self.type]
    
    def toggle_target_dir(self, dir):
        if self._dirs[dir]:
            self._dirCount -= 1
        else:
            self._dirCount += 1
        self._dirs[dir] = not self._dirs[dir]
    
    def uses_target_dir(self, dir):
        return self._dirs[dir]
    
    # methods for status
    def is_passive(self):
        return self.type == Module.type_generator
    
    def is_idle(self):
        return not (self.is_passive() or self.unit or self.is_building())
    
    def is_waiting(self):
        return not self.is_passive() and self.inputTimer >= 0
    
    def is_working(self):
        return self.is_passive() or self.workTimer >= 0
    
    def is_building(self):
        return self.buildTimer >= 0
    
    # progress
    def get_input_progress(self):
        if not self.is_waiting():
            return 0
        return (Module.inputTime - self.inputTimer) / Module.inputTime
    
    def get_work_progress(self):
        if not self.is_working():
            return 0
        return (self.workTimer) / self.workTimerMax
    
    def get_build_progress(self):
        if not self.is_building():
            return 0
        return (self.buildTimer) / self.buildTimerMax
    
    # methods for abilities
    def can_build_new(self):
        return self.is_idle() and self.type == Module.type_empty
    
    def can_upgrade(self):
        return self.is_idle() and self.level < Module.maxLevel[self.type]
    
    def can_sell(self):
        return self.is_idle() and self.type != Module.type_empty
    
    def can_receive_unit(self):
        return self.is_idle() and not self.is_passive()
    
    # actions
    def receive_unit(self, unit, dir):
        if not self.can_receive_unit():
            return False
        self.unit = unit
        self.inputDir = dir
        self.inputTimer = Module.inputTime
        self.workTimerMax = Module.workTimes[self.type]
        self.workTimer = self.workTimerMax
        return True
    
    def build_new(self, type):
        if not self.can_build_new() and type != Module.type_empty:
            return False
        self.buildTimerMax = Module.buildTimes[type]
        self.buildTimer = self.buildTimerMax
        self.type = type
        self.level = 1
    
    def upgrade(self, type):
        if not self.can_upgrade():
            return False
        self.buildTimerMax = Module.buildTimes[type]
        self.buildTimer = self.buildTimerMax
        self.type = type
        self.level += 1
    
    def sell(self):
        if not self.can_sell():
            return False
        self.buildTimerMax = Module.buildTimes[Module.type_empty]
        self.buildTimer = self.buildTimerMax
        self.type = Module.type_empty
        self.level = 1
    
    def update(self, time):
        # building the module has priority
        if self.buildTimer > 0:
            self.buildTimer = max(0, self.buildTimer - time)
            return
        # when not building: if we have no unit to work on, do nothing
        if not self.unit:
            return
        if self.inputTimer > 0:
            if time > inputTimer:
                time -= self.inputTimer
                self.inputTimer = 0
            else:
                self.inputTimer -= time
                return
        self.workTimer -= time
        if self.workTimer <= 0:
            self.workTimer = 0
            self._next_dir()
            if giveUnitCallback(self, unit, self._currDir):
                unit = None
    
    def _next_dir(self):
        for x in range(1, 4):
            dir = (self._currDir + x) % 4
            if self._dirs[dir]:
                self._currDir = dir
                return
    