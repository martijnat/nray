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

# default random is a bit slow, so lets build something custom
class CustomRNG():
    "Simple RNG that is good enough for a ray tracer but terrible from a crypto standpoint"
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

error=(2**-32)

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

    def __init__(self, x, y, z, r, color, reflectivity=0.3, roughness=0.0,refraction=1):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.center = vec3(x,y,z)
        self.color = color
        self.reflectivity = reflectivity        
        self.roughness = roughness
        self.refraction = refraction
    def material(self, p):
        return self.color

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
        color = color_mult(self.material(p),ambient_color)
        sphere_normal = ((p - self.center)).normalized()
        
        for light in lights:
            light_angle = sphere_normal.dot((light.pos-p).normalized())
            if light_angle>0:
                if light.free_path(p,world):
                    color = color + (color_mult(self.material(p),light.color)*light_angle)


        refrected_direction = direction - sphere_normal*(direction.dot(sphere_normal)*(1.0+self.refraction))
        random_direction = (refrected_direction + random_vector()).normalized()
        
        new_direction = (random_direction*self.roughness + refrected_direction*(1-self.roughness)).normalized()
        
        color = (color*(1-self.reflectivity)
                 + raytrace(world,
                            lights,
                            origin+direction*(t-error),
                            new_direction,
                            raydepth+1)*self.reflectivity)
       
        return color,t

class CheckeredSphere(Sphere):
    def material(self,p):
        scale=0.3
        oddx = (p.x%scale)>0.5*scale
        oddy = (p.y%scale)>0.5*scale
        oddz = (p.z%scale)>0.5*scale
        odd = oddx^oddy^oddz
        if odd:
            return self.color
        else:
            return vec3(1,1,1)-self.color
    
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
