#!/usr/bin/env python

from swarm import Agent, World
from random import random, shuffle

class RandomFollow(Agent):

    def init(self, world):
        self.rounds = 0.0
        self.world  = world


    def act(self):
        shuffle(self.world.agents)
        for agent in self.world.agents:
            if self == agent:
                continue
            dist = self.distance(agent)
            if dist < 5 and dist > 1:
                v = [x/15 for x in self.vector_to(agent)]
                self.move(*v)
                return
        self.move((random()-0.5)/2, (random()-0.5)/2, (random()-0.5)/2)


if __name__ == '__main__':
    world = World()
    [world.add(RandomFollow(world=world)) for x in range(100)]
    print '\n'.join(map(str, world.agents))+'\ndone'
    for i in range(1000):
        world.genNext()
        print '\n'.join(map(str, world.agents))+'\ndone'


