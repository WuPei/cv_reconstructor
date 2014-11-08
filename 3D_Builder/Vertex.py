# CS4243: Computer Vision and Pattern Recognition
# Zhou Bin
# 29th, Oct, 2014

import os
import math


class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def sum(a, b):
        return Vertex(a.x + b.x, a.y + b.y, a.z + b.z)

    def diff(a, b):
        return Vertex(a.x - b.x, a.y - b.y, a.z - b.z)

    def cross(a, b):
        return Vertex(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)

    def distance(a, b):
        x = math.pow(a.x - b.x, 2)
        y = math.pow(a.y - b.y, 2)
        z = math.pow(a.z - b.z, 2)
        return math.sqrt(x + y + z)

    def normalize(a):
        temp = math.sqrt(a.x * a.x + a.y * a.y + a.z * a.z)
        return Vertex(a.x / temp, a.y / temp, a.z / temp)

    def scale(a, v):
        return Vertex(a.x * v, a.y * v, a.z * v)

    def equal(a):
        return Vertex(a.x, a.y, a.z)
		