from unicodedata import name
import pygame
import random
import numpy as np
from drawing import *

import os, os.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from button import Button

# from game_settings import num_blocks_vertically

pygame.init()
pygame.display.set_caption("Pixel Art Studio")

frameWidth = 1200
frameHeight = 700 + 50

frame_center_x = frameWidth // 2
frame_center_y = frameHeight // 2

BG_COLOR = (30, 30, 60)




gridSize = 25
gridSize = 25

pixel_size = 25

real_object_size = pixel_size * gridSize

screen = pygame.display.set_mode((frameWidth, frameHeight))


border_x, border_y = frame_center_x - real_object_size // 2, frame_center_y - real_object_size // 2 - 50

offset_x = 12
offset_y = 13


mousex, mousey = pygame.mouse.get_pos()



# global current_color
current_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


object_x, object_y = 0, 0

def update_mouse_coords_on_object():
    global object_x, object_y
    return object_x, object_y

coords_on_object = update_mouse_coords_on_object()

color_size = 64

def draw_color(x, y, color, size=color_size):
    rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(screen, color, rect)

def draw_bar(x, y, color, thickness=4, color_idx=0):
    single_color = current_color[color_idx]
    percent = (single_color / 255) * 100
    width = int(percent / 100 * color_size)

    rect = pygame.Rect(x, y - thickness + color_size, width, thickness)
    pygame.draw.rect(screen, color, rect)

pixels = [[(0, 0, 0) for _ in range(gridSize)] for _ in range(gridSize)]




def draw_border(x, y, thickness):
    rect1 = pygame.Rect(x - thickness, y - thickness, real_object_size + thickness * 2, thickness)
    rect2 = pygame.Rect(x - thickness, y + real_object_size, real_object_size + thickness * 2, thickness)

    rect3 = pygame.Rect(x - thickness, y - thickness, thickness, real_object_size + thickness * 2)
    rect4 = pygame.Rect(x + real_object_size, y - thickness, thickness, real_object_size + thickness * 2)

    pygame.draw.rect(screen, (255, 255, 255), rect1)
    pygame.draw.rect(screen, (255, 255, 255), rect2)
    pygame.draw.rect(screen, (255, 255, 255), rect3)
    pygame.draw.rect(screen, (255, 255, 255), rect4)

def draw_canvas():
    global pixels
    start_x, start_y = border_x + offset_x, border_y + offset_y
    if len(pixels) != gridSize or len(pixels[0]) != gridSize:
        pixels = [[(0, 0, 0) for _ in range(gridSize)] for _ in range(gridSize)]
    #print(start_x, start_y)
    for y in range(gridSize):
        for x in range(gridSize):
            rect = pygame.Rect(pixel_size * x + start_x, y * pixel_size + start_y, pixel_size, pixel_size)
            pygame.draw.rect(screen, pixels[y][x], rect)
            #pygame.draw.rect(screen, (50, y * 10, x * 10), rect)

def in_zone(x, y, width, height=None):
    if height is None:
        height = width
    if mousex >= x and mousex <= x + width:
        #print('siema')
        if mousey >= y and mousey <= y + height:
            #print('SIEMANO')
            return True
    return False

rgb_x = 20
rgb_y = frameHeight - 200

in_zone(rgb_x, rgb_y, color_size)

scroll_up, scroll_down = False, False
mouse_pressed_LB = False
mouse_pressed_RB = False
arrow_pressed = False



# NARZEDZIA DO RYSOWANIA

def fill(x, y, color, tolerance=0):
    max_diff = max(int(255 * (tolerance / 100)), 1)
    fringe = []
    visited = [(x, y)]
    result = [(x, y)]

    x1 = x - 1
    x2 = x + 1
    y1 = y - 1
    y2 = y + 1

    x1 = np.clip(x1, 0, gridSize - 1)
    x2 = np.clip(x2, 0, gridSize - 1)
    y1 = np.clip(y1, 0, gridSize - 1)
    y2 = np.clip(y2, 0, gridSize - 1)

    if (x1, y) not in visited and (x1, y) not in fringe:
        fringe.append((x1, y))
    if (x2, y) not in visited and (x2, y) not in fringe:
        fringe.append((x2, y))
    if (x, y1) not in visited and (x, y1) not in fringe:
        fringe.append((x, y1))
    if (x, y2) not in visited and (x, y2) not in fringe:
        fringe.append((x, y2))

    while fringe:
        current_x, current_y = fringe.pop(0)
        visited.append((current_x, current_y))
        current_color = pixels[current_y][current_x]
        if all(abs(current_color[i] - color[i]) <= max_diff for i in range(3)):
            result.append((current_x, current_y))

            x1 = current_x - 1
            x2 = current_x + 1
            y1 = current_y - 1
            y2 = current_y + 1

            x1 = np.clip(x1, 0, gridSize - 1)
            x2 = np.clip(x2, 0, gridSize - 1)
            y1 = np.clip(y1, 0, gridSize - 1)
            y2 = np.clip(y2, 0, gridSize - 1)

            if (x1, current_y) not in visited and (x1, current_y) not in fringe:
                fringe.append((x1, current_y))
            if (x2, current_y) not in visited and (x2, current_y) not in fringe:
                fringe.append((x2, current_y))
            if (current_x, y1) not in visited and (current_x, y1) not in fringe:
                fringe.append((current_x, y1))
            if (current_x, y2) not in visited and (current_x, y2) not in fringe:
                fringe.append((current_x, y2))

    return result

def get_color_variation(color, variation_percent):
    r, g, b = color
    variation_amount = int(255 * (variation_percent / 100))

    r_variation = random.randint(-variation_amount, variation_amount)
    g_variation = random.randint(-variation_amount, variation_amount)
    b_variation = random.randint(-variation_amount, variation_amount)

    r_new = np.clip(r + r_variation, 0, 255)
    g_new = np.clip(g + g_variation, 0, 255)
    b_new = np.clip(b + b_variation, 0, 255)

    return (r_new, g_new, b_new)

