#!/usr/bin/env python3

def sqrt(x,error=(2**-100)):
    r = 0
    step = x
    while abs(r*r-x)>error:
        if abs((r+step)*(r+step)-x)<abs(r*r-x):
            r += step
        elif abs((r-step)*(r-step)-x)<abs(r*r-x):
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
    def dot(self,other):
        return sum((self.x*other.x,
                    self.y*other.y,
                    self.z*other.z))

    def normalized(self):
        s = abs(self)
        if s<=0:
            return vec3()
        return vec3(self.x/sqrt(s),
                    self.y/sqrt(s),
                    self.z/sqrt(s))

    def __abs__(self):
        return self.dot(self)


if __name__ == "__main__":
    v1 = vec3(1,0,0)
    v2 = vec3(1,2,3)
    s  = 3
    v3 = v2*s

    assert abs(v1) == 1.0
    assert abs(v2.normalized()) == 1.0
    assert abs(v1+v2) == abs(v2+v1)
    assert s*s*abs(v2) == abs(v3)
