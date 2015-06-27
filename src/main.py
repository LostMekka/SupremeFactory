import pygame, sys
from pygame.locals import *
from utils import *
from sf_button import SFButton

class App(Duct):
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

    def setup_ui(self):
        self.main_font = pygame.font.SysFont(None, 24)
        self.tiles = Duct(
            factory_tile = Duct(bg_color=Colors.dark_gray, rect=(0, 100, 400, 600)),
            minimap_tile = Duct(bg_color=Colors.light_gray, rect=(0, 0, 1024, 100)),
            visionrect_tile = Duct(bg_color=Colors.white, rect=(5, 5, 140, 90)),
            battlefield_tile = Duct(bg_color=Colors.gray, rect=(400, 100, 624, 600))
        )
        self.buttons = []
        self.buttons.append(
            SFButton((50, 600, 100, 50), Colors.green, "FOR THE BUTTON!", Colors.white, self.on_button_press)
        )
        self.labels = []
        self.labels.append(self.main_font.render("Modul 1", 1, Colors.white))

    def draw_mouse_pos(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        self.basic_font = pygame.font.SysFont(None, 48)
        text_surf = basic_font.render("X: " + str(mouse_x) + " Y:" + str(mouse_y), True, Colors.black)
        text_rect = text_surf.get_rect()
        text_rect.center = ((mouse_x + 10), mouse_y)
        self.display_surface.blit(text_surf, text_rect)

    def draw_ui(self):
        surface = self.display_surface
        for tile in self.tiles.values():
            pygame.draw.rect(surface, tile.bg_color, tile.rect)

        for button in self.buttons:
            button.draw(surface)
            button.write_text(surface)

        for label in self.labels:
            surface.blit(label, (170, 500))

        # draw_mouse_pos()

    def draw_tile(self, tile):
        surface = self.display_surface
        pygame.draw.rect(surface, tile.bg_color, tile.rect)

    def on_mouse_down(self, pos):
        for button in self.buttons:
            if button.press_if_inside(pos):
                return button.text
            else:
                return None

    def on_mouse_up(self, pos):
        pass
    
    def on_button_press(self, button):
        print("button pressed!")

def main():
    global app
    pygame.init()
    app = App()
    app.setup_ui()
    app.display_surface = pygame.display.set_mode((1024, 700))
    pygame.display.set_caption('SupremeFactory!')
    app.run_main_loop()

if __name__ == "__main__":
    main()
