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

from sys import stderr

def main():
    # lower quality speeds up rendering time at the cost of image quality
    quality = 50
    output_width, output_height = int(1920*(quality**0.5)), int(1080*(quality**0.5))

    # Camera position and relative axis.
    cameraX = vec3(1, 0, 0)
    cameraY = vec3(0, 1, 0)
    cameraZ = vec3(0, 0, 1)
    cameraO = vec3(0, 0, -2)

    world  = [
         # The floor is just a giant sphere
        CheckeredSphere( 0.0, -10000.2, 0.0,  10000, vec3(1.00, 1.00, 1.00)),
        # 3 largest spheres in the back
        Sphere(-0.7,  0.1,  -0.4,  0.3,  vec3(0.44, 0.00, 0.89)),
        Sphere( 0.0,  0.1,  -0.3,  0.3,  vec3(0.00, 0.89, 0.44)),
        Sphere( 0.7,  0.1,  -0.4,  0.3,  vec3(0.89, 0.44, 0.00)),
        # 2 large floating spheres
        Sphere(-0.3,  0.2,  -0.7,  0.2,  vec3(0.00, 0.44, 0.89)),
        Sphere( 0.3,  0.2,  -0.7,  0.2,  vec3(0.44, 0.89, 0.00)),
        # small spheres sunk into floor
        Sphere(-0.5, -0.15, -0.9,  0.1,  vec3(0.70, 0.00, 0.70)),
        Sphere(-0.3, -0.15, -0.8,  0.1,  vec3(0.00, 0.00, 1.00)),
        Sphere(-0.1, -0.15, -0.7,  0.1,  vec3(0.00, 0.70, 0.70)),
        Sphere( 0.1, -0.15, -0.7,  0.1,  vec3(0.00, 1.00, 0.00)),
        Sphere( 0.3, -0.15, -0.8,  0.1,  vec3(0.70, 0.70, 0.00)),
        Sphere( 0.5, -0.15, -0.9,  0.1,  vec3(1.00, 0.00, 0.00)),
        # small pink spheres at the edges of sunken spheres
        Sphere(-0.5, -0.05, -1.0,  0.05, vec3(0.89, 0.00, 0.44)),
        Sphere( 0.5, -0.05, -1.0,  0.05, vec3(0.89, 0.00, 0.44)),
        # Transparent orbs in the foreground
        Sphere(-0.3, -0.15, -1.20, 0.05, vec3(0.50, 0.00, 1.00),0.6,0.02,-1),
        Sphere( 0.0, -0.15, -1.35, 0.05, vec3(0.00, 1.00, 0.50),0.6,0.02,-1),
        Sphere( 0.3, -0.15, -1.20, 0.05, vec3(1.00, 0.50, 0.00),0.6,0.02,-1),]

    # A single light source. Multiple light sources could be used
    sun = Light(vec3(1,8,-0.5), vec3(2,2,1).normalized())

    # Write ppm image format header
    print("P3 %i %i 255"%(output_width, output_height))

    # for every x,y coordintate on the output image shoot a ray and record its color
    screen_ratio = output_width / float(output_height)
    for y in range(output_height):
        stderr.write("%i/%i\r"%(y,output_height))
        y_ratio = y / float(output_height)
        for x in range(output_width):
            x_ratio = x / float(output_width)
            p = cameraX * (2 * x_ratio - 1.0) * screen_ratio - \
                cameraY * (2 * y_ratio - 1.0) + cameraZ * 1
            d = (p - cameraO).normalized()
            print("%i %i %i"%vec2rgb(raytrace(world, sun, cameraO, d)))


def raytrace(world, sun, origin, direction, bounce_count=0):
    if bounce_count > 5:
        # For performace reasons we limit the maximum amount of bounces.
        return vec3(1,2,3).normalized()

    # Color in case the ray hits nothing
    current_color = vec3(1,2,3).normalized()
    # distance to nearest object found so far
    current_dist = float('+inf')

    for ball in world:
        if abs(origin-ball.center)>(ball.r+error):
            t = sphere_ray_collision(ball,origin,direction)
            if t>0 and t<current_dist:
                current_dist = t
                p = origin+direction*t
                color = color_mult(ball.material(p),vec3(1,2,3).normalized())
                sphere_normal = ((p - ball.center)).normalized()


                light_angle = sphere_normal.dot((sun.pos-p).normalized())
                if light_angle>0 and sun.free_path(p,world):
                    light_angle = light_angle
                    color = color + (color_mult(ball.material(p),sun.color)*light_angle)

                reflected_direction = (direction - sphere_normal*(direction.dot(sphere_normal)*(2.0))).normalized() * ball.refraction
                new_direction = (random_vector()*ball.roughness + reflected_direction*(1-ball.roughness)).normalized()
                current_color = (color*(1-ball.reflectivity)
                                 + raytrace(world,
                                            sun,
                                            origin+direction*(t-error),
                                            new_direction,
                                            bounce_count+1)*ball.reflectivity)

    return current_color

