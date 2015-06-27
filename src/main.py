import pygame, sys
from pygame.locals import *
from sf_tiles import sf_tile

def draw_ui():
    for tile in sf_tile.tiles:
        pygame.draw.rect(DISPLAYSURF, tile.bg_color, tile.rect)

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

