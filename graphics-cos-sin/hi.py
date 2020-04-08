import pyglet
from pyglet import gl


window = pyglet.window.Window()
# pyglet.graphics.draw(
#     2, pyglet.gl.GL_POINTS,
#     ('v2i', (10, 15, 30, 35))
# )

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

    def draw(self):
        points = []
        colors = []
        for x in xrange(self.width):
            for y in xrange(self.height):
                points.append(x)
                points.append(y)
                for v in self.data[x][y]:
                    colors.append(v)
        vertex_list = pyglet.graphics.vertex_list(
            self.width * self.height,
            ('v2i', points),
            ('c3B', colors))
        vertex_list.draw(gl.GL_POINTS)




def draw():
    image = Image(300, 300)
    for i in range(50):
        for j in range(50):
            color = int(2.56 * (i + j))
            image.data[i][j] = (color, color, color)
    image.draw()


@window.event
def on_draw():
    setup()
    draw()
    # gl.glBegin(gl.GL_POINTS)
    # gl.glVertex2i(50, 50)
    # gl.glVertex2i(75, 100)
    # gl.glVertex2i(100, 150)
    # gl.glVertex2i(200, 200)
    # gl.glEnd()


if __name__ == '__main__':
    # draw()
    # pyglet.graphics.draw(2, gl.GL_POINTS,
    #                      ('v3f', (10, 15, 5, 30, 35, 5)),
    #                      ('c3B', (0, 120, 120, 255, 120, 120)),
    #                     )
    # draw_triangle()
    pyglet.app.run()
