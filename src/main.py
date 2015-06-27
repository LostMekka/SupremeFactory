import pygame, sys
from pygame.locals import *
from sf_tiles import sf_factory, sf_minimap, sf_battlefield

factory_tile = sf_factory.Factory()
minimap_tile = sf_minimap.Minimap()
battlefield_tile = sf_battlefield.Battlefield()

def draw_ui():
    pygame.draw.rect(DISPLAYSURF, factory_tile.bg_color, factory_tile.rect)
    pygame.draw.rect(DISPLAYSURF, minimap_tile.bg_color, minimap_tile.rect)
    pygame.draw.rect(DISPLAYSURF, battlefield_tile.bg_color, battlefield_tile.rect)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1024, 700))
pygame.display.set_caption('Hello World!')

draw_ui()

while True:  # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

