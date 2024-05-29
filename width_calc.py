
import math
pixel_depths = {"BW": 1,
                "RGB/BGR": 3,
                "RGBA": 4}

while True:
    file_size = input('file size in bytes: ')
    if not file_size: break

    for type in pixel_depths:
        pixel_count = int(file_size) / pixel_depths[type]
        if pixel_count % 1 != 0: continue
        print(f'\n{type}: ',end='')
        #math.floor(math.sqrt(pixel_count))
        for n in range(50,int(pixel_count)):
            if (int(pixel_count) % n == 0):
                print(f'{n} ',end='')
        print('')
