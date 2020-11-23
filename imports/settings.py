import pygame
WW,WH = 1200,720

# Font
tiny_font = pygame.font.Font('Roboto-Thin.ttf', 24)
small_font = pygame.font.Font('Roboto-Thin.ttf', 32)
medium_font = pygame.font.Font('Roboto-Thin.ttf', 48)
big_font = pygame.font.Font('Roboto-Thin.ttf', 64)
GRAVITY = 350
FPS = 60

def game_font_generator(size):
    return pygame.font.Font('Roboto-Thin.ttf', size)


#################   General Settings    #################
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
L_BLUE = (0, 255, 255)
PINK = (255, 0, 255)
PURPLE = (148, 0, 211)
GRAY = (100, 100, 100)
