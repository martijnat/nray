#!/usr/bin/env python3
from ray_math import vec3

output_width=640
output_height=480

# write final image
print("P3",output_width,output_height,255)
gridsize=8
for y in range(output_height):
    for x in range(output_width):
        if (((x//gridsize)%2==1 and (y//gridsize)%2==0) or
            ((x//gridsize)%2==0 and (y//gridsize)%2==1)):
            print(152,152,152)
        else:
            print(104,104,104)
