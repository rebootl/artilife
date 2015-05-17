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
# --> change rgb to rgba !
# --> reorganize the elements ==> OK
#
# cem, 2015-05-10
#

import pyglet
import math

### point elements

class Pixel:

    def __init__(self, pos=(10, 10), color=(255, 255, 255)):
        self.x = pos[0]
        self.y = pos[1]

        self.n_verts = 1

        self.color = color
        self.verts_colors = color

        self.gl_prim_mode = pyglet.gl.GL_POINTS
        self.indexed = False

### line elements

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


class LineRect:

    def __init__(self, center=(0,0), size=(200, 100), color=(0, 255, 0)):
        self.center = center
        self.size = size
        self.width = size[0]
        self.height = size[1]

        self.n_verts = 4
        self.verts = create_rect_verts(center, size)

        self.color = color
        self.verts_colors = color * 4

        self.gl_prim_mode = pyglet.gl.GL_LINE_LOOP
        self.indexed = False


class Circle:

    def __init__(self, center=(0, 0), radius=100, color=(0, 0, 255),
                 segments=20):
        self.center = center
        self.radius = radius

        self.segments = segments

        self.n_verts = segments

        self.verts = create_circle_verts(center, radius, segments)

        self.color = color
        self.verts_colors = color * self.n_verts

        self.gl_prim_mode = pyglet.gl.GL_LINE_LOOP
        self.indexed = False


class Arc:

    def __init__(self, center=(0, 0), radius=100, alpha_1=0, alpha_2=math.pi,
                 color=(200, 0, 255), segments=10):
        self.center = center
        self.radius = radius

        self.alpha_1 = alpha_1
        self.alpha_2 = alpha_2

        self.segments = segments

        self.n_verts = segments+1
        self.verts = create_arc_verts(center, radius, alpha_1, alpha_2, segments)
        self.color = color
        self.verts_colors = color * self.n_verts

        self.gl_prim_mode = pyglet.gl.GL_LINE_STRIP
        self.indexed = False

### surface elements

class StrokeLine:

    def __init__(self, start=(0,0), end=(80, 60), width=8, color=(130,130,150)):
        self.start = start
        self.end = end
        self.width = width

        self.n_verts = 4

        self.verts = create_tiltrect_verts(start, end, width)
        self.verts_index = ( 0, 1, 2, 1, 2, 3 )

        self.color = color
        self.verts_colors = color * 4

        self.gl_prim_mode = pyglet.gl.GL_TRIANGLES
        self.indexed = True


class Rect:

    def __init__(self, center=(0,0), size=(200, 100), color=(255, 0, 0)):
        self.center = center
        self.size = size
        self.width = size[0]
        self.height = size[1]

        self.n_verts = 4
        self.verts = create_rect_verts(center, size)

        self.color = color
        self.verts_colors = color * 4

        self.gl_prim_mode = pyglet.gl.GL_TRIANGLES
        self.indexed = True

        self.verts_index = ( 0, 1, 2, 2, 3, 0 )


class Shape:

    def __init__(self, verts, verts_index, color=(255, 255, 255)):
        self.n_verts = len(verts) / 2
        self.verts = verts
        self.verts_index = verts_index

        self.color = color
        self.verts_color = color * self.n_verts

        self.gl_prim_mode = pyglet.gl.GL_TRIANGLES
        self.indexed = True


class Disk:

    def __init__(self, center=(0, 0), radius=100, color=(180, 180, 120),
                 segments=20):
        self.center = center
        self.radius = radius

        self.segments = segments

        self.n_verts = segments + 1

        # (insert center vertice)
        self.verts = [ center[0], center[1] ]
        self.verts.extend(create_circle_verts(center, radius, segments))

        self.verts_index = create_radial_index(segments-1)
        # (connect last segment to start)
        self.verts_index += [ 0, segments, 1 ]

        self.color = color
        # (use list to allow editing)
        self.verts_colors = list(color * self.n_verts)

        self.gl_prim_mode = pyglet.gl.GL_TRIANGLES
        self.indexed = True


class DiskArc:

    def __init__(self, center=(0, 0), radius=100, alpha_1=0.0, alpha_2=math.pi,
                 color=(180, 120, 180), segments=8):
        self.center = center
        self.radius = radius

        self.alpha_1 = alpha_1
        self.alpha_2 = alpha_2

        self.segments = segments

        self.n_verts = segments + 2

        self.verts = [ center[0], center[1] ]
        self.verts.extend(create_arc_verts(center, radius, alpha_1, alpha_2,
                                           segments))

        self.verts_index = create_radial_index(segments)

        self.color = color
        # (use list to allow editing)
        self.verts_colors = list(color * self.n_verts)

        self.gl_prim_mode = pyglet.gl.GL_TRIANGLES
        self.indexed = True


class RingBase:

    def __init__(self, center=(0, 0), radius_outer=100, radius_inner=90,
                 color=(80, 1180, 150), segments=50):
        self.center = center
        self.r_out = radius_outer
        self.r_in = radius_inner

        self.segments = segments

        self.n_verts = segments * 2

        # create mesh
        self.verts = create_circle_verts(center, radius_outer, segments)
        self.verts += create_circle_verts(center, radius_inner, segments)

        self.create_index()

        self.color = color
        # (use list to allow editing)
        # --> store inner and outer verts_colors,
        #     this way it's very easy to make a radial gradient (+++)
        self.verts_colors = list(color * self.n_verts)

        self.gl_prim_mode = pyglet.gl.GL_TRIANGLES
        self.indexed = True    

    def create_index(self):
        segments = self.segments
        #r_out = self.r_out
        #r_in = self.r_in

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


