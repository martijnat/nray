#!/usr/bin/env pypy3
from ray_math import *

# output_width,output_height=160,120
output_width,output_height=640,480

cameraX = vec3(1,0,0)
cameraY = vec3(0,1,0)
cameraZ = vec3(0,0,1)
cameraO = vec3(0,0,-10)

world = [
    Sphere(0,0,0,0.5,red),
    Sphere(.5,.3,-.5,0.4,green),
    Sphere(0,-99999.5,0,99999,blue)
]
lights = [Light(vec3(3,10,-3),light_color)]

def raytrace(world,lights,origin,direction,raydepth=0):
    if raydepth>8:
        return bg_color
    current_color = bg_color
    current_dist = pos_infinity
    for obj in world:
        test_color,test_dist = obj.trace(origin,direction,world,lights,raytrace,raydepth)
        if (test_dist > 0) and (test_dist<current_dist):
            current_dist = test_dist
            current_color = test_color

    return vec2rgb(current_color)

# write final image
print("P3",output_width,output_height,255)
screen_ratio = output_width/output_height
for y in range(output_height):
    y_ratio = y/float(output_height)
    for x in range(output_width):
        x_ratio = x/float(output_width)
        p = cameraX*(2*x_ratio-1.0)*screen_ratio - cameraY*(2*y_ratio-1.0) + cameraZ*1
        d = (p-cameraO).normalized()
        r,g,b = raytrace(world,lights,cameraO,d)
        print(r,g,b)

