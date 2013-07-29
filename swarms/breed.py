#!/usr/bin/env python

from swarm import Agent, World
from random import random

class RandomMoving(Agent):

    def init(self, world):
        self.rounds = 0.0
        self.world  = world
        self.cooldown = int(100*random())


    def act(self):
        c = 0
        move = None
        for agent in self.world.agents:
            if self == agent:
                continue
            dist = self.distance(agent)
            if dist < 10:
                c += 1
            if dist < 5 and dist > 1 and not move:
                move = [x/15 for x in self.vector_to(agent)]
        if self.cooldown == 0:
            if c > 2 and c < 50 and len(world.agents) < 1000:
                world.add(RandomMoving(color='FF0000FF', world=self.world))
            self.cooldown = 10
        else:
            self.cooldown -= 1
        if move:
            self.move(*move)
        else:
            self.move((random()-0.5)/2, (random()-0.5)/2, (random()-0.5)/2)


if __name__ == '__main__':
    world = World()
    [world.add(RandomMoving(world=world)) for x in range(10)]
    print '\n'.join(map(str, world.agents))+'\ndone'
    for i in range(1000):
        world.genNext()
        print '\n'.join(map(str, world.agents))+'\ndone'