# from game_settings import num_blocks_vertically
num_blocks_vertically = 14

def draw_line2(p1, p2, color=current_color):
    x1, y1 = p1
    x2, y2 = p2

    num_blocks_vertically = 14

    y1 = gridSize - y1
    y2 = gridSize - y2

    p1 = (x1, y1)
    p2 = (x2, y2)

    left_x = min(x1, x2)
    right_x = max(x1, x2)

    upper_y = min(y1, y2)
    lower_y = max(y1, y2)

    if x2 == x1:
        return
    a = (y2 - y1) / (x2 - x1) if x2 >= x1 else (y1 - y2) / (x1 - x2)
    b = y1 - a * x1

    # print(f'linia z {p1} do {p2}, y = {a}x + {b}')

    for x in range(abs(x1 - x2)):

        current_x = left_x + x
        y1 = int(a * current_x + b)
        for y in range(abs(upper_y - lower_y)):
            current_y = gridSize - (upper_y + y)
            dist = abs(current_y - y1)
#print(f'pkt ({current_x}, {current_y}), dystans do linii: {dist}', end='')
            # dist = abs(y2 - y1)
            if dist <= 2:
        # y = int(a * x + b)
                # draw_canvas()
                use_brush(current_x, current_y, color=color)

def draw_line(p1, p2, color=current_color):
    x1, y1 = p1
    x2, y2 = p2
    
    y1 = frameHeight - y1
    y2 = frameHeight - y2

    p1 = (x1, y1)
    p2 = (x2, y2)
    left_x = min(x1, x2)
    right_x = max(x1, x2)
    lower_y = min(y1, y2)

    if x2 == x1:
        return
    a = (y2 - y1) / (x2 - x1) if x2 >= x1 else (y1 - y2) / (x1 - x2)
#print(a)

    for x_offset in range(right_x - left_x):
        current_x = left_x + x_offset * gridSize
        y_on_line = int(a * current_x + y1)
