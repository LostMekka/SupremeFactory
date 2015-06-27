import pygame, sys
from pygame.locals import *
from sf_tiles import sf_tile
from sf_data import sf_unit
from utils import *

app = Duct()

def main():
    pygame.init()

    app.display_surface = pygame.display.set_mode((1024, 700))

    pygame.display.set_caption('SupremeFactory!')
    
    app.unit_stuff = sf_unit.unit_stuff()
    
    run_main_loop()

def update_everything():
    dt = 0.016 # TODO
    #update_units_move(dt)
    update_unit_stuff(dt)

def update_unit_stuff(dt):
    app.unit_stuff.update(dt)

def update_units_move(dt):
    for unit in app.units:
        unit.move_forward(dt)

def render_everything():
    surface = app.display_surface
    surface.fill((64, 64, 64))
    #render_units()
    render_unit_stuff()

def render_unit_stuff():
    surface = app.display_surface
    app.unit_stuff.draw(surface)

def render_units():
    surface = app.display_surface
    for unit in app.units:
        color   = (255, 255, 255)
        rect    = (unit.pos, 0, 100, 100)
        pygame.draw.rect(surface, color, rect)

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
