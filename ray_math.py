#!/usr/bin/env python3
from sys import stderr

error=(2**-100)

# def sqrt(x):
#     r = 0
#     step = x
#     while abs(r * r - x) > error:
#         if abs((r + step) * (r + step) - x) < abs(r * r - x):
#             r += step
#         elif abs((r - step) * (r - step) - x) < abs(r * r - x):
#             r -= step
#         else:
#             step = step * 0.5
#     return r
from math import sqrt


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
        return vec3(self.x / sqrt(s),
                    self.y / sqrt(s),
                    self.z / sqrt(s))

    def __abs__(self):
        return self.dot(self)


pos_infinity  = float('+inf')
neg_infinity  = float('-inf')
bg_color      = vec3(0.1,0.1,0.1)
ambient_color = vec3(0.25,0.5,0.75)
light_color   = vec3(0.75,0.5,0.25)
red           = vec3(1,0,0)
green         = vec3(0,1,0)
blue          = vec3(0,0,1)

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

    def __init__(self, x, y, z, r, color):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.center = vec3(x,y,z)
        self.color = color

    def intersect(self,p):
        return abs(p-self.center)<=(self.r)**2

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

        t1 = (-b-sqrt(S))/(2.0*a)
        t2 = (-b+sqrt(S))/(2.0*a)

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
            return blue,pos_infinity
        elif t<=0:
            return green,pos_infinity

        return self.color,t

        # for R in range(1000):
        #     r= 0.01*R
        #     if self.intersect(origin+(direction)*r):
        #         p = origin+direction*r
        #         # stderr.write("%s\n"%(t*r))
        #         # quit(1)
        #         color = color_mult(self.color,ambient_color)
        #         for light in lights:
        #             sphere_normal = (p - self.center).normalized()
        #             light_angle = sphere_normal.dot((light.pos-p).normalized())
        #             if light_angle>0:
        #                 if light.free_path(p,world):
        #                     color = color + (color_mult(self.color,light.color)*light_angle)
        #         return color,r
        # return bg_color,pos_infinity


class Light():
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
    def free_path(self,pos,world):
        d = (pos-self.pos)
        for R in range(1,1000):
            r = (R*0.001)
            p = pos*(1-r)+self.pos*r
            for o in world:
                if o.intersect(p):
                    return False
        return True


def vec2rgb(c):
    r = min(255,max(0,int(c.x*256)))
    g = min(255,max(0,int(c.y*256)))
    b = min(255,max(0,int(c.z*256)))
    return r,g,b
