#!/usr/bin/env python


from swarm import Agent, World

if __name__ == '__main__':
    world = World()
    [world.add(Agent()) for x in range(100)]
    print world
    for i in range(1000):
        print world.genNext()


