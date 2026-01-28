from PIL import Image
import os, os.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from drawing import load_object, load_object_by_whole_name

files = [name for name in os.listdir('Projects')]
num_files = len(files)

pictures = [name for name in os.listdir('Saved-Pictures') if name.endswith('.jpg')]
print(pictures)

difference = [name[:-4] for name in files if name[:-4] + '.jpg' not in pictures]

print(difference)

def generate_image_by_number(number):
    img = Image.new('RGB', (25, 25))
    pixels = load_object(number)

    for i in range(25):
        for j in range(25):
            img.putpixel((j, i), pixels[i][j])

    name = 'object' + str(number) + '.jpg'
    path = 'Saved-Pictures/'
    img.save(path + name)


def generate_image_by_name(name, pixel_size=1):
    img = Image.new('RGB', (25 * pixel_size, 25 * pixel_size))
    pixels = load_object_by_whole_name(name)

    if not pixels:
        pixels = [[(0, 0, 0) for _ in range(25)] for _ in range(25)]

    for i in range(25):
        for j in range(25):
            for di in range(pixel_size):
                for dj in range(pixel_size):
                    img.putpixel((j * pixel_size + dj, i * pixel_size + di), pixels[i][j])
            # img.putpixel((j * pixel_size, i * pixel_size), pixels[i][j])

    name = name + '.jpg' if pixel_size == 1 else name + f'_{pixel_size * 25}px' + '.jpg'
    path = 'Saved-Pictures/'
    img.save(path + name, quality=100)


# for file_name in files:
#     file_name = file_name[:-4]
#     generate_image_by_name(file_name)


pictures_generated = 0

for file_name in difference:
    generate_image_by_name(file_name)
    generate_image_by_name(file_name, 10)
    pictures_generated += 2

print(f'Succesfully generated {pictures_generated} new pictures.')


# generate_image_by_name('object18', pixel_size=50)