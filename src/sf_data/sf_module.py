from utils import *
import sf_data.sf_factory
import config
import pygame
import images

class Module:
    type_empty = 0
    type_generator = 1
    type_hp = 2
    type_attack = 3
    type_range = 4

    def _action_empty(self, unit):
        pass

    def _action_hp(self, unit):
        unit.add_hp(10 * self.level)

    def _action_attack(self, unit):
        unit.add_attack(1 * self.level)

    def _action_range(self, unit):
        unit.add_range(5 * self.level)

    names = ["empty", "generator", "hp", "attack", "range"]
    text_surfaces = None
    work_times = [0, 0, 1, 1, 1]
    build_times = [2, 10, 10, 10, 10]
    build_costs = [0, 10, 100, 100, 100]
    actions = [_action_empty, _action_empty, _action_hp, _action_attack, _action_range]
    max_level = [1, 10, 10, 10, 10]
    input_time = 0.8
    text_color = (220, 220, 250)

    @staticmethod
    def get_build_cost(type):
        return build_costs[type]

    def __init__(self, pos, pass_unit_callback, change_callback, screen_rect):
        self.pos = pos
        self.pass_unit_callback = pass_unit_callback
        self.change_callback = change_callback
        self.screen_rect = screen_rect
        self.screen_mid_point = get_rect_middle(self.screen_rect)
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
        self.level = 1
        self.unit_group = pygame.sprite.Group()
        self.arrow_group = pygame.sprite.Group()
        asurf = images.load_arrows()
        self.arrows = []
        for dir in range(0, 4):
            arrow = pygame.sprite.Sprite()
            arrow.image = asurf[dir]
            arrow.rect = arrow.image.get_rect()
            self.arrows.append(arrow)
        self.arrows[0].rect.center = (screen_rect[0]+screen_rect[2], screen_rect[1] + 0.75*screen_rect[3])
        self.arrows[1].rect.center = (screen_rect[0]+0.75*screen_rect[2], screen_rect[1])
        self.arrows[2].rect.center = (screen_rect[0], screen_rect[1] + 0.25*screen_rect[3])
        self.arrows[3].rect.center = (screen_rect[0]+0.25*screen_rect[2], screen_rect[1] + screen_rect[3])
        self.arrow_group.add(self.arrows[0])
        if not Module.text_surfaces:
            Module.text_surfaces = []
            fontname    = config.app.choose_fontname()
            font        = pygame.font.SysFont(fontname, 15)
            for i in range(0, len(Module.names)):
                s = font.render(Module.names[i], 1, Module.text_color)
                Module.text_surfaces.append(s)

    def get_type_name(self):
        return Module.names[self.type]

    def toggle_target_dir(self, dir):
        if (self.pos[0] == 0 and dir == 2) or \
                (self.pos[1] == 0 and dir == 1) or \
                (self.pos[1] == sf_data.sf_factory.Factory._module_count_y - 1 and dir == 3):
            return
        if self._dirs[dir]:
            self._dir_count -= 1
            self._dirs[dir] = False
            self.arrow_group.remove(self.arrows[dir])
        else:
            self._dir_count += 1
            self._dirs[dir] = True
            self.arrow_group.add(self.arrows[dir])

    def uses_target_dir(self, dir):
        return self._dirs[dir]

    # methods for status
    def is_passive(self):
        return self.type == Module.type_generator

    def is_idle(self):
        return not (self.is_passive() or self.unit or self.is_building())

    def is_waiting(self):
        return not self.is_passive() and self.input_timer > 0

    def is_working(self):
        return self.is_passive() or (self.work_timer > 0 and self.input_timer <= 0)

    def is_building(self):
        return self.build_timer > 0

    # progress
    def get_input_progress(self):
        if not self.is_waiting():
            return 0
        return 1 - self.input_timer / Module.input_time

    def get_work_progress(self):
        if not self.is_working():
            return 0
        return 1 - self.work_timer / self.work_timer_max

    def get_build_progress(self):
        if not self.is_building():
            return 0
        return 1 - self.build_timer / self.build_timer_max

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
        self.unit_group.add(unit)
        self.unit = unit
        self.input_dir = dir
        self.input_timer = Module.input_time
        self.work_timer_max = Module.work_times[self.type]
        self.work_timer = self.work_timer_max
        self.change_callback(self)
        return True

    def build_new(self, type):
        if not self.can_build_new() and type != Module.type_empty:
            return False
        self.build_timer_max = Module.build_times[type]
        self.build_timer = self.build_timer_max
        self.type = type
        self.level = 1
        self.change_callback(self)
        return True

    def upgrade(self):
        if not self.can_upgrade():
            return False
        self.build_timer_max = Module.build_times[self.type]
        self.build_timer = self.build_timer_max
        self.level += 1
        self.change_callback(self)
        return True

    def sell(self):
        if not self.can_sell():
            return False
        self.build_timer_max = Module.build_times[Module.type_empty]
        self.build_timer = self.build_timer_max
        self.type = Module.type_empty
        self.level = 1
        self.change_callback(self)
        return True

    def update(self, time):
        # building the module has priority
        if self.build_timer > 0:
            self.build_timer = max(0, self.build_timer - time)
            if self.build_timer == 0:
                self.change_callback(self)
            return
        # when not building: if we have no unit to work on, do nothing
        if not self.unit:
            return
        self.unit.update_in_factory(time)
        self.unit.rect.center = self.get_unit_screen_pos()
        if self.input_timer > 0:
            if time >= self.input_timer:
                time -= self.input_timer
                self.input_timer = 0
                self.change_callback(self)
            else:
                self.input_timer -= time
                return
        self.work_timer -= time
        if self.work_timer <= 0:
            self.work_timer = 0
            self._next_dir()
            if self.pass_unit_callback(self, self.unit, self._curr_dir):
                self.unit_group.remove(self.unit)
                self.unit = None
                self.change_callback(self)

    def _next_dir(self):
        curr_dir = self._curr_dir or 0
        self._curr_dir = None
        for x in range(1, 5):
            dir = (curr_dir + x) % 4
            if self._dirs[dir]:
                self._curr_dir = dir
                return
    
    def get_unit_screen_pos(self):
        if not self.unit:
            return None
        mid = self.screen_mid_point
        if not self.is_waiting():
            return mid
        dir = get_adjacent_pos((0, 0), self.input_dir)
        r = self.screen_rect
        p = 1 - self.get_input_progress()
        return (mid[0] - dir[0] * p * r[2], mid[1] - dir[1] * p * r[3])
    
    def draw(self, surface):
        self.arrow_group.draw(surface)
        self.unit_group.draw(surface)
    
    def draw_non_sprites(self, surface):
        r = self.screen_rect
        t = Module.text_surfaces[self.type]
        pygame.draw.rect(surface, (0, 0, 0), r, 1)
        surface.blit(t, ((r[0] + r[2] / 2) - t.get_width() / 2,
                        (r[1] + r[3] / 4) - t.get_height() / 2))
        progress = -1
        col = (100, 100, 255)
        if self.is_working() and not self.is_passive():
            progress = self.get_work_progress()
        if self.is_building():
            progress = self.get_build_progress()
            col = Module.text_color
        if progress >= 0:
            b = 4
            h = 6
            pr1 = (r[0]+b, r[1]+r[3]-b-h, r[2]-2*b, h)
            pr2 = (pr1[0], pr1[1], pr1[2]*progress, pr1[3])
            pygame.draw.rect(surface, col, pr1, 1)
            pygame.draw.rect(surface, col, pr2, 0)
    
