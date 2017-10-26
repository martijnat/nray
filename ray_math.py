#!/usr/bin/env python3

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

from random import random

error=(2**-8)

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
        d = s**0.5
        return vec3(self.x / d,
                    self.y / d,
                    self.z / d)

    def __abs__(self):
        return self.dot(self)

def random_vector():
    return vec3(-1.0+2*random(),
                -1.0+2*random(),
                -1.0+2*random())


pos_infinity  = float('+inf')
neg_infinity  = float('-inf')
ambient_color = vec3(1,2,3).normalized()
bg_color      = ambient_color
light_color   = vec3(2,2,1).normalized()
purple        = vec3(1,0,1)
red           = vec3(1,0,0)
yellow        = vec3(1,1,0)
green         = vec3(0,1,0)
cyan          = vec3(0,1,1)
blue          = vec3(0,0,1)

gray          = vec3(0.5,0.5,0.5)
white         = vec3(1,1,1)
black         = vec3(0,0,0)

def color_mult(c1,c2):
    return vec3(c1.x*c2.x,
                c1.y*c2.y,
                c1.z*c2.z)

class Ray():
    def __init__(self, o, d):
        self.o = o
        self.d = d.normalized()


class Sphere():
    "x²+y²+z² = r²"

    def __init__(self, x, y, z, r, color, reflectivity=0.3, roughness=0.1):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.center = vec3(x,y,z)
        self.color = color
        self.reflectivity = reflectivity        
        self.roughness = roughness

    def intersection(self,origin,direction):
        # p = o +d·t
        # px² +py² + pz²- r² = 0
        o = origin-self.center
        d = direction
        # t²*d.dot(d) + t * 2* o.dot(d) + o.dot(O) - r² = 0

        # # quadratic equation
        # x  = (-b ± √(b²-4ac)) / 2a

        # a = d²
        # b = 2od
        # c = o² - r²

        a = d.dot(d)            # always 1.0
        b = 2.0 * o.dot(d)
        c = o.dot(o) - (self.r*self.r)


        S = (b*b)-(4*a*c)
        if S<=error:
            return pos_infinity

        sqrtS = S**0.5
        t1 = (-b-sqrtS)/(2.0*a)
        t2 = (-b+sqrtS)/(2.0*a)

        t = -1
        if t1<=0 and t2>0:
            return t2
        elif t2<=0 and t1>0:
            return t1
        elif t1<=0 and t2<=0:
            return pos_infinity
        else:
            return min(t1,t2)

    def trace(self,origin,direction,world,lights,raytrace,raydepth):
        t = self.intersection(origin,direction)
        if t==pos_infinity:
            return bg_color,pos_infinity
        elif t<=0:
            return bg_color,pos_infinity


        p = origin+direction*t
        color = color_mult(self.color,ambient_color)
        sphere_normal = (p - self.center).normalized()
        
        for light in lights:
            light_angle = sphere_normal.dot((light.pos-p).normalized())
            if light_angle>0:
                if light.free_path(p,world):
                    color = color + (color_mult(self.color,light.color)*light_angle)


        refrected_direction = direction - sphere_normal*(direction.dot(sphere_normal)*2)
        random_direction = (refrected_direction + random_vector()).normalized()
        
        new_direction = (random_direction*self.roughness + refrected_direction*(1-self.roughness)).normalized()
        
        color = (color*(1-self.reflectivity)
                 + raytrace(world,
                            lights,
                            origin+direction*(t-error),
                            new_direction,
                            raydepth+1)*self.reflectivity)
       
        return color,t


class Light():
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
    def free_path(self,pos,world):
        mt = (self.pos-pos).dot(self.pos-pos)
        d = (pos-self.pos).normalized()
        o = self.pos
        
        for thing in world:
            t = thing.intersection(o,d)
            if t*t<mt-error and t*t>error:
                return False
        return True


def srgb(l):
    if l<=0.00313066844250063:
        return min(255,max(0,int(l*12.92*256)))
    return min(255,max(0,int(256*1.055*(l**(1/2.4))-0.055)))
    
def vec2rgb(c):
    r = srgb(c.x)
    g = srgb(c.y)
    b = srgb(c.z)
    return r,g,b
