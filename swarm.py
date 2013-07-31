#!/usr/bin/env python

import random
from math import sqrt

def _parse_coords(coords):
    if type(coords) == list:
        x = coords[0]
        y = coords[1]
        z = coords[2]
    elif type(coords) == dict:
        x = coords['x']
        y = coords['y']
        z = coords['z']
    else:
        x = coords.x
        y = coords.y
        z = coords.z
    return x, y, z

class Agent:

    count = 0

    def __init__(self, name='Bond', resolution=1, x=None, y=None, z=None, color="FFFFFFFF", **kwargs):
        self.name  = '{:s}_{:0>4d}'.format(name, Agent.count)
        self.color = color
        self.x     = (random.random()-0.5)*pow(10, resolution)*2 if x == None else x
        self.y     = (random.random()-0.5)*pow(10, resolution)*2 if y == None else y
        self.z     = (random.random()-0.5)*pow(10, resolution)*2 if z == None else z
        self.type  = self.__class__.__name__
        Agent.count += 1
        if hasattr(self, 'init'):
            self.init(**kwargs)

    def __str__(self): return '{:s} {:.8f} {:.8f} {:.8f} {:s}'.format(self.name, self.x, self.y, self.z, self.color)

    def act(self):
        pass



    def distance(self, bgent):
        x, y, z = _parse_coords(bgent)
        return sqrt(pow(self.x-x, 2)+pow(self.y-y, 2)+pow(self.z-z, 2))

    def move_to(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        return self

    def vector_to(self, bgent, d=-1):
        x, y, z = _parse_coords(bgent)
        d = float(d)
        return [(self.x-x)/d, (self.y-y)/d, (self.z-z)/d]

    def move(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z
        return self

    def merge_vectors(self, vectors):
        iv = [0, 0, 0]
        iv_len = len(vectors)
        for x,y,z in vectors:
            iv[0] += x
            iv[1] += y
            iv[2] += z
        return iv[0]/iv_len, iv[1]/iv_len, iv[2]/iv_len

def round_coords(agent, prec_x=2, prec_y=2, prec_z=2):
    return round(agent.x, prec_x), round(agent.y, prec_y), round(agent.z, prec_z)

class Zones():

    def __init__(self, precisions=(2,2,2)):
        self.precisions = precisions
        self.zones = { }

    def add(self, agent):
        x, y, z = round_coords(agent, *self.precisions)
        if self.zones.get(x) == None:
            self.zones[x] = {}
        if self.zones[x].get(y) == None:
            self.zones[x][y] = {}
        if self.zones[x][y].get(z) == None:
            self.zones[x][y][z] = [agent]
        elif agent not in self.zones[x][y][z]:
            self.zones[x][y][z].append(agent)

    def remove(self, agent):
        x, y, z = round_coords(agent, *self.precisions)
        # TODO garbage collection - empty lists/dicts
        if not self.zones.get(x):
            return
        if not self.zones[x].get(y):
            return
        if not self.zones[x][y].get(z):
            return
        if not agent in self.zones[x][y][z]:
            return
        self.zones[x][y][z].remove(agent)

    def get_xyz(self, x, y, z):
        if not self.zones.get(x):
            return []
        if not self.zones[x].get(y):
            return []
        if not self.zones[x][y].get(z):
            return []
        return self.zones[x][y][z]

    def get_nearby(self, agent, distance=0):
        x, y, z = round_coords(agent, *self.precisions)
        agents = set()
        for agent in self.get_xyz(x, y, z):
            agents.add(agent)
        return list(agents)


class World:

    def __init__(self, zone_precisions=(2,2,2)):
        self.agents = []
        self.zones = Zones(precisions=zone_precisions)

    def add(self, *args):
        for agent in args:
            if not hasattr(self, agent.type):
                setattr(self, agent.type, [])
            getattr(self, agent.type).append(agent)
            self.agents.append(agent)
            self.zones.add(agent)

    def genNext(self):
        for agent in self.agents:
            # TODO zones optimization - skip non moving acts
            self.zones.remove(agent)
            agent.act()
            self.zones.add(agent)
        return self

    def __repr__(self):
        return '\n'.join(map(str, self.agents))+'\ndone'


def gravity(d):
    return 1/pow(d, 2)

def movingG(a, b, d):
    return [(a.x-b.x)/d*gravity(d), (a.y-b.y)/d*gravity(d), (a.z-b.z)/d*gravity(d)]

def moving(a, b, d):
    return [(a.x-b.x)/d, (a.y-b.y)/d, (a.z-b.z)/d]

if __name__ == '__main__':
    world = World()
    [world.add(Agent()) for x in range(100)]
    print world
    for i in range(1000):
        print world.genNext()

