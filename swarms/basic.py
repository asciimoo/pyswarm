#!/usr/bin/env python


from swarm import Agent, World

if __name__ == '__main__':
    world = World()
    [world.add(Agent()) for x in range(100)]
    print '\n'.join(map(str, world.agents))+'\ndone'
    for i in range(1000):
        world.genNext()
        print '\n'.join(map(str, world.agents))+'\ndone'


