#!/usr/bin/env python

from math import sin

from random import randint

from swarm import Agent, World

class SinAgent(Agent):

    def init(self, world):
        self.rounds = 0.0
        self.max_age = randint(1, 100)
        self.world = world
        self.color = 'FF00FFFF'


    def act(self):
        self.x += sin(self.rounds+int(self.name.split('_')[1]))
        self.y -= sin(self.rounds)
        self.rounds += .1
        if self.rounds > self.max_age:
            self.world.remove(self)

if __name__ == '__main__':
    world = World()
    [world.add(SinAgent(world=world)) for x in range(1000)]
    print world
    for i in range(1000):
        print world.genNext()


