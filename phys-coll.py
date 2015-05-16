#!/usr/bin/python
#
# collision test
#

import pyglet
import pyglet_draw_elements as draw_el

# test simple collision

class Wall:

    def __init__(self, p0=(100, 0), p1=(100, 100)):
        self.p0 = p0
        self.p1 = p1

        self.geometry()

    def geometry(self):
        line = draw_el.Line(self.p0, self.p1, color=(50, 220, 120))

        self.geom = draw_el.Group((0, 0))
        self.geom.shapes.append(line)

    def render(self):
        self.geom.render()


class Agent:

    def __init__(self, pos=(100, 200), velocity_x=30):
        self.pos = list(pos)
        self.x = pos[0]
        self.y = pos[1]

        # size (circular)
        self.r = 25

        self.v_x = velocity_x

        self.geometry()

    def move(self, dt):
        # (currently simply moving in +x)
        self.x = self.x + self.v_x * dt
        self.pos[0] = self.x

    def geometry(self):
        circle = draw_el.Circle(radius=self.r)

        self.geom = draw_el.Group(self.pos)
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
        wall1 = Wall((400, 20), (400, 400))
        self.obstacles.append(wall1)

    def add_agent(self):
        # (currently only one agent is used,
        #  later use agent = Agent() w/o self)
        agent = Agent()
        self.agents.append(agent)

    def dynamics(self, dt):
        for agent in self.agents:
            agent.move(dt)

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
