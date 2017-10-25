#!/usr/bin/env pypy3
from ray_math import *
from sys import stderr

# output_width,output_height=64,64
# output_width,output_height=160,120
# output_width,output_height=320,240
# output_width,output_height=640,480
# output_width, output_height = 1024, 768

output_width, output_height = 1920, 1080

# output_width, output_height = 480, 800

cameraX = vec3(1, 0, 0)
cameraY = vec3(0, 1, 0)
cameraZ = vec3(0, 0, 1)
cameraO = vec3(0, 0, -2)

world  = [
    Sphere(-0.3,  -0.3,  0.1,   0.2, black,0.7,0.0),
    Sphere( 0.3,  -0.3,  0.1,   0.2, white,0.5,0.5),
   
    Sphere( 0.0, -999.5, 0.0, 999, gray, 0.7,0.5),
    Sphere( 0.0, 0, 1, 0.5, green),
    Sphere(-1.0, 0, 0, 0.5, red),
    Sphere( 1.0, 0, 0, 0.5, blue),
]
lights = [Light(vec3(7, 10, -3), light_color)]


def raytrace(world, lights, origin, direction, raydepth=0):
    if raydepth > 8:
        return bg_color
    current_color = bg_color
    current_dist = pos_infinity
    for obj in world:
        test_color, test_dist = obj.trace(
            origin, direction, world, lights, raytrace, raydepth)
        if (test_dist > 0) and (test_dist < current_dist):
            current_dist = test_dist
            current_color = test_color

    return current_color


# write final image
print("P3", output_width, output_height, 255)
screen_ratio = output_width / output_height

sample_x = 8
sample_y = sample_x

for y in range(output_height):
    stderr.write("%i/%i\r"%(y,output_height))
    y_ratio = y / float(output_height)
    for x in range(output_width):
        x_ratio = x / float(output_width)
        color = vec3()
        for sy in range(sample_y):
            for sx in range(sample_x):
                cx = x_ratio + sx/(output_width*sample_x)
                cy = y_ratio + sy/(output_height*sample_y)
                p = cameraX * (2 * cx - 1.0) * screen_ratio - \
                    cameraY * (2 * cy - 1.0) + cameraZ * 1
                d = (p - cameraO).normalized()
                color = color + raytrace(world, lights, cameraO, d)
            
        color = color * (1.0/(sample_x*sample_y))
        r, g, b = vec2rgb(color)
        print(r, g, b)
