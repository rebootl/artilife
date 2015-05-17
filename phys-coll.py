#!/usr/bin/python
#
# collision test
#

import numpy as np
import pyglet

import pyglet_draw_elements as draw_el

# test simple collision

class Vec2:

    def __init__(self, r):
        self.r = list(r)
        # (use numpy instead)
        #self.r = np.array(r)
        self.x = r[0]
        self.y = r[1]


class Wall:

    def __init__(self, p0=(100, 0), p1=(100, 100)):
        self.p0 = Vec2(p0)
        self.p1 = Vec2(p1)

        self.geometry()

    def geometry(self):
        line = draw_el.Line(self.p0.r, self.p1.r, color=(50, 220, 120))

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

    def __init__(self, pos=(150, 200), velocity_x=80):
        self.pos = Vec2(pos)

        # size (circular)
        self.radius = 25

        self.v_x = velocity_x

        self.geometry()

    def move(self, dt):
        # (currently simply moving in +x)
        self.pos.x = self.pos.x + self.v_x * dt
        self.pos.r[0] = self.pos.x

    def collide(self, dir):
        # takes the direction from where the collision came
        # reset pos
        #self.pos.x = self.pos.x - self.v_x * 0.5
        self.v_x = self.v_x * -1

    def geometry(self):
        circle = draw_el.Circle(radius=self.radius)

        self.geom = draw_el.Group(self.pos.r)
        self.geom.shapes.append(circle)

    def render(self):
        self.geom.render()


class World:

    def __init__(self):
        self.obstacles = []
        self.agents = []

        self.create_environment()
        self.add_agent()

    def create_environment(self):
        #wall1 = Wall((400, 20), (400, 400))
        wall1 = VertWall(400, 20, 400)
        self.obstacles.append(wall1)

        wall2 = VertWall(100, 20, 350)
        self.obstacles.append(wall2)

    def add_agent(self):
        # (currently only one agent is used,
        #  later use agent = Agent() w/o self)
        agent = Agent()
        self.agents.append(agent)

    def dynamics(self, dt):
        # move the agents
        for agent in self.agents:
            agent.move(dt)
        # check collisions
        for wall in self.obstacles:
            wall.check_collisions()

    def render(self):
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
