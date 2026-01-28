import pygame
import re

def bound(x, lower, upper):
    return min(max(x, lower), upper)

# def get_object_types():
#     object_types = []
#     with open('global_object_list.txt', 'r') as f:
#         for line in f:
#             line = line.strip()
#             line = re.sub(r'\d+ ', '', line)
#             object_types.append(line)
#     return object_types


pygame.init()
pygame.display.set_caption("Perypetie Boba")

frameWidth = 1200
frameHeight = 700


# IN GAME

gridSize = 50

grid_width = int(frameWidth / gridSize)
grid_height = int(frameHeight / gridSize)

screen = pygame.display.set_mode((frameWidth, frameHeight))

# object_types = []
# object_types = get_object_types()


import os, os.path
num_files = len([name for name in os.listdir('Projects')])


# IN EDITOR

pixel_size = 40

num_blocks_horizontally = 24
num_blocks_vertically = 14

right_toolbar_width = 100
right_toolbar_space = 20

border_x, border_y = pixel_size, pixel_size

# real dimensions of the level in pixels in the editor
real_width = num_blocks_horizontally * pixel_size
real_height = num_blocks_vertically * pixel_size


def render_text_inside_rect(text, rect, color=(0,0,0)):
    w = rect[2]
    h = rect[3]
    w1 = 9999
    h1 = 9999
    current_size = 150
    while w1 > w or h1 > h:
        current_size -= 10
        font = pygame.font.SysFont('Arial', current_size)
        text_surface = font.render(text, True, color)
        _, _, w1, h1 = text_surface.get_rect()


def get_perfect_font_size(text, rect):
    w = rect[2]
    h = rect[3]
    w1 = 9999
    h1 = 9999
    current_size = 50
    while w1 > w or h1 > h:
        current_size -= current_size // 10
        font = pygame.font.SysFont('Arial', current_size)
        text_surface = font.render(text, True, (0, 0, 0))
        _, _, w1, h1 = text_surface.get_rect()
    return current_size