class Ring(RingBase):

    def __init__(self, center=(0, 0), radius_outer=100, radius_inner=90,
                 color=(80, 180, 150), segments=50):

        super().__init__(center, radius_outer, radius_inner, color, segments)


class StrokeRing(RingBase):

    def __init__(self, center=(0, 0), radius=120, width=5,
                 color=(200, 180, 160), segments=30):

        r_out = radius + width/2
        r_in = radius - width/2

        super().__init__(center, r_out, r_in, color, segments)


class RingArcBase:

    def __init__(self, center=(0, 0), radius_outer=100, radius_inner=80,
                 alpha_1=0, alpha_2=math.pi, color=(200, 0, 255), segments=10):

        self.center = center
        self.radius_outer = radius_outer
        self.radius_inner = radius_inner

        self.alpha_1 = alpha_1
        self.alpha_2 = alpha_2

        self.segments = segments

        self.n_verts = segments * 2 + 2
        # (debug-print)
        #print("n_verts: ", self.n_verts)

        self.verts = create_arc_verts(center, radius_outer, alpha_1, alpha_2,
                                      segments)
        self.verts += create_arc_verts(center, radius_inner, alpha_1, alpha_2,
                                       segments)

        self.create_index()

        self.color = color
        self.verts_colors = color * self.n_verts

        self.gl_prim_mode = pyglet.gl.GL_TRIANGLES
        self.indexed = True

    def create_index(self):
        segments = self.segments

        verts_i = []
        for n in range(segments):

            verts_i += [ segments+n+1, n, n+1 ]
            verts_i += [ segments+n+1, n+1, segments+n+2 ]

        self.verts_index = verts_i


class RingArc(RingArcBase):

    def __init__(self, center=(0, 0), radius_outer=100, radius_inner=80,
                 alpha_1=0, alpha_2=math.pi, color=(200, 0, 255), segments=10):

        super().__init__(center, radius_outer, radius_inner, alpha_1, alpha_2, 
                         color, segments)


class StrokeRingArc(RingArcBase):

    def __init__(self, center=(0, 0), radius=100, width=15,
                 alpha_1=0, alpha_2=math.pi, color=(200, 0, 255), segments=10):

        radius_outer = radius + width/2
        radius_inner = radius - width/2

        super().__init__(center, radius_outer, radius_inner, alpha_1, alpha_2,
                         color, segments)


### element group

class Group:

    def __init__(self, position=(0, 0), angle=0):
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

# (deprecated)
#            shape.draw()
#            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
#                            ('v2f', shape.verts),
#                            ('c3B', shape.colors))
        pyglet.gl.glPopMatrix()


### helper functions

def create_circle_verts(center, r, segments):
    segment_angle = 2 * math.pi / segments

    verts = []
    for n in range(segments):

        alpha = n * segment_angle

        verts.append( center[0] + round(r*math.cos(alpha)) )
        verts.append( center[1] + round(r*math.sin(alpha)) )

    return verts


def create_arc_verts(center, r, alpha_1, alpha_2, segments):
    segment_angle = (alpha_2-alpha_1) / segments

    verts = []
    for n in range(segments+1):

        alpha = alpha_1 + n * segment_angle

        verts.append( center[0] + round(r*math.cos(alpha)) )
        verts.append( center[1] + round(r*math.sin(alpha)) )

    return verts


def create_radial_index(segments):
    verts_index = []
    # (leaves last segment open)
    for n in range(segments):

        triangle_index = [ 0, n+1, n+2 ]
        verts_index += triangle_index

    return verts_index


def create_rect_verts(center, size):
    c_x = center[0]
    c_y = center[1]
    width = size[0]
    height = size[1]

    return [ c_x-width/2, c_y-height/2,
             c_x+width/2, c_y-height/2,
             c_x+width/2, c_y+height/2,
             c_x-width/2, c_y+height/2 ]


def create_tiltrect_verts(start, end, width):
    Sx = start[0]
    Sy = start[1]

    Ex = end[0]
    Ey = end[1]

    x = Ex - Sx
    y = Ey - Sy

    angle = math.atan2(y, x)

    w_2 = width/2

    px = w_2 * math.sin(angle)
    py = w_2 * math.cos(angle)

    # (debug-print)
    #print("px: ", px)
    #print("py: ", py)    

    v0_x = Sx + px
    v0_y = Sy - py
    v1_x = Sx - px
    v1_y = Sy + py

    v2_x = Ex + px
    v2_y = Ey - py
    v3_x = Ex - px
    v3_y = Ey + py

    verts = [ v0_x, v0_y, v1_x, v1_y, v2_x, v2_y, v3_x, v3_y ]

    # (debug-print)
    #print("verts: ", verts)

    return verts

# (debug)
#create_rectangle_verts((0,0), (50,-50), 10)
