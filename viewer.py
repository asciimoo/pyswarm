import sys, os, os.path, soya, soya.cube
from threading import Thread

PAUSE = False
STOP  = False
FPS   = 10.0

class MovableCamera(soya.Camera):
    def __init__(self, parent, light):
        soya.Camera.__init__(self, parent)

        self.speed = soya.Vector(self)
        self.rotation_x_speed = 0.0
        self.rotation_y_speed = 0.0
        self.rotation_z_speed = 0.0
        self.light = light

    def begin_round(self):
        global PAUSE, STOP, FPS
        soya.Camera.begin_round(self)

        for event in soya.process_event():
            if event[0] == soya.sdlconst.KEYDOWN:
                if   event[1] == soya.sdlconst.K_w     : self.speed.z = -0.5
                elif event[1] == soya.sdlconst.K_s     : self.speed.z =  0.5
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
        self.light.set_xyz(self.x, self.y, self.z)


class SwarmEntity(soya.Body):
    def __init__(self, scene, model):
        soya.Body.__init__(self, scene, model)
        self.state1 = soya.CoordSystState(self)
        self.state2 = soya.CoordSystState(self)
        self.factor = 0.0

    def begin_round(self):
        self.factor = 0.0
        self.state1 = self.state2
        self.state2 = soya.CoordSystState(self)

    def advance_time(self, prop):
        self.factor += prop
        self.interpolate(self.state1, self.state2, self.factor)


class Reader(Thread):
    def __init__(self, input_file):
        Thread.__init__(self)
        self.input_file = input_file
        self.running = False
        self.swarms = []

    def run(self):
        self.running = True
        while self.running:
            csw = {}
            while True:
                s = self.input_file.readline().strip()
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
                     ,help      = 'Input file - default is STDIN'
                     ,metavar   = 'FILE'
                     ,default   = stdin
                     ,type      = argparse.FileType('r')
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

    def __init__(self, scene):
        soya.MainLoop.__init__(self, scene)
        self.round_duration = 1.0 / FPS

    def begin_round(self):
        soya.MainLoop.begin_round(self)
        if STOP:
            reader.running = False
            sys.exit()
        if not PAUSE:
            swarms = reader.get_round()
            if not len(swarms):
                return
            cube_keys = self.cubes.keys()
            for name,swarm in swarms.items():
                if not name in self.cubes.keys():
                    color = soya.Material()
                    color.diffuse = [int(swarm['color'][x:x+2], 16)/255.0 for x in range(0, len(swarm['color']), 2)]
                    cube = soya.cube.Cube(None, color, size=0.08).shapify()
                    self.cubes[name] = SwarmEntity(scene,cube)
                else:
                    cube_keys.remove(name)
                p = soya.Point(scene)
                p.set_xyz(*swarm['coords'])
                self.cubes[name].state2.move(p)
            for swarm in cube_keys:
                scene.remove(self.cubes.pop(swarm))


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

    soya.cursor_set_visible(0)

    #scene.atmosphere = soya.Atmosphere()
    #scene.atmosphere.ambient = (0.0, 1.0, 1.0, 1.0)

    camera = MovableCamera(scene, light)
    camera.set_xyz(-10.0, 4.0, 10.0)
    camera.fov = 140.0
    soya.set_root_widget(camera)
    cubes = {}
    reader = Reader(args['input'])
    reader.start()
    MainLoop(scene).main_loop()
