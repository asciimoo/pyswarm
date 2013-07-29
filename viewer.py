import sys, os, os.path, soya, soya.cube
from threading import Thread

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


class SwarmEntity(soya.Body):
    def __init__(self, scene, model):
        soya.Body.__init__(self, scene, model)
        self.new_pos = (0.0, 0.0, 0.0)
        self.speed = soya.Vector(self, 0.0, 0.0, 0.0)

    def newpos(self, x, y, z):
        self.new_pos = soya.Point()
        self.new_pos.set_xyz(x, y, z)

    def begin_round(self):
        soya.Body.begin_round(self)
        self.speed = self.vector_to(self.new_pos)

    def advance_time(self, prop):
        soya.Body.advance_time(self, prop)
        self.add_mul_vector(prop, self.speed)


class Reader(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = False
        self.swarms = []

    def run(self):
        self.running = True
        while self.running:
            csw = {}
            while True:
                s = sys.stdin.readline().strip()
                if s == 'done':
                    break
                s = s.split()
                csw[s[0]] = {'coords': map(float, s[1:4]), 'color': s[4]}
            self.swarms.append(csw)

    def get_round(self):
        if len(self.swarms) > 0:
            return self.swarms.pop(0)
        else:
            return {}


def argparser():
    import argparse
    from sys import stdin
    argp = argparse.ArgumentParser(description='PyswarmViewer')
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
    argp.add_argument('-F', '--full-screen'
                     ,action    = 'store_true'
                     ,help      = 'Fullscreen mode'
                     ,default   = False
                     )
    argp.add_argument('-r', '--resolution'
                     ,help      = 'Resolution - default 800x600'
                     ,default   = '800x600'
                     ,action    = 'store'
                     ,type      = str
                     ,metavar   = 'WIDTHxHEIGHT'
                     )
    return vars(argp.parse_args())


# Main loop
class MainLoop(soya.MainLoop):
    cubes = {}
    def begin_round(self):
        soya.MainLoop.begin_round(self)
        if STOP:
            reader.running = False
            sys.exit()
        if not PAUSE:
            for name,swarm in reader.get_round().items():
                if not name in self.cubes.keys():
                    color = soya.Material()
                    color.diffuse = [int(swarm['color'][x:x+2], 16)/255.0 for x in range(0, len(swarm['color']), 2)]
                    cube = soya.cube.Cube(None, color, size=0.08).shapify()
                    self.cubes[name] = SwarmEntity(scene,cube)
                self.cubes[name].newpos(*swarm['coords'])


if __name__ == '__main__':
    args = argparser()
    args['resolution'] = map(int, args['resolution'].split('x'))
    FPS = args['fps']
    soya.init(title='SwarmViewer', fullscreen=args['full_screen'], width=args['resolution'][0], height=args['resolution'][1])
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
    cubes = {}
    reader = Reader()
    reader.start()
    MainLoop(scene).main_loop()
