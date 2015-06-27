import pygame, sys
from pygame.locals import *
from sf_tiles import sf_tile
from utils import Colors 

def draw_ui():
    for tile in sf_tile.tiles:
        pygame.draw.rect(DISPLAYSURF, tile.bg_color, tile.rect)
		
def drawMousePos():	
    (mouseX, mouseY) = pygame.mouse.get_pos()
    TextSurf = basicFont.render("X: "+str(mouseX)+" Y:" + str(mouseY), True, Colors.black)
    TextRect= TextSurf.get_rect()
    TextRect.center = ((mouseX+10),(mouseY))
    DISPLAYSURF.blit(TextSurf, TextRect)		

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1024, 700))
pygame.display.set_caption('Hello World!')
basicFont = pygame.font.SysFont(None, 48)

while True:  # main game loop
    draw_ui()
    drawMousePos()
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()	
    pygame.display.update()
	
