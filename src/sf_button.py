import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from utils import *
import config



class SFButton:
    def __init__(self, rect, color, text, text_color, callback, callback_object):
        self.rect = rect
        self.color = color
        self.text = text
        self.text_color = text_color
        self.callback = callback
        self.callback_object = callback_object
        self.active = True
        
        self.bg_sprite          = Sprite()
        self.bg_sprite.rect     = Rect(rect)
        self.bg_sprite.layer    = 1
        self.label_sprite       = Sprite()
        self.label_sprite.rect  = Rect(rect)
        self.label_sprite.layer = 2
        
        self.set_available() # trigger .render

    def sprites(self):
        return self.bg_sprite, self.label_sprite

    def set_available(self):
        self.color = (0, 50, 0)
        self.text_color = (0, 255, 0)
        self.active = True
        self.render()

    def set_unavailable(self):
        self.color = (50, 0, 0)
        self.text_color = (255, 0, 0)
        self.active = False
        self.render()

    def set_deactivated(self):
        self.color = (0, 50, 0)
        self.text_color = (150, 150, 150)
        self.active = False
        self.render()

    def render_bg(self):
        rect    = Rect(self.rect)
        rect.topleft = (0, 0)
        color   = self.color
        surf    = pygame.Surface(rect.size)
        pygame.draw.rect(surf, color, rect, 0)
        pygame.draw.rect(surf, (190, 190, 190), rect, 1)
        self.bg_sprite.image = surf
        self.bg_sprite.rect  = self.rect
    
    def render_label(self):
        rect    = Rect(self.rect)
        fontname    = config.app.choose_fontname()
        font_size   = 14
        text_color  = self.text_color
        text        = self.text
        font        = pygame.font.SysFont(fontname, font_size)
        surf        = font.render(text, 1, text_color)
        self.label_sprite.image         = surf
        self.label_sprite.rect.size     = surf.get_rect().size
        self.label_sprite.rect.center   = rect.center
    
    def render(self):
        self.render_bg()
        self.render_label()
    
    def press(self):
        if self.active:
            if self.callback_object:
                self.callback(self.callback_object)
            else:
                self.callback(self)
    
    def is_inside(self, point):
        return is_point_in_rect(point, self.rect)
    
    def press_if_inside(self, point):
        """
        Calls callback and returns true if the given mouse (x,y) is within the button's bounds
        :param mouse:
        :return:
        """
        if is_point_in_rect(point, self.rect):
            if self.active:
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
