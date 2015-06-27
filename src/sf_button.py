import pygame
from utils import *

class SFButton:
    def __init__(self, rect, color, text, text_color, callback):
        self.rect = rect
        self.color = color
        self.text = text
        self.text_color = text_color
        self.callback = callback

    def write_text(self, surface, font_size=14):
        """
        Writes the buttons text to the given surface (like draw(), only for the text).
        Font size defaults to 14.
        :param surface:
        :param font_size:
        :return:
        """
        font = pygame.font.SysFont(None, font_size)
        this_text = font.render(self.text, 1, self.text_color)
        surface.blit(this_text, ((self.rect[0] + self.rect[2] / 2) - this_text.get_width() / 2,
                                 (self.rect[1] + self.rect[3] / 2) - this_text.get_height() / 2))
        return surface

    def draw(self, surface):
        """
        Draws the button to the given surface.
        :param surface:
        :return:
        """
        pygame.draw.rect(surface, self.color, self.rect, 0)
        pygame.draw.rect(surface, (190, 190, 190), self.rect, 1)
        return surface
    
    def press(self):
        self.callback(self)
    
    def is_inside(self, point):
        return is_point_in_rect(mouse, self.rect)
    
    def press_if_inside(self, mouse):
        """
        Calls callback and returns true if the given mouse (x,y) is within the button's bounds
        :param mouse:
        :return:
        """
        if is_point_in_rect(mouse, self.rect):
            self.press()
            return True
        return False

    def calc_module_pos(self, pos):
        """
        Returns a rect for a module position for a given position of said module.
        :param pos:
        :return:
        """
        offset_x = 50
        offset_y = 150
        module_size = 150

        return offset_x + (pos[0] * module_size), offset_y + (pos[1] * module_size), module_size, module_size
