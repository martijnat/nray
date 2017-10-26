#!/usr/bin/env pypy3

# Copyright (C) 2017  Martijn Terpstra

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from ray_math import *
from sys import stderr

output_width, output_height = 1920*8, 1080*8

cameraX = vec3(1, 0, 0)
cameraY = vec3(0, 1, 0)
cameraZ = vec3(0, 0, 1)
cameraO = vec3(0, 0, -2)

world  = [
    Sphere(-0.3,  -0.3,  0.1,   0.2, black,0.7,0.0),
    Sphere( 0.3,  -0.3,  0.1,   0.2, white,0.5,0.5),
   
    Sphere( 0.0, -999.5, 0.0, 999, gray, 0.7,0.5),
    Sphere( 0.0, 0, 1.0, 0.5, green),
    Sphere(-1.0, 0, 0.5, 0.5, red),
    Sphere( 1.0, 0, 0.5, 0.5, blue),


    Sphere(-0.5, -0.4, -0.3, 0.1, purple),
    Sphere(-0.3, -0.4, -0.3, 0.1, blue),
    Sphere(-0.1, -0.4, -0.3, 0.1, cyan),
    
    Sphere( 0.1, -0.4, -0.3, 0.1, green),
    Sphere( 0.3, -0.4, -0.3, 0.1, yellow),
    Sphere( 0.5, -0.4, -0.3, 0.1, red),

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
for y in range(output_height):
    stderr.write("%i/%i\r"%(y,output_height))
    y_ratio = y / float(output_height)
    for x in range(output_width):
        x_ratio = x / float(output_width)
        p = cameraX * (2 * x_ratio - 1.0) * screen_ratio - \
            cameraY * (2 * y_ratio - 1.0) + cameraZ * 1
        d = (p - cameraO).normalized()
        
        r, g, b = vec2rgb(raytrace(world, lights, cameraO, d))
        print(r, g, b)
