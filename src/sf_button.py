import pygame

class SFButton:
    def __init__(self, rect, color, text, text_color):
        self.rect = rect
        self.color = color
        self.text = text
        self.text_color = text_color

    def write_text(self, surface):
        font_size = 14
        font = pygame.font.SysFont(None, font_size)
        this_text = font.render(self.text, 1, self.text_color)
        surface.blit(this_text, ((self.rect[0] + self.rect[2] / 2) - this_text.get_width() / 2, (self.rect[1] + self.rect[3] / 2) - this_text.get_height() / 2))
        return surface

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 0)
        pygame.draw.rect(surface, (190, 190, 190), self.rect, 1)
        return surface

    def is_pressed(self, mouse):
        if self.rect[0] < mouse[0] < (self.rect[0] + self.rect[3]) and self.rect[1] < mouse[1] < (self.rect[1] + self.rect[2]):
            return True
        else:
            return False
