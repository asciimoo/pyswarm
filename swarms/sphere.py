#!/usr/bin/env python

from swarm import Agent, World

class RandomFollow(Agent):

    def init(self, world):
        self.rounds = 0.0
        self.world  = world


    def act(self):
        for agent in self.world.agents:
            if self == agent:
                continue
            dist = self.distance(agent)
            if dist > 5:
                v = [x/50 for x in self.vector_to(agent)]
                self.move(*v)
                return
            elif dist < 5:
                v = [x/50 for x in self.vector_to(agent, 1)]
                self.move(*v)
                return
            else:
                return


if __name__ == '__main__':
    world = World()
    [world.add(RandomFollow(world=world)) for x in range(1000)]
    print world
    for i in range(1000):
        print world.genNext()


