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
import math

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

    def __init__(self, pos_x, pos_y):

        # physical geometry
        self.width = 2
        self.height = 1.2

        # (wheelbase)
        self.s_wheel = 0.3

        self.r_wheel = 0.05

        # draw geometry
        self.geometry()

        # mass
        self.mass = 100

        # coefficients
        self.c_drag = 1.2
        self.c_fric = 10.0

        # orientation
        self.phi = 30 / 180 * math.pi

        # position
        self.x = pos_x
        self.y = pos_y

        # velocity
        #self.vy = 0.0
        #self.vx = 0.0
        self.v_lon = 0.0

    def dynamic_calc(self, M_motL, M_motR, dt):

        # force
        F_mot = (M_motL + M_motR) / self.r_wheel

        F_drag = self.c_drag * self.v_lon * self.v_lon

        # --> friction, possibly wrong calculation...
        F_fric = self.c_fric * self.v_lon

        F_lon = F_mot - F_drag - F_fric

        #print("Flon: ", Flon)

        # acceleration
        a_lon = F_lon / self.mass

        # velocity (euler)
        self.v_lon = self.v_lon + a_lon * dt

        #print("v_lon: ", self.v_lon)

        # orientation
        # acc. to formula N (rot. speed) should be used,
        # trying w/ moment instead
        # (turn radius)
        if M_motL != M_motR:
            r = self.s_wheel / 2 * ((M_motL + M_motR) / (M_motL - M_motR))

            omega = self.v_lon / r

            self.phi = self.phi + omega * dt
            # --> normalize

        # position (euler)
        s_lon = self.v_lon * dt

        self.x = self.x + s_lon * math.cos(self.phi)
        self.y = self.y + s_lon * math.sin(self.phi)

        # (reset boundary)
        x_px = m_to_px(self.x)
        y_px = m_to_px(self.y)

        if x_px > W:
            self.x = 0
        elif x_px < 0:
            self.x = W / SCALE_MPX

        if y_px > H:
            self.y = 0
        elif y_px < 0:
            self.y = H / SCALE_MPX

    def geometry(self):

        self.color = BLUE
        self.draw_w = m_to_px(self.width)
        self.draw_h = m_to_px(self.height)

    def draw(self):

        screen = self.screen

        draw_x = m_to_px(self.x)
        draw_y = m_to_px(self.y)

        # draw a dummy rectangle
        pygame.draw.rect(screen, self.color, [ draw_x, draw_y, self.draw_w, self.draw_h ])


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

    car = OneDimCar(3, 3)

    dw.add_element(car)

    # get clock
    clock = pygame.time.Clock()

    # "game loop"
    while True:

        # process events (keystrokes etc.)
        #..

        # run physics
        #..
        car.dynamic_calc(0.49, 0.5, 0.1)

        # redraw
        dw.redraw()

        # set framerate
        clock.tick(30)

    #pygame.quit()


world()
