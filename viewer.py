import sys, os, os.path, soya, soya.cube
from time import sleep

PAUSE = False
STOP  = False
FPS   = 10.0

class MovableCamera(soya.Camera):
    def __init__(self, parent):
        soya.Camera.__init__(self, parent)

        self.speed = soya.Vector(self)
        self.rotation_x_speed = 0.0
        self.rotation_y_speed = 0.0
        self.rotation_z_speed = 0.0

    def begin_round(self):
        global PAUSE, STOP, FPS
        soya.Camera.begin_round(self)

        for event in soya.process_event():
            if event[0] == soya.sdlconst.KEYDOWN:
                if   event[1] == soya.sdlconst.K_w     : self.speed.z = -0.1
                elif event[1] == soya.sdlconst.K_s     : self.speed.z =  0.1
                elif event[1] == soya.sdlconst.K_e     : self.rotation_x_speed =  1.0
                elif event[1] == soya.sdlconst.K_q     : self.rotation_x_speed = -1.0
                elif event[1] == soya.sdlconst.K_a     : self.rotation_y_speed =  1.0
                elif event[1] == soya.sdlconst.K_d     : self.rotation_y_speed = -1.0
                elif event[1] == soya.sdlconst.K_q     : STOP = True
                elif event[1] == soya.sdlconst.K_ESCAPE: STOP = True
                elif event[1] == soya.sdlconst.K_SPACE : PAUSE = not PAUSE
                elif event[1] == soya.sdlconst.K_PLUS  : FPS += 1
                elif event[1] == soya.sdlconst.K_MINUS : FPS -= 1
                else: print event[1]
            if event[0] == soya.sdlconst.KEYUP:
                if   event[1] == soya.sdlconst.K_w  : self.speed.z = 0.0
                elif event[1] == soya.sdlconst.K_s  : self.speed.z = 0.0
                elif event[1] == soya.sdlconst.K_e  : self.rotation_x_speed = 0.0
                elif event[1] == soya.sdlconst.K_q  : self.rotation_x_speed = 0.0
                elif event[1] == soya.sdlconst.K_a  : self.rotation_y_speed = 0.0
                elif event[1] == soya.sdlconst.K_d  : self.rotation_y_speed = 0.0

    def advance_time(self, proportion):
        self.add_mul_vector(proportion, self.speed)
        self.turn_y(self.rotation_y_speed * proportion)
        self.turn_x(self.rotation_x_speed * proportion)

def read_swarms():
    global sys
    swarms = {}
    while True:
        s = sys.stdin.readline().strip()
        if s == 'done':
            break
        s = s.split()
        swarms[s[0]] = {'coords': map(float, s[1:4]), 'color': s[4]}
    return swarms

def argparser():
    import argparse
    from sys import stdin
    argp = argparse.ArgumentParser(description='exrex - regular expression string generator')
    argp.add_argument('-i', '--input'
                     ,help      = 'Output file - default is STDIN'
                     ,metavar   = 'FILE'
                     ,default   = stdin
                     ,type      = argparse.FileType('w')
                     )
    argp.add_argument('-f', '--fps'
                     ,help      = 'Reading speed - default is 10'
                     ,default   = 10.0
                     ,action    = 'store'
                     ,type      = float
                     ,metavar   = 'N'
                     )
    return vars(argp.parse_args())

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

# Creates the scene.

scene = soya.World()

light = soya.Light(scene)
light.set_xyz(10.0, 10.2, 11.0)

#scene.atmosphere = soya.Atmosphere()
#scene.atmosphere.ambient = (0.0, 1.0, 1.0, 1.0)

camera = MovableCamera(scene)
camera.set_xyz(-10.0, 4.0, 10.0)
camera.fov = 140.0
soya.set_root_widget(camera)

# Main loop
class MainLoop(soya.MainLoop):
    def begin_round(self):
        soya.MainLoop.begin_round(self)



if __name__ == '__main__':
    args = argparser()
    FPS = args['fps']
    cubes = {}
    ml = MainLoop(scene)
    while not STOP:
        if not PAUSE:
            swarms = read_swarms()
            for name,swarm in swarms.items():
                if not name in cubes.keys():
                    color = soya.Material()
                    color.diffuse = [int(swarm['color'][x:x+2], 16)/255.0 for x in range(0, len(swarm['color']), 2)]
                    cube = soya.cube.Cube(None, color, size=0.08).shapify()
                    cubes[name] = soya.Body(scene,cube)
                cubes[name].set_xyz(*swarms[name]['coords'])
            if FPS > 0:
                sleep(1/FPS)
        ml.update()