# default random is a bit slow, so lets build something custom
class CustomRNG():
    """Simple RNG that is good enough for a ray tracer. Its internal state
    is only 32-bits so at best it will repeat after 4GB of data.

    """
    def __init__(self):
        # Rijndeal S-box. A random S-box can also be used
        self.S = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
                  0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
                  0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0,
                  0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
                  0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC,
                  0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
                  0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A,
                  0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
                  0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0,
                  0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
                  0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B,
                  0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
                  0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85,
                  0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
                  0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5,
                  0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
                  0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17,
                  0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
                  0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88,
                  0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
                  0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C,
                  0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
                  0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9,
                  0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
                  0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6,
                  0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
                  0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E,
                  0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
                  0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94,
                  0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
                  0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68,
                  0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]

        # internal state, any numbers can be used
        self.w = 2
        self.x = 3
        self.y = 5
        self.z = 7
    def int8(self):
        "get random integer between 0 and 255"
        r = self.w
        r = self.S[r];
        r ^= self.x;
        r = self.S[r];
        r ^= self.y;
        r = self.S[r];
        r ^= self.z;

        self.w, self.x,self.y,self.z = r , self.w, self.x, self.y
        return self.w
    def __call__(self):
        "return a random float"
        r1 = self.int8()
        r2 = self.int8()
        r3 = self.int8()
        r4 = self.int8()
        r_int32 = (r1<<24)+(r2<<16)+(r3<<8)+(r4)
        return r_int32/(2**32)

random = CustomRNG()

error=(2**-32)                  # used for comparisons of floats to account for rounding errors

# Vector of size 3, used for positions, direction and r,g,b color triples.
class vec3():
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "(%f, %f, %f)" % (self.x, self.y, self.z)

    def __neg__(self):
        return vec3(-self.x,
                    -self.y,
                    -self.z)

    def __add__(self, other):
        return vec3(self.x + other.x,
                    self.y + other.y,
                    self.z + other.z)

    def __sub__(self, other):
        return self + -other

    def __mul__(self, scalar):
        return vec3(scalar * self.x,
                    scalar * self.y,
                    scalar * self.z)

    def dot(self, other):
        return sum((self.x * other.x,
                    self.y * other.y,
                    self.z * other.z))

    def normalized(self):
        s = abs(self)
        if s <= error:
            return vec3()
        return vec3(self.x / s,
                    self.y / s,
                    self.z / s)

    def __abs__(self):
        return (self.dot(self))**0.5

def random_vector():
    return vec3(-1.0+2*random(),
                -1.0+2*random(),
                -1.0+2*random())

def color_mult(c1,c2):
    return vec3(c1.x*c2.x,
                c1.y*c2.y,
                c1.z*c2.z)

def sphere_ray_collision(ball,origin,direction):
    # Find point of collision between a ray and sphere

    # Points on a ray with origin o and direction vector d are given by o+dt
    # Points on the surface of the sphere at the origin with radio r are given by p² - r² = 0
    # The intersections of these gives us (o+dt)² - r² = 0
    # This can be rewritten as (d²)t² + (2do)t + (o²-r²) = 0

    # So we solve the quadratic equation at²+bt+c = 0 with the following a,b and c
    a = direction.dot(direction)
    b = 2.0 * (origin-ball.center).dot(direction)
    c = (origin-ball.center).dot(origin-ball.center) - (ball.r**2)
    # We can solve this with the quadratic equation t = (-b±sqrt(b²-4ac)) / 2a

    # Calculate the root term
    S = (b*b)-(4*a*c)
    # If the root term is negative, there are no solutions
    if S<=error:
        return float('+inf')

    # Otherwise calculate both points
    sqrtS = S**0.5
    t1 = (-b-sqrtS)/(2.0*a)
    t2 = (-b+sqrtS)/(2.0*a)
    # return the closes point
    return min(t1,t2)

class Sphere():
    "A sphere defined by a center x,y,z and radius r"
    def __init__(self, x, y, z, r, color, reflectivity=0.3, roughness=0.01,refraction=1):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.center = vec3(x,y,z)
        self.color = color
        # fraction of light that is not taken from sphere color on hit but from a reflected raytrace
        self.reflectivity = reflectivity
        # amount by which a reflect ray is non-perfect
        self.roughness = roughness
        # Amount by which a ray changes it direction on a reflection.
        # Positive values bounce off the sphere
        # Negative values allow a ray to pass through the sphere simulating transparency
        self.refraction = refraction
    def material(self, p):
        return self.color

class CheckeredSphere(Sphere):
    """
    Spere with a custom material function to simulate a checkerboard.
    Works best where the surface normal of the sphere is close to one of
    the base vectors"""
    def material(self,p):
        if ((p.x%0.2)>0.1)^((p.y%0.2)>0.1)^((p.z%0.2)>0.1):
            return self.color
        else:
            return vec3(1,1,1)-self.color

class Light():
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
    def free_path(self,pos,world):
        for ball in world:
            t = sphere_ray_collision(ball,self.pos,(pos-self.pos).normalized())
            if t*t<(self.pos-pos).dot(self.pos-pos)-error and t*t>error:
                return False
        return True

def srgb(l):
    "Maps a color from [0,1) (linear) to [0,255] (gamma-corrected)"
    return min(255,max(0,int(l*12.92*256 if l<=0.00313066844250063 else 256*1.055*(l**(1/2.4))-0.055)))

def vec2rgb(c):
    "Given a vec3 representing a color, return a triplet of r,g,b values"
    r = srgb(c.x)
    g = srgb(c.y)
    b = srgb(c.z)
    return r,g,b

if __name__ == "__main__":
    main()


