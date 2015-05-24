#!/usr/bin/python
#
# collision test
#

#import numpy as np
import pyglet
import math

import pyglet_draw_elements as draw_el

### globals

SCALE_MPX = 100

### helper functions

# (actually there's math.radians/degrees)
#def deg2rad(alpha_deg):
#    return alpha_deg / 180 * math.pi
#
#def rad2deg(alpha_rad):
#    return alpha_rad / math.pi * 180

def m2px(s):
    return s * SCALE_MPX

# test simple collision

class Vec2:

    def __init__(self, r):
        self.r = list(r)
        # (use numpy instead)
        #self.r = np.array(r)
        self.x = r[0]
        self.y = r[1]

    def __mul__(self, other):
        if type(other) in (int, float):
            return Vec2((self.x * other, self.y * other))

    __rmul__ = __mul__


class Wall:

    def __init__(self, p0=(100, 0), p1=(100, 100)):
        self.p0 = Vec2(p0)
        self.p1 = Vec2(p1)

        self.geometry()

    def geometry(self):
        line = draw_el.Line(m2px(self.p0).r,
                            (m2px(self.p1.r[0]), m2px(self.p1.r[1])), 
                            color=(50, 220, 120))

        self.geom = draw_el.Group((0, 0))
        self.geom.shapes.append(line)

    def render(self):
        self.geom.render()


class VertWall(Wall):

    def __init__(self, x=100, h0=10, h1=200):
        self.p0 = Vec2((x, h0))
        self.p1 = Vec2((x, h1))

        self.geometry()

    def check_collisions(self):
        # checks for collisions with agents, calling agent.collide
        # with a direction vector
        # (debug-print)
        #print("checking coll")
        for agent in world.agents:
            p = agent.pos
            r = agent.radius
            wall_bot = self.p0.y
            wall_top = self.p1.y
            wall_x = self.p0.x
            # check vertical range
            if p.y+r < wall_bot or p.y-r > wall_top:
                continue
            # get horizontal distance
            d = abs(wall_x - p.x)
            if d < r and p.x < wall_x: # collision from left
                agent.collide((-1, 0))
            elif d < r and p.x > wall_x: # collision from right
                agent.collide((1, 0))


class Agent:

    def __init__(self, pos=(1.5, 2)):
        self.pos = Vec2(pos)
        self.phi = math.radians(10.0) #math.pi  # (orientation)

        # size (circular)
        self.radius = 0.25
        # wheelbase
        self.s_wheel = 0.5
        # wheel radius
        self.r_wheel = 0.075

        self.mass = 2.5

        # coefficients
        self.c_drag = 0.5  # (air drag)
        self.c_rfric = 0.01 #0.8  # (rolling friction)

        #self.v_x = velocity_x
        self.v_lon = 0.0
        self.omega = 0.0

        self.geometry()

    def dynamics(self, T_motL, T_motR, dt):

        # Definition: Moment M (torque) clockwise is positive

        F_rfric = self.mass * world.g * self.c_rfric
        #print("F_rfric: ", F_rfric)
        F_drag = self.c_drag * self.v_lon * self.v_lon
        #print("F_drag: ", F_drag)

        F_tracL = T_motL * self.r_wheel
        #print("F_tracL: ", F_tracL)
        F_effL = max(F_tracL - F_rfric, 0)

        F_tracR = T_motR * self.r_wheel
        F_effR = max(F_tracR - F_rfric, 0)

        F_lon = F_effL + F_effR - F_drag
        #print("F_lon: ", F_lon)

        #M = F_L * self.s_wheel - F_R * self.s_wheel

        a_lon = F_lon / self.mass

        v_lon = self.v_lon + a_lon * dt
        self.v_lon = v_lon

#        print("v_lon: ", self.v_lon)

        # (orientation)
        if T_motL != T_motR:
            r = self.s_wheel / 2 * ((T_motL + T_motR) / (T_motL - T_motR))

            omega = v_lon / r

            self.phi = ( self.phi + omega * dt ) % (2*math.pi)
            print("phi deg: ", degrees(self.phi))

        # (position)
        s_lon = v_lon * dt

        self.pos.x += s_lon * math.cos(self.phi)
        self.pos.y += s_lon * math.sin(self.phi)

        self.pos.r[0] = self.pos.x
        self.pos.r[1] = self.pos.y

#    def move(self, dt):
#        # (currently simply moving in +x)
#        self.pos.x = self.pos.x + self.v_x * dt
#        self.pos.r[0] = self.pos.x

    def collide(self, dir):
        # takes the direction from where the collision came
        # reset pos
        #self.pos.x = self.pos.x - self.v_x * 0.5
        #self.v_x = self.v_x * -1
        pass

    def geometry(self):
        circle = draw_el.Circle(radius=m2px(self.radius))

        line = draw_el.Line((0, 0), (m2px(self.radius), 0))

        self.geom = draw_el.Group((m2px(self.pos.r[0]), m2px(self.pos.r[1])))
        self.geom.shapes.append(circle)
        self.geom.shapes.append(line)

    def render(self):
        self.geom.position = (m2px(self.pos.r[0]), m2px(self.pos.r[1]))
        self.geom.angle = degrees(self.phi)
        self.geom.render()


class World:

    def __init__(self):
        self.obstacles = []
        self.agents = []

        self.g = 9.81  # (gravity)

        self.create_environment()
        self.add_agent()

    def create_environment(self):
#        self.camera = draw_el.Camera((2, 2), scale=100)
        #self.camera.focus(window.width, window.height)

        #wall1 = Wall((400, 20), (400, 400))
        wall1 = VertWall(4, 1, 4)
        self.obstacles.append(wall1)

        wall2 = VertWall(1, 1, 3.5)
        self.obstacles.append(wall2)

    def add_agent(self):
        # (currently only one agent is used,
        #  later use agent = Agent() w/o self)
        agent = Agent()
        self.agents.append(agent)

    def dynamics(self, dt):
        # move the agents
        for agent in self.agents:
            agent.dynamics(1, 5, dt)
        # check collisions
        for wall in self.obstacles:
            wall.check_collisions()

    def render(self):
#        self.camera.shoot(window.width, window.height)
#        self.camera.shoot()
        for obstacle in self.obstacles:
            obstacle.render()
        #print("agents: ", self.agents)
        for agent in self.agents:
            agent.render()

### initialize pyglet

window = pyglet.window.Window()
window.clear()
fps_display = pyglet.clock.ClockDisplay()

@window.event
def on_draw():
    pass

### 'game loop'

def update(dt):
    window.clear()

    world.dynamics(dt)

    # animate
    # (later a for loop could be used to animate the agents)
    world.render()

    fps_display.draw()

### set up world

world = World()

### run pyglet

# dt=0.1 results in visible delay (min. fps about 15)
# dt=0.05 better (min. fps about 25)
pyglet.clock.schedule_interval(update, 1/20)
#pyglet.clock.schedule(update)

pyglet.app.run()
