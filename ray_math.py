#!/usr/bin/env python3

def sqrt(x, error=(2**-10)):
    r = 0
    step = x
    while abs(r * r - x) > error:
        if abs((r + step) * (r + step) - x) < abs(r * r - x):
            r += step
        elif abs((r - step) * (r - step) - x) < abs(r * r - x):
            r -= step
        else:
            step = step * 0.5
    return r


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
        if s <= 0:
            return vec3()
        return vec3(self.x / sqrt(s),
                    self.y / sqrt(s),
                    self.z / sqrt(s))

    def __abs__(self):
        return self.dot(self)


class Ray():
    def __init__(self, o, d):
        self.o = o
        self.d = d.normalized()


class Sphere():
    "x²+y²+z² = r"

    def __init__(self, x, y, z, r, color):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.color = color

    def trace(self,origin,direction,world,lights,raytrace,raydepth):
        for R in range(1000):
            r= 0.01*R
            if abs(origin+(direction)*r-vec3(self.x,self.y,self.z))<=self.r:
                return self.color,r
        return bg_color,pos_infinity


class Light():
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color


def vec2rgb(c):
    r = min(255,max(0,int(c.x*256)))
    g = min(255,max(0,int(c.y*256)))
    b = min(255,max(0,int(c.z*256)))
    return r,g,b

pos_infinity = float('+inf')
neg_infinity = float('-inf')
bg_color = vec3(0.1,0.1,0.1)
