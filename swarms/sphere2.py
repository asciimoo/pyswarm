#!/usr/bin/env python

from swarm import Agent, World

class Cubic(Agent):

    def init(self, world):
        self.rounds = 0.0
        self.world  = world


    def act(self):
        nearbys = self.world.zones.get_nearby(self, 2)
        vectors = []
        for agent in nearbys:
            if self == agent:
                continue
            dist = self.distance(agent)
            if dist < 1:
                vectors.append(self.vector_to(agent, 1))
        dist = self.distance([0.5, 0.5, 0.5])
        if len(vectors):
            self.move(*[x/15 for x in self.merge_vectors(vectors)])
        else:
            new_coords = [x/(dist*5) for x in self.vector_to([0.5, 0.5, 0.5])]
            self.move(*new_coords)

class Spheric(Agent):

    def init(self, world):
        self.rounds = 0.0
        self.world  = world
        self.color  = '00FF00FF'


    def act(self):
        nearbys = self.world.zones.get_nearby(self, 2)
        vectors = []
        for agent in nearbys:
            if self == agent:
                continue
            dist = self.distance(agent)
            if dist < 1:
                if agent.type == self.type:
                    vectors.append(self.vector_to(agent, 1))
            elif agent.type != self.type:
                vectors.append(self.vector_to(agent, -1))
        dist = self.distance([2.5, -0.5, 1.5])
        if len(vectors):
            self.move(*[x/15 for x in self.merge_vectors(vectors)])
        else:
            new_coords = [x/(dist*5) for x in self.vector_to([2.5, -0.5, 1.5])]
            self.move(*new_coords)


if __name__ == '__main__':
    world = World(zone_precisions=(-1,-1,-1))
    [world.add(Cubic(world=world)) for x in range(100)]
    [world.add(Spheric(world=world)) for x in range(100)]
    print world
    for i in range(1000):
        print world.genNext()


