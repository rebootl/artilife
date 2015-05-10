#!/usr/bin/python
#
# test drawing elements from gldraw2d
#
# using pyglet
#

import pyglet

from pyglet_draw_elements import *

window = pyglet.window.Window()


class Figure:

    def __init__(self):

        self.line = Line()

        self.circle = Circle()

        self.disk = Disk()
        # (modify some properties)
        self.disk.verts_colors[0] = 5
        self.disk.verts_colors[1] = 5
        self.disk.verts_colors[2] = 5

        self.rect = Rect((50,-100), filled=True)
        # (modify some properies)
        self.rect.verts_colors = (255, 255, 100) * 2 + (100, 255, 100) * 2

        self.ring = Ring((-20, 150))

        self.figure = Group((450, 200), 10)
        self.figure.shapes.append(self.line)
        self.figure.shapes.append(self.disk)
        self.figure.shapes.append(self.rect)
        self.figure.shapes.append(self.ring)


@window.event
def on_draw():
    window.clear()

    # draw single elements
    for pix in pixel_list:
        pix.draw()

    fig.line.draw()
    fig.circle.draw()

    # render the figure
    fig.figure.render()

# create single elements
pixel_list = []
for n in range(30):
    pix = Pixel((10+4*n, 10))
    pixel_list.append(pix)

# create figure
fig = Figure()

pyglet.app.run()
