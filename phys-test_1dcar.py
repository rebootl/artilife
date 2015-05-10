#!/usr/bin/python
#
# test physics
#
# Car physics: http://www.asawicki.info/Mirror/Car%20Physics%20for%20Games/Car%20Physics%20for%20Games.html
#
# Differential steering:
# - http://www.researchgate.net/profile/Fernando_Ribeiro7/publication/228680998_Controlling_omni-directional_Wheels_of_a_MSL_RoboCup_autonomous_mobile_robot/links/0deec522f23a15d546000000.pdf
#

import pygame

### globals

# gui
# (font and window size)
FONTPATH = '/usr/share/fonts/TTF/DejaVuSansMono.ttf'
W, H = 640, 420

#M = (int(W/2), int(H/2))

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 1m = 100px
SCALE_MPX = 20

def m_to_px(s):
    return s * SCALE_MPX


class OneDimCar():

    def __init__(self, pos_x):

        # physical geometry
        self.width = 2
        self.height = 1.2

        self.r_wheel = 0.05

        # draw geometry
        self.geometry()

        # mass
        self.mass = 100

        # coefficients
        self.c_drag = 1.2
        self.c_fric = 10.0

        # initial velocity and position
        self.vx = 0.0
        self.x = pos_x

    def dynamic_calc(self, M_mot, dt):

        # force
        Fx_mot = M_mot / self.r_wheel

        Fx_drag = self.c_drag * self.vx * self.vx
        Fx_fric = self.c_fric * self.vx

        Fx = Fx_mot - Fx_drag - Fx_fric

        print("Fx_mot: ", Fx_mot)

        # acceleration
        ax = Fx / self.mass

        # velocity (euler)
        self.vx = self.vx + ax * dt

        print("vx: ", self.vx)

        # position (euler)
        self.x = self.x + self.vx * dt

        if m_to_px(self.x) > W:
            self.x = 0

    def geometry(self):

        self.color = BLUE
        self.draw_w = m_to_px(self.width)
        self.draw_h = m_to_px(self.height)

        self.draw_y = 0.8 * H

    def draw(self):

        screen = self.screen

        draw_x = m_to_px(self.x)

        # draw a dummy rectangle
        pygame.draw.rect(screen, self.color, [ draw_x, self.draw_y, self.draw_w, self.draw_h ])


class DrawWorld():

    def __init__(self):

        pygame.init()

        screen_size = W, H
        self.screen = pygame.display.set_mode(screen_size)

        self.elements = []

    def add_element(self, element):

        self.elements.append(element)

        # (cheat the screen in)
        element.screen = self.screen

    def redraw(self):
        # set bg (clears the screen)
        self.screen.fill(BLACK)

        # draw the elements
        for element in self.elements:
            element.draw()

        # update display
        pygame.display.flip()


def world():
    '''Main function.'''

    # drawing
    dw = DrawWorld()

    # ground
#    gnd = Ground(0.2)

    car = OneDimCar(3)

    dw.add_element(car)

    # get clock
    clock = pygame.time.Clock()

    # "game loop"
    while True:

        # process events (keystrokes etc.)
        #..

        # run physics
        #..
        car.dynamic_calc(0.5, 0.1)

        # redraw
        dw.redraw()

        # set framerate
        clock.tick(30)

    #pygame.quit()


world()
