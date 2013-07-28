#!/usr/bin/env python

import random
from math import sqrt

class Agent:
    count = 0

    def __init__(self, name='Bond', resolution=1, x=None, y=None, z=None, color="FF00FFFF", **kwargs):
        self.name  = '{:s}_{:0>4d}'.format(name, Agent.count)
        self.color = color
        self.x     = (random.random()-0.5)*pow(10, resolution)*2 if x == None else x
        self.y     = (random.random()-0.5)*pow(10, resolution)*2 if y == None else y
        self.z     = (random.random()-0.5)*pow(10, resolution)*2 if z == None else z
        Agent.count += 1
        if hasattr(self, 'init'):
            self.init(**kwargs)

    def __str__(self): return '{:s} {:.8f} {:.8f} {:.8f} {:s}'.format(self.name, self.x, self.y, self.z, self.color)

    def act(self):
        pass

    def distance(self, bgent):
        return sqrt(pow(self.x-bgent.x, 2)+pow(self.y-bgent.y, 2)+pow(self.z-bgent.z, 2))

    def vector_to(self, bgent, d=-1):
        d = float(d)
        return [(self.x-bgent.x)/d, (self.y-bgent.y)/d, (self.z-bgent.z)/d]

    def move(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z
        return self

class World:

    def __init__(self):
        self.agents = []

    def add(self, *args):
        self.agents.extend(args)

    def genNext(self):
        for agent in self.agents:
            agent.act()


def gravity(d):
    return 1/pow(d, 2)

def movingG(a, b, d):
    return [(a.x-b.x)/d*gravity(d), (a.y-b.y)/d*gravity(d), (a.z-b.z)/d*gravity(d)]

def moving(a, b, d):
    return [(a.x-b.x)/d, (a.y-b.y)/d, (a.z-b.z)/d]

if __name__ == '__main__':
    world = World()
    [world.add(Agent()) for x in range(100)]
    print '\n'.join(map(str, world.agents))+'\ndone'
    for i in range(1000):
        world.genNext()
        print '\n'.join(map(str, world.agents))+'\ndone'

