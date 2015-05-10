#!/usr/bin/python
#
# draw opengl triangle
#
# adapted from: http://tartley.com/files/stretching_pyglets_wings/presentation/
#

import pyglet
from pyglet.gl import *


window = pyglet.window.Window()

def triangle():
#    verts = [ (window.width * 0.9, window.height * 0.9),
#          (window.width * 0.5, window.height * 0.1),
#          (window.width * 0.1, window.height * 0.9) ]

#    colors = [ (255, 000, 000),
#           (000, 255, 000),
#           (000, 000, 255) ]

#    glBegin(GL_TRIANGLES)
#    for idx in range(len(verts)):
#        glColor3ub(colors[idx][0], colors[idx][1], colors[idx][2])
#        glVertex2f(verts[idx][0], verts[idx][1])
#    glEnd()

    # (alternative notation)
    verts = [ window.width * 0.9, window.height * 0.9,
          window.width * 0.5, window.height * 0.1,
          window.width * 0.1, window.height * 0.9 ]

    colors = [ 255, 000, 000,
           000, 255, 000,
           000, 000, 255 ]

    pyglet.graphics.draw(3, GL_TRIANGLES,
                        ('v2f', verts),
                        ('c3B', colors), )

@window.event
def on_draw():
    window.clear()
    triangle()

pyglet.app.run()
