import math
import pyglet

from pyglet import gl




WIDTH = 256
HEIGHT = 256

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


window = pyglet.window.Window(WIDTH, HEIGHT)


def setup():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)


class Image(object):
    def __init__(self, width, height, base_color=None):
        base_color = base_color or (0, 0, 0)
        self.width = width
        self.height = height
        self.data = [
            [base_color for _ in xrange(height)] for _ in xrange(width)
        ]

    def getpixel(self, x_y):
        return self.data[int(x_y[0])][int(x_y[1])]

    def putpixel(self, x_y, val):
        self.data[x_y[0]][x_y[1]] = val

    def draw(self):
        points = []
        colors = []
        for x in xrange(self.width):
            for y in xrange(self.height):
                points.append(self.width - x)
                points.append(self.height - y)
                for v in self.data[x][y]:
                    colors.append(v)
        vertex_list = pyglet.graphics.vertex_list(
            self.width * self.height,
            ('v2i', points),
            ('c3B', colors))
        vertex_list.draw(gl.GL_POINTS)


def _map_range(x, min_from, max_from, min_to, max_to):
    return int(((x - min_from) * (max_to - min_to) /
                (max_from - min_from))
               + min_to)


def draw_circle(im):
    length = 50
    angle_stepsize = 0.1
    angle = 0
    while angle < 2 * math.pi:
        x = length * math.cos(angle)
        y = length * math.sin(angle)
        im.putpixel((int(x + WIDTH/2.0), int(y + HEIGHT/2.0)), WHITE)
        angle += angle_stepsize
    return im


def draw_fxn(im, fxn, color=WHITE):
    length = 50
    angle = 0
    angle_stepsize = 0.1
    while angle < 2 * math.pi:
        x = _map_range(angle, 0, 2.5*math.pi, 0, 255)
        y = length * fxn(angle)
        im.putpixel((int(x), int(y + HEIGHT/2.0)), color)
        angle += angle_stepsize
    return im


def draw_sin(im):
    return draw_fxn(im, math.sin)


def draw_cos(im):
    return draw_fxn(im, math.cos, color=RED)


def get_sprite():
    """Generate a sprite that is neat to see.

    Make brightness correspond to distance from center.
    """
    width = 32
    height = 32
    margin = 5
    data = []
    for i in xrange(width):
        if i < margin or (width - i ) < margin:
            data.append([BLACK for j in xrange(height)])
            continue
        data.append([])
        for j in xrange(height):
            if j < margin or (height - j) < margin:
                data[i].append(BLACK)
                continue
            cur_x = i
            cur_y = j
            mid_x = width / 2.0
            mid_y = height / 2.0
            dist = math.sqrt((cur_x - mid_x)**2 + (cur_y - mid_y)**2)
            max_dist = math.sqrt(mid_x**2 + mid_y**2)
            dist = abs(cur_x - mid_x) + abs(cur_y - mid_y)
            max_dist = mid_x + mid_y
            factor = 0.8 * (1 - dist / max_dist)
            data[i].append((int(255 * factor), int(255 * factor), 0))
    return data


def draw_sprites(im):
    sprite = get_sprite()
    width = len(sprite)
    height = len(sprite[0])
    for wide in xrange(WIDTH / width):
        for high in xrange(HEIGHT / height):
            im = draw_sprite(im, sprite, wide * width, high * height)
    return im


def draw_sprite(im, sprite, offset_x, offset_y):
    for i, col in enumerate(sprite):
        for j, val in enumerate(col):
            im.putpixel((offset_x + i, offset_y + j), val)
    return im


def rotate_im(im, angle, scale=1):
    start_x = 0
    start_y = 0
    new_im = Image(WIDTH, HEIGHT)
    dx = scale * math.cos(angle)
    dy = scale * math.sin(angle)
    for dest_y in xrange(HEIGHT):
        src_x = start_x
        src_y = start_y
        for dest_x in xrange(WIDTH):
            src_x %= WIDTH
            src_y %= HEIGHT
            val = im.getpixel((src_x, src_y))
            new_im.putpixel((dest_x, dest_y), val)
            src_x += dx
            src_y += dy
        start_x -= dy
        start_y += dx
    return new_im


def project_im(im, angle, cx=0, cy=0, scale_x=200.0, scale_y=200.0, space_z=100.0,
               horizon=10):
    new_im = Image(WIDTH, HEIGHT)
    for screen_y in xrange(HEIGHT):
        distance = (space_z * scale_y) / (screen_y + horizon)
        horizontal_scale = distance / scale_x

        line_dx = -math.sin(angle) * horizontal_scale
        line_dy = math.cos(angle) * horizontal_scale

        space_x = cx + (distance * math.cos(angle)) - WIDTH * line_dx / 2.0
        space_y = cy + (distance * math.sin(angle)) - WIDTH * line_dy / 2.0
        for screen_x in xrange(WIDTH):
            space_x %= WIDTH
            space_y %= HEIGHT
            val = im.getpixel((space_x, space_y))
            new_im.putpixel((screen_x, screen_y), val)
            space_x += line_dx
            space_y += line_dy
    return new_im


class ViewState(object):
    def __init__(self):
        self.angle = 0
        self.x = 0

    def change_angle(self, diff):
        self.angle += diff

    def change_x(self, diff):
        self.x += diff



VIEW_STATE = ViewState()


@window.event
def on_draw():
    setup()
    im = Image(WIDTH, HEIGHT)
    # im = draw_circle(im)
    # im = draw_sin(im)
    # im = draw_cos(im)
    # Sprites and sprite projection
    im = draw_sprites(im)
    # im = rotate_im(im, math.pi/4.0)
    im = project_im(im, VIEW_STATE.angle, cx=VIEW_STATE.x)
    # Racing car with key commands
    # Orbit
    # Draw circle efficiently
    # Homing missile w/ atan2
    my_im = Image(WIDTH, HEIGHT)
    for x in xrange(WIDTH):
        for y in xrange(HEIGHT):
            my_im.data[x][y] = im.getpixel((x, y))
    my_im.draw()

ANGLE_DELTA = math.pi / 30.0
X_DELTA = 100
SYMBOL2LAMBDA = {
    pyglet.window.key.LEFT: (lambda s: s.change_angle(ANGLE_DELTA)),
    pyglet.window.key.RIGHT: (lambda s: s.change_angle(-ANGLE_DELTA)),
    pyglet.window.key.UP: (lambda s: s.change_x(X_DELTA)),
    pyglet.window.key.DOWN: (lambda s: s.change_x(-X_DELTA)),

}



@window.event
def on_key_press(symbol, modifiers):
    global VIEW_STATE
    fxn = SYMBOL2LAMBDA.get(symbol)
    if not fxn:
        print symbol, modifiers
        return
    fxn(VIEW_STATE)


def main():
    pyglet.app.run()


if __name__ == '__main__':
    main()
