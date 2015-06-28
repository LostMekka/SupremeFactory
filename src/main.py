import pygame, sys
from pygame.locals import *
from utils import *
from sf_button import SFButton
from sf_data.sf_factory import Factory
from sf_data.sf_module import Module
import config

class Frame:
    def __init__(self, l_color, bg_color, rect):
        self.rect = rect
        self.l_color = l_color
        self.bg_color = bg_color
        
    def draw(self, surface):
        if self.bg_color:
            pygame.draw.rect(surface, self.bg_color, self.rect, 0)
        if self.l_color:
            pygame.draw.rect(surface, self.l_color, self.rect, 1)


class App(Duct):

    def __init__(self):
        self.drag_start = None
        self.selected_module = None

    def update_everything(self):
        pass

    def render_everything(self):
        self.draw_ui()

    def run_main_loop(self):
        while True:  # main game loop
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.on_mouse_down(pygame.mouse.get_pos())
                if event.type == MOUSEBUTTONUP:
                    self.on_mouse_up(pygame.mouse.get_pos())

                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
            self.update_everything()
            self.render_everything()
            pygame.display.update()

    def choose_fontname(self):
        fonts   = pygame.font.get_fonts()
        wants   = "freesansbold liberationmono".split()
        for font in wants:
            if font in fonts:
                return font
        return None

    def setup_ui(self):
        fontname        = self.choose_fontname()
        self.main_font  = pygame.font.SysFont(fontname, 24)
        w = self.size[0]
        h = self.size[1]
        mh = 100
        ih = 200
        fw = 400
        bw = w - fw
        self.frames = Duct(
            minimap_frame = Frame(Colors.black, Colors.light_gray, (0, 0, w, mh)),
            factory_frame = Frame(Colors.black, (70,70,70), (0, mh, fw, h-mh-ih)),
            buttons_frame = Frame(Colors.black, (50,50,50), (0, h-ih, fw, ih)),
            battlefield_frame = Frame(Colors.black, (150,150,150), (fw, mh, bw, h-mh-ih)),
            info_frame = Frame(Colors.black, (100,100,100), (fw, h-ih, bw, ih))
        )
        self.minimap_height = mh
        self.factory_width = fw
        self.battlefield_width = bw
        self.info_height = ih
        
        bh = 20
        mn = 4
        n = mn + 3
        sh = (ih - n * bh) / (n + 1)
        self.build_buttons = []
        self.buttons = Duct()
        def getrekt(i):
            return (fw / 2, h - ih + sh + (i - 1) * (bh + sh), fw / 2 - sh, bh)
        for t in range(1, mn+1):
            text = "Build: " + Module.names[t]
            btn = SFButton(getrekt(t), None, text, None, self.on_build_press, t)
            self.buttons[text] = btn
            self.build_buttons.append(btn)
        self.buttons.upgrade = SFButton(getrekt(mn+1.5), None, "Upgrade", None, self.on_upgrade_press, None)
        self.buttons.sell = SFButton(getrekt(mn+3), None, "Sell", None, self.on_sell_press, None)
        self.select_module(None)
        
        self.labels = []
        #self.labels.append(self.main_font.render("Modul 1", 1, Colors.white))

    def new_game(self):
        self.factory1 = Factory(1, self.on_put_unit, self.frames.factory_frame.rect)

    def draw_mouse_pos(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        fontname        = self.choose_fontname()
        self.basic_font = pygame.font.SysFont(fontname, 48)
        text_surf = basic_font.render("X: " + str(mouse_x) + " Y:" + str(mouse_y), True, Colors.black)
        text_rect = text_surf.get_rect()
        text_rect.center = ((mouse_x + 10), mouse_y)
        self.display_surface.blit(text_surf, text_rect)

    def draw_ui(self):
        surface = self.display_surface
        for frame in self.frames.values():
            frame.draw(surface)

        for button in self.buttons.values():
            button.draw(surface)

        for label in self.labels:
            surface.blit(label, (170, 500))

        # draw_mouse_pos()

    def select_module(self, module):
        self.selected_module = module
        if(module):
            for b in self.build_buttons:
                if module.can_build_new():
                    b.set_available()
                else:
                    b.set_unavailable()
            if module.can_upgrade():
                self.buttons.upgrade.set_available()
            else:
                self.buttons.upgrade.set_unavailable()
            if module.can_sell():
                self.buttons.sell.set_available()
            else:
                self.buttons.sell.set_unavailable()
        else:
            for b in self.build_buttons:
                b.set_deactivated()
            self.buttons.upgrade.set_deactivated()
            self.buttons.sell.set_deactivated()

    def on_mouse_down(self, pos):
        # hit a module? if yes, select it and start drag
        module = None
        for m in self.factory1.modules:
            if is_point_in_rect(pos, m.screen_rect):
                module = m
                break
        if module:
            self.select_module(module)
            self.drag_start = pos
            return
        # no module clicked. maybe a button?
        button = None
        for b in self.buttons.values():
            if b.is_inside(pos):
                button = b
                break
        if button:
            button.press()

    def on_mouse_up(self, pos):
        if self.drag_start and self.selected_module:
            dx = pos[0] - self.drag_start[0]
            dy = pos[1] - self.drag_start[1]
            min = 10
            if dx*dx + dy*dy > min*min:
                dir = -1
                if abs(dx) > abs(dy):
                    if dx > 0:
                        dir = 0
                    else:
                        dir = 2
                else:
                    if dy > 0:
                        dir = 3
                    else:
                        dir = 1
                self.selected_module.toggle_target_dir(dir)
        self.drag_start = None
    
    def on_build_press(self, type):
        print("build ", type, " pressed!")
    
    def on_upgrade_press(self, object):
        print("upgrade pressed!")
        
    def on_sell_press(self, object):
        print("sell pressed!")
    
    def on_put_unit(self, unit):
        # TODO: insert unit
        pass

def main():
    pygame.init()
    app = App()
    config.app = app
    app.size = (1000, 700)
    app.setup_ui()
    app.new_game()
    app.display_surface = pygame.display.set_mode(app.size)
    pygame.display.set_caption('SupremeFactory!')
    app.run_main_loop()

if __name__ == "__main__":
    main()
