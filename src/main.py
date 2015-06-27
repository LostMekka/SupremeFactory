import pygame, sys
from pygame.locals import *
from sf_tiles import sf_tile
from utils import *

app = Duct()

def main():
    pygame.init()

    app.display_surface = pygame.display.set_mode((1024, 700))

    pygame.display.set_caption('SupremeFactory!')
    
    run_main_loop()

def update_everything():
    pass

def render_everything():
    pass

def run_main_loop():
    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        update_everything()
        render_everything()
        pygame.display.update()

def draw_ui():
    surface = app.display_surface
    for tile in sf_tile.tiles:
        draw_tile(tile)

def draw_tile(tile):
    surface = app.display_surface
    pygame.draw.rect(surface, tile.bg_color, tile.rect)

if __name__ == "__main__":
    main()
