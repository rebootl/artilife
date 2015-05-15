#!/usr/bin/python
#
# test drawing elements from gldraw2d
#
# using pyglet
#

import pyglet

from pyglet_draw_elements import *

window = pyglet.window.Window()

def deg2rad(a_deg):
    return math.pi/180 * a_deg

def rad2deg(a_rad):
    return 180/math.pi * a_rad


class Figure:

    def __init__(self):

        self.line = Line()

        self.rect = Rect((50,-100))
        # (modify some properies)
        self.rect.verts_colors = (255, 255, 100) * 2 + (100, 255, 100) * 2


        self.figure = Group((450, 200), 0)
        self.figure.shapes.append(self.line)
        self.figure.shapes.append(self.rect)
#        self.figure.shapes.append(self.ring)
#        self.figure.shapes.append(self.diskarc)

        self.fig1 = Group((20, 20), 10)

        self.circle = Circle((120, 300))
        self.arc = Arc((300, 300))

        self.disk = Disk((500, 300))
        # (modify some properties)
        self.disk.verts_colors[0] = 5
        self.disk.verts_colors[1] = 5
        self.disk.verts_colors[2] = 5

        self.diskarc = DiskArc((240, 300), radius=80)

        self.sline = StrokeLine()

        self.lrect = LineRect((175, 25))

        self.ring = Ring((200, 150))

        self.sring = StrokeRing((230, 130))

        self.fig1.shapes.append(self.circle)
        self.fig1.shapes.append(self.arc)
        self.fig1.shapes.append(self.disk)
        self.fig1.shapes.append(self.diskarc)
        self.fig1.shapes.append(self.sline)
        self.fig1.shapes.append(self.lrect)
        self.fig1.shapes.append(self.ring)
        self.fig1.shapes.append(self.sring)


@window.event
def on_draw():
    window.clear()

    # draw single elements
    #for pix in pixel_list:
    #    pix.draw()

    #fig.line.draw()
    #fig.circle.draw()

    # render the figure
    fig.figure.render()
    fig.fig1.render()

# create single elements
pixel_list = []
for n in range(30):
    pix = Pixel((10+4*n, 10))
    pixel_list.append(pix)

# create figure
fig = Figure()

pyglet.app.run()
