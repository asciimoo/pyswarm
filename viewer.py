import sys, os, os.path, soya, soya.cube
from time import sleep

PAUSE = False
STOP = False

class MovableCamera(soya.Camera):
    def __init__(self, parent):
        soya.Camera.__init__(self, parent)

        self.speed = soya.Vector(self)
        self.rotation_y_speed = 0.0
        self.rotation_x_speed = 0.0

    def begin_round(self):
        global PAUSE, STOP
        soya.Camera.begin_round(self)

        for event in soya.process_event():
            if event[0] == soya.sdlconst.KEYDOWN:
                if   event[1] == soya.sdlconst.K_UP:     self.speed.z = -0.1
                elif event[1] == soya.sdlconst.K_DOWN:   self.speed.z =  0.1
                elif event[1] == soya.sdlconst.K_LEFT:   self.rotation_y_speed =  1.0
                elif event[1] == soya.sdlconst.K_RIGHT:  self.rotation_y_speed = -1.0
                elif event[1] == soya.sdlconst.K_q:      STOP = True
                elif event[1] == soya.sdlconst.K_ESCAPE: STOP = True
                elif event[1] == soya.sdlconst.K_SPACE : PAUSE = not PAUSE
            if event[0] == soya.sdlconst.KEYUP:
                if   event[1] == soya.sdlconst.K_UP:     self.speed.z = 0.0
                elif event[1] == soya.sdlconst.K_DOWN:   self.speed.z = 0.0
                elif event[1] == soya.sdlconst.K_LEFT:   self.rotation_y_speed = 0.0
                elif event[1] == soya.sdlconst.K_RIGHT:  self.rotation_y_speed = 0.0

    def advance_time(self, proportion):
        self.add_mul_vector(proportion, self.speed)
        self.turn_y(self.rotation_y_speed * proportion)
        self.turn_x(self.rotation_x_speed * proportion)

def read_swarms():
    swarms = []
    while True:
        s = raw_input().strip()
        if s == 'done':
            break
        swarms.append(map(float, s.split()))
    return swarms


soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

# Creates the scene.

scene = soya.World()

light = soya.Light(scene)
light.set_xyz(0.0, 0.2, 1.0)

camera = MovableCamera(scene)
camera.set_xyz(-10.0, 4.0, 10.0)
camera.fov = 140.0
soya.set_root_widget(camera)


swarms = read_swarms()

cube = soya.cube.Cube(None, size=0.1).shapify()
cubes = []
for i,swarm in enumerate(swarms):
    cubes.append(soya.Body(scene,cube))
    cubes[i].set_xyz(*swarms[i])



# Creates the ray.



# Main loop
class MainLoop(soya.MainLoop):
    def begin_round(self):
        #swarms = read_swarms()
        #print 'asdf'
        #for i,swarm in enumerate(swarms):
        #    cubes[i].set_xyz(*swarms[i])
        soya.MainLoop.begin_round(self)



ml = MainLoop(scene)

print dir(soya.MAIN_LOOP)

while not STOP:
    if not PAUSE:
        swarms = read_swarms()
        for i,swarm in enumerate(swarms):
            cubes[i].set_xyz(*swarms[i])
    sleep(1/10.)
    ml.update()
