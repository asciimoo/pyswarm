#!/usr/bin/env python

from math import sin

from swarm import Agent, World

class SinAgent(Agent):

    def init(self):
        self.rounds = 0.0


    def act(self):
        self.x += sin(self.rounds+int(self.name.split('_')[1]))
        self.y -= sin(self.rounds)
        self.rounds += .1

if __name__ == '__main__':
    world = World()
    [world.add(SinAgent()) for x in range(1000)]
    print world
    for i in range(1000):
        print world.genNext()


