#!/usr/bin/python
#
# basic 2-D drawing elements and grouping for pyglet
#
# using pyglet (OpenGL)
#
#
# the way to use this is as following:
# - use the basic drawing elements to define a figure
# - create a group to hold the single elements
#   and add the elements to the group
# - render the group
#
# (+) the group can be moved and rotated around ! (suitable for animations,
#     designed as such, but not tested yet)
# (+) only using gl triangles and lines
# (-) currently every basic drawing element implements
#     it's own draw method, which might be slow, but
#     offers more flexibility <-- changed, they're not used
#     when rendered from a group (the group renders the elements on it's own)
# (-) not using pyglet's list_array(?) VBO (?), yet...
#
# --> change rgb to rgba ! (must)
#
# cem, 2015-05-10
#

import pyglet
import math

class Pixel:

    def __init__(self, pos=(10, 10), color=(255, 255, 255)):

        self.x = pos[0]
        self.y = pos[1]

        self.n_verts = 1

        self.color = color
        self.verts_colors = color

        self.gl_prim_mode = pyglet.gl.GL_POINTS
        self.indexed = False

    def draw(self):

        pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
                            ('v2i', (self.x, self.y)),
                            ('c3B', self.color))


class Line:

    def __init__(self, start=(10, 10), end=(150, 150), color=(255, 255, 255)):

        self.start = start
        self.end = end

        self.n_verts = 2
        self.verts = (start[0], start[1], end[0], end[1])

        self.color = color
        self.verts_colors = color * 2

        self.gl_prim_mode = pyglet.gl.GL_LINES
        self.indexed = False

    def draw(self):

        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                            ('v2i', self.verts),
                            ('c3B', self.verts_colors))


class MultiLine:

    def __init__(self, verts, color, closed=False):

        self.n_verts = len(verts) / 2
        self.verts = verts

        self.color = color
        self.verts_color = color * self.n_verts

        if not closed:
            self.gl_prim_mode = pyglet.gl.GL_LINES
        else:
            self.gl_prim_mode = pyglet.gl.GL_LINE_LOOP

        self.indexed = False


class Circle:

    def __init__(self, center=(300, 300), radius=100, color=(0, 0, 255), segments=20):
        self.center = center
        self.radius = radius

        self.segments = segments

        self.n_verts = segments
        self.create_mesh()
#        self.verts = self.create_mesh(center, radius, segments)

        self.color = color
        self.verts_colors = color * segments

        self.gl_prim_mode = pyglet.gl.GL_LINE_LOOP
        self.indexed = False

    def create_mesh(self):

        center = self.center
        r = self.radius
        segments = self.segments

        segment_angle = 2 * math.pi / segments

        verts = []
        for n in range(segments):

            alpha = n * segment_angle

            verts.append( center[0] + round(r*math.cos(alpha)) )
            verts.append( center[1] + round(r*math.sin(alpha)) )

        self.verts = verts

    def draw(self):

        pyglet.graphics.draw(self.segments, pyglet.gl.GL_LINE_LOOP,
                            ('v2i', self.verts),
                            ('c3B', self.verts_colors))


class Disk:

    def __init__(self, center=(0, 0), radius=100, color=(180, 180, 120), segments=20):
        self.center = center
        self.radius = radius

        self.segments = segments

        self.n_verts = segments + 1

        self.create_mesh()
        self.create_index()

        self.color = color
        # (use list to allow editing)
        self.verts_colors = list(color * self.n_verts)

        self.gl_prim_mode = pyglet.gl.GL_TRIANGLES
        self.indexed = True

    def create_mesh(self):

        # (make locals for performance)
        center = self.center
        r = self.radius
        segments = self.segments

        segment_angle = 2 * math.pi / segments

        verts = [ center[0], center[1] ]
        for n in range(segments):

            alpha = n * segment_angle

            verts.append( center[0] + round(r*math.cos(alpha)) )
            verts.append( center[1] + round(r*math.sin(alpha)) )

        self.verts = verts

    def create_index(self):

        segments = self.segments

        verts_index = []
        # (leave last segment open)
        for n in range(segments-1):

            triangle_index = [ 0, n+1, n+2 ]
            verts_index += triangle_index

        # (connect last segment to start)
        verts_index += [ 0, segments, 1 ]

        self.verts_index = verts_index

    def draw(self):

        pyglet.graphics.draw_indexed(self.n_verts,
                            pyglet.gl.GL_TRIANGLES,
                            self.verts_index,
                            ('v2i', self.verts),
                            ('c3B', self.verts_colors))


