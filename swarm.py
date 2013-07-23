#!/usr/bin/env python2.6

import random
from math import sqrt
from itertools import imap
from operator import add, sub

# number of swarms
SN = 100

class Swarm:
    def __init__(self, weight=1, avoid=0.3, attract=6, resolution=1):
        self.x          = (random.random()-0.5)*pow(10, resolution)*2
        self.y          = (random.random()-0.5)*pow(10, resolution)*2
        self.z          = (random.random()-0.5)*pow(10, resolution)*2
        self.weight     = weight
        self.avoid      = avoid
        self.attract    = attract

    def __str__(self): return '%.4f %.4f %.4f' % (self.x, self.y, self.z)

    def add(self, b):
        self.x += b[0]
        self.y += b[1]
        self.z += b[2]
        return [self.x, self.y, self.z]

def distance(a, b):
    return sqrt(pow(a.x-b.x, 2)+pow(a.y-b.y, 2)+pow(a.z-b.z, 2))

def gravity(d):
    return 1/pow(d, 2)

def movingG(a, b, d):
    return [(a.x-b.x)/d*gravity(d), (a.y-b.y)/d*gravity(d), (a.z-b.z)/d*gravity(d)]

def moving(a, b, d):
    return [(a.x-b.x)/d, (a.y-b.y)/d, (a.z-b.z)/d]

def genNext(world):
    dm = [[distance(a,b) for a in world] for b in world]
    for i,swarm in enumerate(world):
        move = [0, 0, 0]
        c = 0
        for j,dist in enumerate(dm[i]):
            if i == j or dist == 0:
                continue
            if dist > swarm.avoid and dist < swarm.attract:
                c+=1
                move = [x for x in imap(sub, move, moving(swarm, world[j], dist))]
            elif dist < swarm.avoid:
                c+=1
                move = [x for x in imap(add, move, moving(swarm, world[j], dist))]
        if c:
            world[i].add([x/c for x in move])

if __name__ == '__main__':
    world = [Swarm() for x in range(SN)]
    print '\n'.join(map(str, world))+'\ndone'
    for i in range(1000):
        genNext(world)
        print '\n'.join(map(str, world))+'\ndone'

