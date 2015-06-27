import pygame, sys
from pygame.locals import *
from utils import *
from sf_button import SFButton

app = Duct()


def main():
    pygame.init()
    setup_ui()

    app.display_surface = pygame.display.set_mode((1024, 700))

    pygame.display.set_caption('SupremeFactory!')

    run_main_loop()


def update_everything():
    pass


def render_everything():
    draw_ui()


def run_main_loop():
    while True:  # main game loop

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                button_text = check_button_press(mouse_pos)
                if button_text:
                    print(button_text)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        update_everything()
        render_everything()
        pygame.display.update()


def setup_ui():
    base_factory_tile = Duct(bg_color=Colors.dark_gray, rect=(0, 100, 400, 600))
    minimap_tile = Duct(bg_color=Colors.light_gray, rect=(0, 0, 1024, 100))
    visionrect_tile = Duct(bg_color=Colors.white, rect=(5, 5, 140, 90))
    battlefield_tile = Duct(bg_color=Colors.gray, rect=(400, 100, 624, 600))
    app.tiles = [
        base_factory_tile,
        minimap_tile,
        visionrect_tile,
        battlefield_tile
    ]

    app.buttons = []
    app.buttons.append(SFButton((50, 600, 100, 50), Colors.green, "FOR THE BUTTON!", Colors.white))


def draw_ui():
    surface = app.display_surface

    for tile in app.tiles:
        pygame.draw.rect(surface, tile.bg_color, tile.rect)

    for button in app.buttons:
        button.draw(surface)
        button.write_text(surface)


def draw_tile(tile):
    surface = app.display_surface
    pygame.draw.rect(surface, tile.bg_color, tile.rect)

def check_button_press(mouse_pos):
    for button in app.buttons:
        if button.is_pressed:
            return button.text

if __name__ == "__main__":
    main()