class Ring:

    def __init__(self, center=(0, 0), radius_outer=100, radius_inner=90, color=(80, 1180, 150), segments=50):

        self.center = center
        self.r_out = radius_outer
        self.r_in = radius_inner

        self.segments = segments

        self.n_verts = segments * 2

        self.create_mesh()
        self.create_index()

        self.color = color
        # (use list to allow editing)
        self.verts_colors = list(color * self.n_verts)

        self.gl_prim_mode = pyglet.gl.GL_TRIANGLES
        self.indexed = True    

    def create_mesh(self):

        # (make locals for performance)
        center = self.center
        segments = self.segments
        r_out = self.r_out
        r_in = self.r_in

        segment_angle = 2 * math.pi / segments

        verts = []
        for n in range(segments):

            alpha = n * segment_angle

            verts.append( center[0] + round(r_out*math.cos(alpha)) )
            verts.append( center[1] + round(r_out*math.sin(alpha)) )

        for n in range(segments):

            alpha = n * segment_angle

            verts.append( center[0] + round(r_in*math.cos(alpha)) )
            verts.append( center[1] + round(r_in*math.sin(alpha)) )

        self.verts = verts

    def create_index(self):

        segments = self.segments
        r_out = self.r_out
        r_in = self.r_in

        verts_index = []
        # (leave last segment open)
        for n in range(segments-1):

            # (first ring of triangles [ 0, 1, 4, ... ])
            verts_index += [ n, n+1, segments+n ]
            # (second ring of triangles [ 4, 1, 5, ... ])
            verts_index += [ segments+n, n+1, segments+n+1 ]
            #verts_index += triangle_index

        # (connect last segment to start)
        verts_index += [ segments-1, 0, segments*2-1 ]
        verts_index += [ segments*2-1, 0, segments ]

        self.verts_index = verts_index


class Rect:

    def __init__(self, center=(0,0), size=(200, 100), color=(255, 0, 0), filled=False):
        self.center = center
        self.size = size
        self.width = size[0]
        self.height = size[1]

        self.n_verts = 4
        self.create_mesh()
#        self.verts = self.create_mesh(center, size[0], size[1])

        self.color = color
        self.verts_colors = color * 4

        if not filled:
            self.gl_prim_mode = pyglet.gl.GL_LINE_LOOP
            self.indexed = False
        else:
            self.gl_prim_mode = pyglet.gl.GL_TRIANGLES
            self.indexed = True

            self.verts_index = ( 0, 1, 2, 2, 3, 0 )

    def create_mesh(self):
 
        c_x = self.center[0]
        c_y = self.center[1]
        width = self.width
        height = self.height

        self.verts = ( c_x-width/2, c_y-height/2,
                    c_x+width/2, c_y-height/2,
                    c_x+width/2, c_y+height/2,
                    c_x-width/2, c_y+height/2 )

    # alternative: use return in create_mesh and update_mesh --> evtl. test perform.
    #def update_mesh(self):
    #    self.verts = self.create_mesh(self.center, self.width, self.height)


class LRect:
    '''Draws a rectangle with the given width, from point 1 to point 2.
Can therefor be used to draw bold lines ;) .'''
    # .. todo..
    pass

class Shape:
    '''Unicolor shape, build from triangles.
To use multiple colors easily set <inst>.verts_colors.'''

    def __init__(self, verts, verts_index, color=(255, 255, 255)):

        self.n_verts = len(verts) / 2
        self.verts = verts
        self.verts_index = verts_index

        self.color = color
        self.verts_color = color * self.n_verts

        self.gl_prim_mode = pyglet.gl.GL_TRIANGLES
        self.indexed = True


class Group:

    def __init__(self, position, angle):

        self.position = position
        self.angle = angle

        self.shapes = []

    def render(self):

        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(self.position[0], self.position[1], 0)
        pyglet.gl.glRotatef(self.angle, 0, 0, 1)

        for shape in self.shapes:
            if not shape.indexed:
                # (call draw here, avoids function call, (+) performance hopefully)
                pyglet.graphics.draw(shape.n_verts, shape.gl_prim_mode,
                            ('v2f', shape.verts),
                            ('c3B', shape.verts_colors))
            else:
                pyglet.graphics.draw_indexed(shape.n_verts, shape.gl_prim_mode,
                            shape.verts_index,
                            ('v2f', shape.verts),
                            ('c3B', shape.verts_colors))

#            shape.draw()
#            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
#                            ('v2f', shape.verts),
#                            ('c3B', shape.colors))
        pyglet.gl.glPopMatrix()
