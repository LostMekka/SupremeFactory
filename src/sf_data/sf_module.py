class Module:

    type_empty = 0
    type_generator = 1
    type_hp = 2
    type_attack = 3
    type_range = 4

    names = ["empty", "generator", "hp", "attack", "range"]
    work_times = [0, 0, 1000, 1000, 1000]
    build_times = [2000, 10000, 10000, 10000, 10000]
    build_costs = [0, 10, 100, 100, 100]
    actions = [_action_empty, _action_empty, _action_hp, _action_attack, _action_range]
    max_level = [1, 10, 10, 10, 10]
    input_time = 800
    
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
        return build_costs[type]
    
    def __init__(self, pos, pass_unit_callback):
        self.pos = pos
        self.pass_unit_callback = pass_unit_callback
        self._dirs = [True, False, False, False]
        self._dir_count = 1
        self._curr_dir = 0
        self.unit = None
        self.type = 0
        self.build_timer = 0
        self.work_timer = 0
        self.input_timer = 0
        self.build_timer_max = 1
        self.work_timer_max = 1
        self.input_dir = 0
        self.level = 0
    
    def get_type_name(self):
        return Module.names[self.type]
    
    def toggle_target_dir(self, dir):
        if (pos[0] == 0 and dir == 2) or \
        (pos[1] == 0 and dir == 1) or \
        (pos[1] == Factory.module_count_y - 1 and dir == 3):
            return;
        if self._dirs[dir]:
            self._dir_count -= 1
            self._dirs[dir] = False;
        else:
            self._dir_count += 1
            self._dirs[dir] = True;
    
    def uses_target_dir(self, dir):
        return self._dirs[dir]
    
    # methods for status
    def is_passive(self):
        return self.type == Module.type_generator
    
    def is_idle(self):
        return not (self.is_passive() or self.unit or self.is_building())
    
    def is_waiting(self):
        return not self.is_passive() and self.input_timer >= 0
    
    def is_working(self):
        return self.is_passive() or self.work_timer >= 0
    
    def is_building(self):
        return self.build_timer >= 0
    
    # progress
    def get_input_progress(self):
        if not self.is_waiting():
            return 0
        return (Module.input_time - self.input_timer) / Module.input_time
    
    def get_work_progress(self):
        if not self.is_working():
            return 0
        return (self.work_timer) / self.work_timer_max
    
    def get_build_progress(self):
        if not self.is_building():
            return 0
        return (self.build_timer) / self.build_timer_max
    
    # methods for abilities
    def can_build_new(self):
        return self.is_idle() and self.type == Module.type_empty
    
    def can_upgrade(self):
        return self.is_idle() and self.level < Module.max_level[self.type]
    
    def can_sell(self):
        return self.is_idle() and self.type != Module.type_empty
    
    def can_receive_unit(self):
        return self.is_idle() and not self.is_passive()
    
    # actions
    def receive_unit(self, unit, dir):
        if not self.can_receive_unit():
            return False
        self.unit = unit
        self.input_dir = dir
        self.input_timer = Module.input_time
        self.work_timer_max = Module.work_times[self.type]
        self.work_timer = self.work_timer_max
        return True
    
    def build_new(self, type):
        if not self.can_build_new() and type != Module.type_empty:
            return False
        self.build_timer_max = Module.build_times[type]
        self.build_timer = self.build_timer_max
        self.type = type
        self.level = 1
    
    def upgrade(self, type):
        if not self.can_upgrade():
            return False
        self.build_timer_max = Module.build_times[type]
        self.build_timer = self.build_timer_max
        self.type = type
        self.level += 1
    
    def sell(self):
        if not self.can_sell():
            return False
        self.build_timer_max = Module.build_times[Module.type_empty]
        self.build_timer = self.build_timer_max
        self.type = Module.type_empty
        self.level = 1
    
    def update(self, time):
        # building the module has priority
        if self.build_timer > 0:
            self.build_timer = max(0, self.build_timer - time)
            return
        # when not building: if we have no unit to work on, do nothing
        if not self.unit:
            return
        if self.input_timer > 0:
            if time > input_timer:
                time -= self.input_timer
                self.input_timer = 0
            else:
                self.input_timer -= time
                return
        self.work_timer -= time
        if self.work_timer <= 0:
            self.work_timer = 0
            self._next_dir()
            if pass_unit_callback(self, unit, self._curr_dir):
                unit = None
    
    def _next_dir(self):
        for x in range(1, 4):
            dir = (self._curr_dir + x) % 4
            if self._dirs[dir]:
                self._curr_dir = dir
                return
    