#print(y_on_line, (y_on_line - offset_y - border_y )// pixel_size)
        for y_offset in range(-2, 3):
            current_y = y_on_line + y_offset
            object_x = int((current_x - border_x - offset_x) // pixel_size)
            object_y = int((current_y - border_y - offset_y) // pixel_size)
            use_brush(object_x, object_y, color=color)

current_history_id = 0
history = [current_color]



def same_as_neighbors(x, y, min_neighbors_count=4, tolerance=0):
    max_diff = max(int(255 * (tolerance / 100)), 1)
    cur_col = pixels[y][x]

    adjacent_pixels_colors = []
    adjacent_pixels_colors.append((pixels[y-1][x] if y > 0 else cur_col))  # North
    adjacent_pixels_colors.append((pixels[y+1][x] if y < gridSize - 1 else cur_col))  # South
    adjacent_pixels_colors.append((pixels[y][x-1] if x > 0 else cur_col))  # West
    adjacent_pixels_colors.append((pixels[y][x+1] if x < gridSize - 1 else cur_col))  # East


    # print(x,y, adjacent_pixels_colors, cur_col)

    num_same = 0
    
    for col in adjacent_pixels_colors:
        if all([abs(col[i] - cur_col[i]) <= max_diff for i in range(3)]):
            # print(x,y,col, cur_col)
            num_same += 1

    return num_same >= min_neighbors_count


def same_as_neighbors_diagonally(x, y, min_neighbors_count=4, tolerance=0):
    max_diff = max(int(255 * (tolerance / 100)), 1)
    cur_col = pixels[y][x]

    adjacent_pixels_colors = []

    adjacent_pixels_colors.append((pixels[y-1][x-1] if y > 0 and x > 0 else cur_col))  # North-West
    adjacent_pixels_colors.append((pixels[y-1][x+1] if y > 0 and x < gridSize - 1 else cur_col))  # North-East
    adjacent_pixels_colors.append((pixels[y+1][x-1] if y < gridSize - 1 and x > 0 else cur_col))  # South-West
    adjacent_pixels_colors.append((pixels[y+1][x+1] if y < gridSize - 1 and x < gridSize - 1 else cur_col))  # South-East

    num_same = 0

    for col in adjacent_pixels_colors:
        if all([abs(col[i] - cur_col[i]) <= max_diff for i in range(3)]):
            num_same += 1

    return num_same >= min_neighbors_count


def get_outline(x, y, bg_color=(0,0,0), color=current_color):
    global pixels
    if not pixels:
        pixels = [[(0, 0, 0) for _ in range(gridSize)] for _ in range(gridSize)]
    bg_color=pixels[y][x]

    adjacent_pixels_colors = []
    adjacent_pixels_colors.append((pixels[y-1][x] if y > 0 else None))  # North
    adjacent_pixels_colors.append((pixels[y+1][x] if y < gridSize - 1 else None))  # South
    adjacent_pixels_colors.append((pixels[y][x-1] if x > 0 else None))  # West
    adjacent_pixels_colors.append((pixels[y][x+1] if x < gridSize - 1 else None))  # East

    # adjacent_pixels_colors2 = [col for idx, col in enumerate(adjacent_pixels_colors) if col in adjacent_pixels_colors[:idx] + adjacent_pixels_colors[idx+1:]]
    if not same_as_neighbors(x, y, min_neighbors_count=1):
        return None
    

    fringe = []
    visited = [(x, y)]
    result = [(x, y)]
    dir_offsets = [ (0, -1), (0, 1), (-1, 0), (1, 0) ]

    def add_neighbors_if_adjacent(x, y, visited=visited, fringe=fringe):
        fringeq = []
        for idx, (dx, dy) in enumerate(dir_offsets):
            nx, ny = x + dx, y + dy
            if nx >= 0 and nx < gridSize and ny >= 0 and ny < gridSize:
                if pixels[ny][nx] == bg_color and not same_as_neighbors_diagonally(nx, ny) and (nx, ny) not in visited:# (nx, ny) not in visited and (nx, ny) not in fringe:
                    fringeq.append((nx, ny))

        return fringeq
    
    fringe = [(x, y)]
    iter = 0
    while fringe:
        current_x, current_y = fringe.pop(0)
        visited.append((current_x, current_y))
        result.append((current_x, current_y))
        # current_color = pixels[current_y][current_x]
        fringe.extend(add_neighbors_if_adjacent(current_x, current_y, visited))
        iter += 1
        if iter > 1000:
            print()

    return result



def draw_history():
    start_x = frameWidth - 60
    start_y = frameHeight - 60
    space = 20
    history_size = 20
    border_size = 4
    adder_current_border_size = 2
    used_border_size = border_size + adder_current_border_size
    history_len = len(history)
    history_bar_size = 10
    deco_subtraction = 12

    toolbar_bg_color = (20, 20, 20)
    history_bar_color = (30, 30, 30)
    used_bar_color = (255, 255, 255)
    deco_color = (0, 0, 0)


    global toolbar_x_start, toolbar_y_start, toolbar_width, toolbar_height
    toolbar_x_start = (start_x - (history_len - 1) * (history_size + space) - history_bar_size)
    toolbar_y_start = start_y - history_bar_size
    toolbar_width = history_size + history_bar_size * 2 + (history_len - 1) * (history_size + space)
    toolbar_height = history_size + history_bar_size * 2

    pygame.draw.rect(screen, toolbar_bg_color, (toolbar_x_start, toolbar_y_start, toolbar_width, toolbar_height))

    for i in range(history_len):
        x = start_x - i * (history_size + space)
        y = start_y


        rect = pygame.Rect(x, y, history_size, history_size)
        rect_bg = pygame.Rect(x - border_size , y - border_size, history_size + border_size * 2, history_size + border_size * 2)
        if i != 0 or True:
            pygame.draw.rect(screen, history_bar_color, rect_bg)
            pygame.draw.rect(screen, history[-i-1], rect)
        if i == len(history) - 1:
            x = start_x - current_history_id * (history_size + space)
            y = start_y

            # rect_bg.x = start_x - border_size - adder_current_border_size
            # rect_bg.y = start_y - border_size - adder_current_border_size
            
            rect = pygame.Rect(x, y, history_size, history_size)
            rect_bg = pygame.Rect(x - border_size - adder_current_border_size, y - border_size - adder_current_border_size, history_size + border_size * 2 + adder_current_border_size * 2, history_size + border_size * 2 + adder_current_border_size * 2)
            rect_deco_horizontal = pygame.Rect(rect_bg.x + deco_subtraction, rect_bg.y, rect_bg.width - (deco_subtraction * 2), used_border_size)
            rect_deco_vertical = pygame.Rect(rect_bg.x, rect_bg.y + deco_subtraction, used_border_size, rect_bg.height - (deco_subtraction * 2))
            
            pygame.draw.rect(screen, used_bar_color, rect_bg)

            pygame.draw.rect(screen, deco_color, rect_deco_horizontal)
            pygame.draw.rect(screen, deco_color, rect_deco_vertical)

            rect_deco_horizontal.y += history_size + used_border_size
            rect_deco_vertical.x += history_size + used_border_size
            pygame.draw.rect(screen, deco_color, rect_deco_horizontal)
            pygame.draw.rect(screen, deco_color, rect_deco_vertical)

            rect_bg = pygame.Rect(rect.x - border_size , rect.y - border_size, history_size + border_size * 2, history_size + border_size * 2)
            pygame.draw.rect(screen, history_bar_color, rect_bg)
            pygame.draw.rect(screen, history[-1 - current_history_id], rect)


def remove_duplicates():
    all_removed = False
    while not all_removed:
        all_removed = True
        for i, color in enumerate(history):
            if color in history[i+1:]:
                history.pop(i)
                all_removed = False


start_x = offset_x + border_x
start_y = offset_y + border_y

def draw_bar2(x, y, dir, thick_percent=20):
    thickness = int((thick_percent / 100) * pixel_size)
    rect = pygame.Rect(x, y, pixel_size, thickness)

    if dir == 'n':
        return rect

    elif dir == 'e':
        rect.width = thickness
        rect.height = pixel_size
        rect.x += gridSize - thickness

    elif dir == 'w':
        rect.width = thickness
        rect.height = pixel_size

    elif dir == 's':
        rect.y = rect.y + pixel_size - thickness

    return rect
    # return pygame.draw.rect(screen, (255, 255, 255), rect)


def draw_selection(p1, p2, thickness, color=(255, 255, 255)):
    x1, y1 = p1
    x2, y2 = p2

    left_x = min(x1,x2) * pixel_size + start_x
    right_x = max(x1,x2) * pixel_size + start_x

    upper_y = min(y1,y2) * pixel_size + start_y
    lower_y = max(y1,y2) * pixel_size + start_y

    upper = [draw_bar2(left_x + x * pixel_size, upper_y, 'n') if x%2==0 else None for x in range(abs(x2 - x1))]# if x%2==0 else None]
#print(upper)
    
    lower = [draw_bar2(left_x + x * pixel_size, lower_y, 's') if x%2==0 else None for x in range(abs(x2 - x1))]# if x%2==0 else None]
    left = [draw_bar2(left_x, upper_y + y * pixel_size, 'w') if y%2==0 else None for y in range(abs(y2 - y1))]# if y%2==0 else None]
    right = [draw_bar2(right_x, upper_y + y * pixel_size, 'e') if y%2==0 else None  for y in range(abs(y2 - y1) + 1)]# if y%2==0 else None]

    all = upper + lower + left + right

    for rect in all:
        if rect is not None:
            pygame.draw.rect(screen, color, rect)
#print(rect)

    

#print('\n\n\n')

    return all

class User:
    def get_current_toolbar(self):
        if self.LMB_toolbar.mouse_in_zone():
            return -1
        if self.RMB_toolbar.mouse_in_zone():
            return 1
        return 0
    
    def update_current_toolbar(self):
        self.current_toolbar = self.get_current_toolbar()
        
    
    def __init__(self):
        self.LMB_binded_tool = 'brush'
        self.RMB_binded_tool = 'fill'
        
        self.tool_index_LMB = 0
        self.tool_index_RMB = 1

        

        self.LMB_toolbar = None
        self.RMB_toolbar = None

        self.mouse_toolbars = [self.LMB_toolbar, self.RMB_toolbar]

        self.current_toolbar = 0 # -1 LMB, 1 RMB, 0 none

        self.settings_mode = False


        self.grip_point = None
        self.current_point = None

        self.is_selecting = False
        self.current_selection = (None, None)

    def update(self):
        self.update_current_toolbar()
        self.mouse_toolbars = [self.LMB_toolbar, self.RMB_toolbar]
        pass

    def change_tool(self, direction):
        toolbar_index = int((user.current_toolbar + 1) / 2)  # we make sure we map -1 to 0 and 1 to 1
        self.mouse_toolbars[toolbar_index].selected_index += direction
        self.mouse_toolbars[toolbar_index].selected_index = np.clip(self.mouse_toolbars[toolbar_index].selected_index, 0, len(self.mouse_toolbars[toolbar_index].tools) - 1)
        

user = User()

global coll
coll = (0,0,0)


TOOL_SIZE = 64
BORDER_SIZE = 4


class Tool:
    def __init__(self, name, icon_path, quick_buttons_names=[]):
        self.name = name
        self.icon_path = icon_path
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.scale(self.icon, (150, 150))

        self.parent_toolbar = None

        self.x = 0
        self.y = 0

        self.is_selected = False

        self.quick_buttons_names = quick_buttons_names
        self.quick_buttons = []
        
        


    def set_position(self):
        index = self.parent_toolbar.tools.index(self)
        self.x = self.parent_toolbar.x + self.parent_toolbar.border_size
        self.y = self.parent_toolbar.y + self.parent_toolbar.border_size + index * (self.parent_toolbar.tool_size + self.parent_toolbar.border_size)



        self.icon = pygame.transform.scale(self.icon, (self.parent_toolbar.tool_size, self.parent_toolbar.tool_size))
        # why -4? but the border for toolbar is all it is, theres no other border for tool


        if not self.quick_buttons_names:
            return
        
        all_buttons_width = 100
        num_buttons = len(self.quick_buttons_names)
        qbutton_width = int(all_buttons_width / num_buttons)

        for idx, name in enumerate(self.quick_buttons_names):
            button = Button(self.x + TOOL_SIZE + BORDER_SIZE + idx * qbutton_width, self.y, name, width=qbutton_width, height=TOOL_SIZE + BORDER_SIZE)
            self.quick_buttons.append(button)


        
        


    def draw(self, x, y):
        screen.blit(self.icon, (x, y))
        if self.is_selected:
            pygame.draw.rect(screen, (255, 255, 255), (x - 2, y - 2, self.parent_toolbar.tool_size + 4, self.parent_toolbar.tool_size + 4), 2)
        
            for qbutton in self.quick_buttons:
                qbutton.draw()
        #pygame.draw.rect(screen, (255, 255, 255), (x, y, 32, 32), 2)

    def use(self):
        if user.settings_mode:
            return
        global current_color
        if self.name == 'brush':
            use_brush(object_x, object_y, current_color)

        elif self.name == 'fill':
            for x, y in fill(object_x, object_y, pixels[object_y][object_x], tolerance=fill_panel.object.properties[1].value):
                if fill_panel.object.properties[0].value == 1:
                    pixels[y][x] = current_color
                else:
                    variation_percent = fill_panel.object.properties[2].value
                    varied_color = get_color_variation(current_color, variation_percent)
                    pixels[y][x] = varied_color if random.randint(1, 100) <= fill_panel.object.properties[3].value else current_color

        elif self.name == 'picker':
            current_color = pixels[object_y][object_x]
            if history[-1] != current_color:
                history.append(current_color)
                if len(history) > 20:
                    history.pop(0)
                current_history_id = 0

        elif self.name == 'selection':
            if user.grip_point is None:
                user.grip_point = coords_on_object

            p1, p2 = (user.grip_point, update_mouse_coords_on_object())
            user.current_selection = (p1, p2)

            return draw_selection(p1, p2, thickness=4, color=coll)

        elif self.name == 'line':
            user.current_point = coords_on_object
            draw_line(user.grip_point, user.current_point)

def create_tools():
    tools = []
    tools.append(Tool('brush', 'icons/brush.jpg'))
    tools.append(Tool('fill', 'icons/fill.jpg'))
    tools.append(Tool('picker', 'icons/picker3.jpg'))
    tools.append(Tool('selection', 'icons/hand2.jpg', ['Wyłącz zaznaczenie']))
    # tools.append(Tool('line', 'icons/brush.jpg'))
    return tools

toolset1 = create_tools()
toolset2 = create_tools()


class Toolbar:
    def generate_tool_y_positions(self):
        pos1 = self.border_size
        distance = self.tool_size + self.border_size
        return [pos1 + i * distance for i in range(len(self.tools))]
    
    def __init__(self, x, y, toolset=toolset1):
        self.x = x
        self.y = y

        self.tool_size = TOOL_SIZE
        self.border_size = BORDER_SIZE
        self.tools = toolset

        for tool in self.tools:
            tool.parent_toolbar = self

        self.tool_y_positions = self.generate_tool_y_positions()

        for tool in self.tools:
            tool.set_position()

        self.selected_index = 0 if user.mouse_toolbars[0] == self else 1

        self.width = self.tool_size + self.border_size * 2
        self.height = self.tool_size * len(self.tools) + self.border_size * (len(self.tools) + 1)

    def mouse_in_zone(self):
        if in_zone(self.x, self.y, self.width, self.height):
            return True
        return False

    def draw(self):
        self.update_selected_tool()
        pygame.draw.rect(screen, (20, 20, 20), (self.x, self.y, self.width, self.height))
        for tool in self.tools:
            tool.draw(tool.x, tool.y)

    def update_selected_tool(self):
        for tool in self.tools:
            tool.is_selected = False
            self.tools[self.selected_index].is_selected = True

    def handle_buttons(self):
        selected = self.tools[self.selected_index]
        qbuttons = selected.quick_buttons
        for qbutton in qbuttons:
            qbutton.update(mousex, mousey, mouse_pressed_LB)



def use_brush(object_x, object_y, color=current_color,):
    if object_x >= 0 and object_x < gridSize:
        if object_y >= 0 and object_y < gridSize:
            pixels[object_y][object_x] = color

toolbar1 = Toolbar(120, border_y + 20, toolset=toolset1)
toolbar2 = Toolbar(1020, border_y + 20, toolset=toolset2)



user.LMB_toolbar = toolbar1
user.RMB_toolbar = toolbar2



class ObjectProperty:
    def __init__(self, name, initial_value=0, min_value=0, max_value=999, controlled_by=None, is_text=False, is_bool=False, negate_control=False):
        self.name = name
        self.initial_value = initial_value
        self.value = initial_value
        self.min_value = min_value
        self.max_value = max_value

        self.is_text = is_text
        self.is_bool = is_bool

        self.controlled_by = controlled_by
        self.enabled = True
        self.negate_control = negate_control if controlled_by is not None else False

    def set_value(self, new_value):
        if not self.is_text:
            if new_value >= self.min_value and new_value <= self.max_value:
                self.value = new_value
        else:
            self.value = new_value

    def get_text_value(self):
        if self.is_bool:
            return 'Yes' if self.value else 'No'
        return str(self.value)
    
    def update_enabled(self):
        if self.controlled_by is not None:
            self.enabled = self.controlled_by.value == (1 - self.negate_control) 

class ObjectWithProperties:
    def __init__(self, name, properties=None):
        self.name = name
        self.properties = properties if properties is not None else []

    def add_property(self, property):
        self.properties.append(property) if isinstance(property, list) else self.properties.extend(property)
        # how to check if property is type list?
        # 

    def num_properties(self):
        return len(self.properties)
    
    def update_properties_enabled(self):
        for prop in self.properties:
            prop.update_enabled()


props = [
    ObjectProperty('Sprite Name', initial_value='MySprite', is_text=True),
    ObjectProperty('Sprite Width', initial_value=50, min_value=1, max_value=500),
    ObjectProperty('Sprite Height', initial_value=100, min_value=1, max_value=500),
    ObjectProperty('Frames Per Animation', initial_value=8, min_value=1, max_value=10),
    ObjectProperty('Number of Animations', initial_value=1, min_value=1, max_value=100),
    ObjectProperty('Is Transparent', initial_value=0, min_value=0, max_value=1, is_bool=True),
]

sprite_sheet_config = ObjectWithProperties('SpriteSheet Configuration (In Progressi)', props)



fill_props = [
    ObjectProperty('Classic Fill', initial_value=1, min_value=0, max_value=1, is_bool=True),
]

fill_props.extend([
    ObjectProperty('Tolerance %', initial_value=0, min_value=0, max_value=100, controlled_by=fill_props[0], negate_control=True),
    ObjectProperty('Color Variation %', initial_value=0, min_value=0, max_value=100, controlled_by=fill_props[0], negate_control=True),
    ObjectProperty('Chance of Variation %', initial_value=100, min_value=0, max_value=100, controlled_by=fill_props[0], negate_control=True),
])



fill_config = ObjectWithProperties('Fill Tool \nConfig', fill_props)


panels = []

class PropertiesPanel:
    def __init__(self, object_with_properties):
        self.object = object_with_properties

        self.scale = 1.5
        self.update_dimensions()
        panels.append(self)

        self.last_pos = (self.x, self.y)

        self.title_offset = (0,0)

    def update(self):
        self.object.update_properties_enabled()

    def update_dimensions(self, pos=True):
        if pos:
            self.x = int(100 * self.scale)
            self.y = int(50 * self.scale)



        self.padding1 = int(5 * self.scale)
        self.padding2 = int(10 * self.scale)
        self.title_height = int(40 * self.scale)



        self.property_size = int(100 * self.scale)

        self.button_bar_height = int(60 * self.scale) - self.padding2

        self.width = self.padding1 * 2 + self.padding2 + (self.property_size + self.padding2) * (self.object.num_properties() - 1)
        self.height = self.title_height + self.padding1 * 2 + (self.property_size + self.padding2 * 2) * 2 + self.button_bar_height


        
        self.button_height = int(self.button_bar_height - self.padding2 * 2)
        self.button_width = int(self.width - self.padding1 * 2)


        self.save_button = Button(self.x + self.width // 2 - self.button_width // 2, self.y + self.height - self.button_bar_height // 2 - self.button_height // 2, 'Save', self.button_width, self.button_height)

        self.new_spritesheet_button = Button(self.x + self.width - self.padding1 - 50, self.y + self.padding1, '+', 50, 50)


        self.col1 = (20, 20, 20)
        self.col2 = (40, 40, 40)
        self.bg_color = (40, 40, 50)
        self.text_color = (255, 255, 255)


        self.bar_width = self.padding2 + (self.property_size + self.padding2) * (self.object.num_properties() - 1)

        # RECTS

        current_y = self.y
        

        self.r1 = pygame.Rect(self.x, self.y, self.width, self.height - self.padding2)

        current_y += self.title_height + self.padding1

        self.r2 = pygame.Rect(self.x + self.padding1, current_y + self.padding1, self.bar_width, self.height - self.title_height - self.padding1 * 2 - self.padding2 - self.button_bar_height)

        current_y += self.padding1

        self.option_rects = []

        self.option_rects.append(pygame.Rect(self.r2.x + self.padding2, current_y + self.padding2, self.bar_width - (self.padding2 * 2), self.property_size))
        
        current_y += self.property_size + self.padding2

        for i in range(self.object.num_properties() - 1):
            self.option_rects.append(pygame.Rect(self.x + self.padding1 + self.padding2 + i * (self.property_size + self.padding2), current_y + self.padding2, self.property_size, self.property_size))


        current_y += self.property_size + self.padding2 * 2

        self.save_button.y = current_y + self.button_bar_height // 2 - self.button_height // 2

        self.font1 = pygame.font.SysFont('Arial', 16)
        self.font2 = pygame.font.SysFont('Arial', 24)
        self.font3 = pygame.font.SysFont('Arial', 32)


        


    def draw(self, title_offset=(0,0)):
        pygame.draw.rect(screen, self.bg_color, self.r1)
        title_surf = self.font2.render(self.object.name, True, self.text_color)
        
        screen.blit(title_surf, (self.x + self.width // 2 - title_surf.get_width() // 2 - self.title_offset[0], self.y + self.title_height // 2 - title_surf.get_height() // 2 + self.padding1))

        pygame.draw.rect(screen, self.col1, self.r2)

        for i, prop in enumerate(self.object.properties[0:]):
            color1 = [0,0,0]
            color1[0] = self.col2[0] - (not prop.enabled) * 20
            color1[1] = self.col2[1] - (not prop.enabled) * 20
            color1[2] = self.col2[2] - (not prop.enabled) * 20
            color1 = tuple(color1)

            option_rect = self.option_rects[i]
            pygame.draw.rect(screen, color1, option_rect)

            prop_name_surf = self.font1.render(prop.name, True, self.text_color)
            screen.blit(prop_name_surf, (option_rect.x + option_rect.width // 2 - prop_name_surf.get_width() // 2, option_rect.y + 4))

            prop_value_surf = self.font3.render(str(prop.get_text_value()), True, self.text_color)
            screen.blit(prop_value_surf, (option_rect.x + option_rect.width // 2 - prop_value_surf.get_width() // 2, option_rect.y + option_rect.height // 2 - prop_value_surf.get_height() // 2))

        self.draw_selected()
        self.save_button.draw()
        self.new_spritesheet_button.draw()

    def draw_selected(self):
        prop = self.get_property_mouse_is_over()
        if prop is not None:
            idx = self.object.properties.index(prop)
            option_rect = self.option_rects[idx]
            pygame.draw.rect(screen, (255, 255, 255), (option_rect.x - 2, option_rect.y - 2, option_rect.width + 4, option_rect.height + 4), 2)


    def get_property_mouse_is_over(self):
        for i, option_rect in enumerate(self.option_rects):
            if in_zone(option_rect.x, option_rect.y, option_rect.width, option_rect.height):
                return self.object.properties[i]
        return None
    
    def save_properties(self):
        result = ''
        for prop in self.object.properties:
            result += f'{prop.value}\n'

        with open(f'spritesheet_config.txt', 'w') as f:
            f.write(result)

    def load_properties(self):
        if not os.path.exists(f'spritesheet_config.txt'):
            return
        with open(f'spritesheet_config.txt', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if i < len(self.object.properties):
                    prop = self.object.properties[i]
                    if prop.is_text:
                        prop.set_value(line.strip())
                    else:
                        prop.set_value(int(line.strip()))

                    


sprite_sheet_panel = PropertiesPanel(sprite_sheet_config)


fill_panel = PropertiesPanel(fill_config)


fill_panel.x = 10
fill_panel.scale = 1.2

fill_panel.padding1 += 2
fill_panel.title_offset = (35, 0)


sprite_sheet_panel.x = 500

for panel in panels:
    panel.update_dimensions()

class Sprite:
    def __init__(self, name='sprite', animation_id=0, width=50, height=100):
        self.name = name

        self.animation = None

        # self.animation_id = animation_id
        self.current_version = 1
        
        self.width = width
        self.height = height

        self.bg_color = (255, 230, 255)

        self.pixels = []
        self.init_pixels()

        self.is_blank = True

    def init_pixels(self):
        pixels = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.bg_color)
            pixels.append(row)

        self.pixels = pixels

    def change_pixel(self, x, y, color):
        if x >= 0 and x < self.width:
            if y >= 0 and y < self.height:
                self.pixels[y][x] = color
                if color != self.bg_color:
                    self.is_blank = False

    def update_all_pixels(self, new_pixels):
        self.pixels = new_pixels
        self.is_blank = False

    def is_blank(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.pixels[y][x] != self.bg_color:
                    return False
        return True

class Animation:    
    def __init__(self, sprite_sheet, name='animation'):
        self.name = name
        self.sprite_sheet = sprite_sheet

        self.ss_name = sprite_sheet.name
        self.sprite_width = sprite_sheet.sprite_width
        self.sprite_height = sprite_sheet.sprite_height

        self.current_version = 1
        
        self.sprites = []

        self.num_frames = self.sprite_sheet.max_frames_per_animation
        self.num_frames_used = 0

        self.create_blank_animation(self.num_frames)


        self.max_width = self.sprite_width * self.num_frames
        self.width = self.sprite_width * self.num_frames_used
        self.height = self.sprite_height

    def create_blank_animation(self, num_frames):
        sprite_width = self.sprite_sheet.sprite_width
        sprite_height = self.sprite_sheet.sprite_height
        name = self.sprite_sheet.name
        self.sprites = [Sprite(name, width=sprite_width, height=sprite_height) for _ in range(num_frames)]

    def are_blanks_next_to_normal(self):
        for idx, sprite in enumerate(self.sprites):
            if sprite.is_blank:
                next = self.sprites[idx + 1]
                if next is not None and not next.is_blank:
                    return True, idx
        return False, -1

    def fix_frames(self):
        for sprite in self.sprites:
            if sprite.is_blank:
                self.sprites.remove(sprite)

        length = len(self.sprites)
        for _ in range(self.num_frames - length):
            self.sprites.append(Sprite(self.ss_name, width=self.sprite_sheet.sprite_width, height=self.sprite_sheet.sprite_height))

        # print('fixed frames, new length:', len(self.sprites))

    def get_frame(self, frame_index):
        if frame_index >= 0 and frame_index < len(self.sprites):
            return self.sprites[frame_index]

    def add_sprite(self, sprite):
        self.sprites[self.num_frames_used] = sprite
        self.num_frames_used += 1

    def change_sprite_at(self, index, sprite):
        if index >= 0 and index < len(self.sprites):
            self.sprites[index] = sprite

    def remove_sprite_at(self, index):
        if index >= 0 and index < len(self.sprites):
            self.sprites[index] = Sprite(self.ss_name, width=self.sprite_sheet.sprite_width, height=self.sprite_sheet.sprite_height)
            self.num_frames_used -= 1

        self.fix_frames()

class SpriteSheet:
    def __init__(self, name):
        self.name = name
        file_path = f'spritesheets/{name}/'
        self.current_version = 1
        
        self.sprite_width = 50
        self.sprite_height = 100
        self.max_frames_per_animation = 8
        self.animations = []

        self.bg_color = (255, 230, 255)

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        return image


clock = 0

shift_pressed = False
    
#print(load_object(1))
loading = False

current_loaded = -1


adder = 0

color_change_speed = 5

rects_to_draw = []

sprite_sheet_panel.load_properties()

dragging = False
dragged_panel = None
dragged_point = (0, 0)

color_history = []

run = True
while run:
    
    user.update()
    # print(user.current_toolbar)
    #print(current_loaded)
    if loading:
        current_loaded = np.clip(current_loaded, 0, num_files - 1)
        pixels = load_object(current_loaded)
        loading = False

    mousex, mousey = pygame.mouse.get_pos()
    
    screen.fill(BG_COLOR)


    object_x, object_y = int((mousex - border_x - offset_x) // pixel_size), int((mousey - border_y - offset_y) // pixel_size)
    object_x = np.clip(object_x, 0, gridSize - 1)
    object_y = np.clip(object_y, 0, gridSize - 1)
    if mouse_pressed_LB:
        if in_zone(border_x, border_y, real_object_size, real_object_size):
            idx = user.mouse_toolbars[0].selected_index
            rects_to_draw = user.mouse_toolbars[0].tools[idx].use()
            # draw_line(user.grip_point, coords_on_object)
    if mouse_pressed_RB:
        if in_zone(border_x, border_y, real_object_size, real_object_size):
            idx = user.mouse_toolbars[1].selected_index
            rects_to_draw =user.mouse_toolbars[1].tools[idx].use()

    if mouse_pressed_RB or mouse_pressed_LB:
        history.append(current_color)
        if current_color in history[:-2]:
            history.pop(history.index(current_color))
        if len(history) > 20:
            history.pop(0)
        current_history_id = 0
        remove_duplicates()

    if adder != 0:
        #print('siema')
        if in_zone(rgb_x, rgb_y, color_size): # czerwony
            one_color = np.clip(current_color[0] + adder, 0, 255)
            current_color = (one_color, current_color[1], current_color[2])
        if in_zone(rgb_x, rgb_y - 100, color_size): # zielony
            one_color = np.clip(current_color[1] + adder, 0, 255)
            current_color = (current_color[0], one_color, current_color[2])
        if in_zone(rgb_x, rgb_y - 200, color_size): # niebieski
            one_color = np.clip(current_color[2] + adder, 0, 255)
            current_color = (current_color[0], current_color[1], one_color)
        adder = 0


    

    draw_border(border_x + offset_x, border_y + offset_y, 5)

    pygame.draw.rect(screen, (10, 10, 10), (20 - 5, frameHeight - 80 - 5, color_size + 10, color_size + 10))
    draw_color(20, frameHeight - 80, current_color)


    pygame.draw.rect(screen, (10, 10, 10), (20 - 5, rgb_y - 5, color_size + 10, color_size + 10))
    pygame.draw.rect(screen, (10, 10, 10), (20 - 5, rgb_y - 100 - 5, color_size + 10, color_size + 10))
    pygame.draw.rect(screen, (10, 10, 10), (20 - 5, rgb_y - 200 - 5, color_size + 10, color_size + 10))
    draw_color(20, rgb_y, (255, 0, 0))
    draw_color(20, rgb_y - 100, (0, 255, 0))
    draw_color(20, rgb_y - 200, (0, 0, 255))

    draw_bar(20, rgb_y, (255, 255, 255), color_idx=0)
    draw_bar(20, rgb_y - 100, (255, 255, 255), color_idx=1)
    draw_bar(20, rgb_y - 200, (255, 255, 255), color_idx=2)

    draw_canvas()

    draw_history()

    toolbar1.handle_buttons()
    toolbar2.handle_buttons()


    toolbar1.draw()
    toolbar2.draw()

    coll = [0,0,0]
    coll[0] = (current_color[0] + clock // 2) % 255
    coll[1] = (current_color[1] + clock // 3) % 255
    coll[2] = (current_color[2] + clock // 5) % 255
    coll = tuple(coll)


    if rects_to_draw or user.is_selecting:
        # user.current_selection = (user.grip_point, user.current_point)
        for rect in rects_to_draw:
            if rect is None:
                continue
            pygame.draw.rect(screen, coll, rect)
    else:
        user.current_selection = (None, None)


    user.current_point = (object_x, object_y)

    if mousex > border_x and mousex < border_x + real_object_size:
        if mousey > border_y and mousey < border_y + real_object_size:
            #print(mousex // pixel_size, mousey // pixel_size)
            draw_cursor(mousex // pixel_size * pixel_size, mousey // pixel_size * pixel_size + 1, 6, 3)


    if user.settings_mode:
        for panel in panels:
            panel.update_dimensions(pos=False)
            
            panel.save_button.get_mouse_signal(mousex, mousey, mouse_pressed_LB)
            panel.draw()
            if panel.save_button.got_pressed():
                panel.save_properties()

            panel.update()

    




    if dragging and dragged_panel is not None:
        diff_x = mousex - dragged_point[0]
        diff_y = mousey - dragged_point[1]
        dragged_panel.x = dragged_panel.last_pos[0] + diff_x
        dragged_panel.y = dragged_panel.last_pos[1] + diff_y

        dragged_panel.update_dimensions(pos=False)



    print(get_outline(object_x, object_y))

    

    # for (x, y) in get_outline(object_x, object_y):
    #     if (x, y) is not None and 0 <= x < gridSize and 0 <= y < gridSize:
    #         cx = border_x + offset_x + (x * pixel_size) + (pixel_size // 2)
    #         cy = border_y + offset_y + (y * pixel_size) + (pixel_size // 2)
            
    #         draw_cursor(cx, cy, 6, 2)

    pygame.display.flip()

    key = pygame.key.get_pressed()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #KLIKNIECIE MYSZKA
                mouse_pressed_LB = True

                if user.settings_mode:
                    for panel in panels:
                        if in_zone(panel.x, panel.y, panel.width, panel.height) and not dragging:
                            dragged_point = (mousex, mousey)
                            dragging = True
                            dragged_panel = panel
                            panel.last_pos = (panel.x, panel.y)



                if user.grip_point is None or True:
                    user.grip_point = (object_x, object_y)
                user.current_point = (object_x, object_y)

                
                #player.x, player.y = pygame.mouse.get_pos()
                pass

            if event.button == 2:
                #KLIKNIECIE SCROLLA
                if in_zone(border_x, border_y, real_object_size, real_object_size):
                    current_color = pixels[object_y][object_x]
                    if history[-1] != current_color:
                        history.append(current_color)
                        if len(history) > 20:
                            history.pop(0)
                        current_history_id = 0
                    # print('czysto')
            if event.button == 3:
                #KLIKNIECIE MYSZKA PRAWYM
                mouse_pressed_RB = True

                if user.grip_point is None:
                    user.grip_point = (object_x, object_y)
                user.current_point = (object_x, object_y)

            if event.button == 4:
                # SCROLL W GORE
                scroll_up = True
                adder += color_change_speed

                if not user.settings_mode:
                    if in_zone(toolbar_x_start, toolbar_y_start, toolbar_width, toolbar_height):
                        if current_history_id > 0:
                            current_history_id -= 1
                            current_color = history[len(history) - 1 - current_history_id]
                    if user.current_toolbar != 0:
                        user.change_tool(-1)


                if user.settings_mode:
                    for panel in panels:
                        if panel.get_property_mouse_is_over() is not None and panel.get_property_mouse_is_over().enabled:
                            if not panel.get_property_mouse_is_over().is_text:
                                prop = panel.get_property_mouse_is_over()
                                prop.set_value(prop.value + 1)

            if event.button == 5:
                # SCROLL W DOL
                adder -= color_change_speed



                if not user.settings_mode:
                    if in_zone(toolbar_x_start, toolbar_y_start, toolbar_width, toolbar_height):
                        if current_history_id < len(history) - 1:
                            current_history_id += 1
                            current_color = history[len(history) - 1 - current_history_id]

                    if user.current_toolbar != 0:
                        user.change_tool(1)


                if user.settings_mode:
                    for panel in panels:
                        if panel.get_property_mouse_is_over() is not None and panel.get_property_mouse_is_over().enabled:
                            if not panel.get_property_mouse_is_over().is_text:
                                prop = panel.get_property_mouse_is_over()
                                prop.set_value(prop.value - 1)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_pressed_LB = False
                #PUSZCZENIE MYSZKI
                # user.grip_point = None
                user.current_point = None
                dragging = False
                dragged_panel = None

            if event.button == 3:
                # PUSZCZENIE MYSZKI PRAWYM
                mouse_pressed_RB = False
                
            if event.button == 4:
                # PUSZCZENIE SCROLLA W GORE
                scroll_up = False

            if event.button == 5:
                # PUSZCZENIE SCROLLA W DOL
                scroll_down = False

        if event.type == pygame.KEYDOWN:
            if user.settings_mode:
                
                if sprite_sheet_panel.get_property_mouse_is_over() is not None and sprite_sheet_panel.get_property_mouse_is_over().name == 'Sprite Name':
                    prop = sprite_sheet_panel.get_property_mouse_is_over()

                    if prop.is_text:
                        if event.key == pygame.K_BACKSPACE:
                            prop.set_value(prop.value[:-1])
                        else:
                            prop.set_value(prop.value + pygame.key.name(event.key))



            if event.key == pygame.K_LSHIFT:
                shift_pressed = True
            if event.key == pygame.K_s:
                if shift_pressed:
                    # save_to_new_object_type()
                    pass
                else:
                    save_object(name='object', data=pixels)


            if not user.settings_mode:
                if event.key == pygame.K_RIGHT:
                    if not arrow_pressed:
                        if current_loaded < num_files - 1:
                            current_loaded += 1
                        arrow_pressed = True
                        loading = True
                if event.key == pygame.K_LEFT:
                    if not arrow_pressed:
                        if current_loaded > 0:
                            current_loaded -= 1
                        arrow_pressed = True
                        loading = True

            # else:
            #     if event.key == pygame.K_RIGHT

            if event.key == pygame.K_c:
                pixels = [[(0, 0, 0) for _ in range(gridSize)] for _ in range(gridSize)]
                # print('ciemno')

            if event.key == pygame.K_ESCAPE:
                user.settings_mode = False

            if event.key == pygame.K_RETURN:
                user.settings_mode = True

            if event.key == pygame.K_DELETE:
                if not user.settings_mode:
                    if user.current_selection != (None, None):
                        p1, p2 = user.current_selection
                        x1 = min(p1[0], p2[0])
                        x2 = max(p1[0], p2[0])
                        y1 = min(p1[1], p2[1])
                        y2 = max(p1[1], p2[1])

                        for y in range(y1, y2 + 1):
                            for x in range(x1, x2 + 1):
                                pixels[y][x] = (0, 0, 0)
                        # user.grip_point = None
                        # user.current_point = None
                        # user.current_selection = (None, None)
                    # pixels = [[(255, 230, 255) for _ in range(gridSize)] for _ in range(gridSize)]
                    # print('pusto')

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                arrow_pressed = False
            if event.key == pygame.K_RIGHT:
                arrow_pressed = False
            if event.key == pygame.K_LSHIFT:
                shift_pressed = False


            

    
    clock += 1

pygame.quit()