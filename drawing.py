import pygame
import numpy as np

frameWidth = 1200
frameHeight = 700

screen = pygame.display.set_mode((frameWidth, frameHeight))

pixel_size = 25

def draw_cursor(x, y, length, thickness, pixel_size=pixel_size, surface=screen):
    rect1 = pygame.Rect(x, y, length, thickness)
    rect2 = pygame.Rect(x + pixel_size - length, y, length, thickness)

    rect3 = pygame.Rect(x, y + pixel_size - thickness, length, thickness)
    rect4 = pygame.Rect(x + pixel_size - length, y + pixel_size - thickness, length, thickness)


    rect5 = pygame.Rect(x, y, thickness, length)
    rect6 = pygame.Rect(x + pixel_size - thickness, y, thickness, length)

    rect7 = pygame.Rect(x, y + pixel_size - length, thickness, length)
    rect8 = pygame.Rect(x + pixel_size - thickness, y + pixel_size - length, thickness, length)

    pygame.draw.rect(surface, (255, 255, 255), rect1)
    pygame.draw.rect(surface, (255, 255, 255), rect2)
    pygame.draw.rect(surface, (255, 255, 255), rect3)
    pygame.draw.rect(surface, (255, 255, 255), rect4)

    pygame.draw.rect(surface, (255, 255, 255), rect5)
    pygame.draw.rect(surface, (255, 255, 255), rect6)
    pygame.draw.rect(surface, (255, 255, 255), rect7)
    pygame.draw.rect(surface, (255, 255, 255), rect8)


pixels = []

import os, os.path

num_files = len([name for name in os.listdir('Projects')]) - 1

def save_object(name='object', data=pixels):
    #num_files = len([name for name in os.listdir('custom_objects')])

    name = name + str(num_files)
    path = 'Projects/' + name + '.txt'
    with open(path, 'w') as f:
        f.write(str(data))

# def save_to_new_object_type(name='object'):
#     name = name + str(num_files)

#     save_object()
#     with open('objects.txt', 'r') as f:
#         for line in f:
#             pass
#         number = int(line[0])

#     with open('objects.txt', 'a') as f:
#         f.append(str(number + 1) + ' ' + name)

#save_to_new_object_type()

import ast 

def load_object(number, name='object'):
    #num_files = len([name for name in os.listdir('custom_objects')])

    name = name + str(number)
    path = 'Projects/' + name + '.txt'

    with open(path, 'r') as f:
        lista = f.read()
        return ast.literal_eval(lista)
    
def load_object_by_whole_name(name):
    #num_files = len([name for name in os.listdir('custom_objects')])

    name = name
    path = 'Projects/' + name + '.txt'

    with open(path, 'r') as f:
        lista = f.read()
        return ast.literal_eval(lista)
    

def get_scaled_pixels(pixels, wanted_size=40):
    original_size = len(pixels)
    #ratio = np.clip(int(original_size / wanted_size), 1, 10)
    ratio = original_size / wanted_size
    new_pixels = [[pixels[int(ratio * i)][int(ratio * j)] for j in range(wanted_size)] for i in range(wanted_size)]

    return new_pixels

def scale_by_2(pixels):
    size = len(pixels)
    new_pixels = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(pixels[i][j])
            row.append(pixels[i][j])
        new_pixels.append(row)
        new_pixels.append(row)
    return new_pixels

def average_color_in_region(pixels):
    r, g, b = 0, 0, 0
    size = len(pixels)
    den = size * size
    for i in range(size):
        for j in range(size):
            r += pixels[i][j][0]
            g += pixels[i][j][1]
            b += pixels[i][j][2]
    return (int(r / den), int(g / den), int(b / den))




big_pixel_size = 5


from PIL import Image

def average_from_nearby(pixels):
    r, g, b = 0, 0, 0
    size = len(pixels)
    new_pixels = []
    colors_nearby = []

    jump = size / big_pixel_size / 2

    for y in range(big_pixel_size):
        pixels_row = []
        for x in range(big_pixel_size):
            r, g, b = 0, 0, 0

            colors_nearby = []

            #colors_nearby = [pixels[np.clip(y + j, 0, size - 1)][np.clip(x - i, 0, size - 1)] for i in range(- radius, radius + 1) for j in range(- radius, radius + 1)]

            

            colors_nearby = [pixels[int(jump + 2 * jump * y) + j][int(jump + 2 * jump * x) + i] for i in range(- int(jump), int(jump)) for j in range(- int(jump), int(jump))]

            # colors_left = [pixels[y][np.clip(x - i, 0, size - 1)] for i in range(1, radius + 1)]
            # colors_right = [pixels[y][np.clip(x + i, 0, size - 1)] for i in range(1, radius + 1)]
            # colors_up = [pixels[np.clip(y - i, 0, size - 1)][x] for i in range(1, radius + 1)]
            # colors_down = [pixels[np.clip(y + i, 0, size - 1)][x] for i in range(1, radius + 1)]

            # colors_nearby.extend(colors_left)
            # colors_nearby.extend(colors_right)
            # colors_nearby.extend(colors_up)
            # colors_nearby.extend(colors_down)

            for color in colors_nearby:
                r += color[0]
                g += color[1]
                b += color[2]

            # den = 4 * radius ** 2
            den = len(colors_nearby)
            pixels_row.append((int(r / den), int(g / den), int(b / den)))
        new_pixels.append(pixels_row)
    return new_pixels

        

# pixels_test = load_object_by_whole_name('object5')

img = Image.new('RGB', (5, 5))

# new_pixels = average_from_nearby(pixels_test)


# print(new_pixels)

# for j in range(5):
#     for i in range(5):
#         img.putpixel((i, j), new_pixels[j][i])

img.save('test1.jpg')

img2 = Image.new('RGB', (25, 25))

# every5 = [[pixels_test[j * 5][i * 5] for i in range(5)] for j in range(5)]



def generate_pixelated_image(name):
    original_img = Image.open('Saved-Pictures/' + name)
    original_img = original_img.convert('RGB')

    original_pixels2 = original_img.load()

    original_pixels = []

    for i in range(original_img.size[0]):
        original_pixels.append([])
        for j in range(original_img.size[1]):
            original_pixels[i].append(original_pixels2[i, j])

    new_pixels = average_from_nearby(original_pixels)


    image_size = 20
    num_big_pixels = int(image_size / big_pixel_size)

    new_image = Image.new('RGB', (image_size, image_size))

    for y in range(num_big_pixels):
        for x in range(num_big_pixels):
            for k in range(big_pixel_size):
                for l in range(big_pixel_size):
                    # jakim cudem x i y tutaj odwrotnie??
                    new_image.putpixel((x * big_pixel_size + k, y * big_pixel_size + l), new_pixels[y][x])


    path = 'Saved-Pictures/pixelated/'
    name = 'pixelated_' + name[:-4] + '.jpg'
    new_image.save(path + name, quality=100)

#img2.save('test2.jpg')