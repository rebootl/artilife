#!/usr/bin/python
#
# drawing functions for artilife simulation
#
# Using pygame.
#

import pygame


FONTPATH = '/usr/share/fonts/TTF/DejaVuSansMono.ttf'
SIZE = (W, H) = (640, 420)

M = (int(W/2), int(H/2))

G_FAC = 5

class DrawArtilife():

    # (colors)

    bg_col = (0, 0, 0)

    lcol_red = (220, 100, 100)
    col_green = (81, 237, 96)

    cell_size_px = 3

    def __init__(self, plant_inst):

        self.plant_inst = plant_inst

        pygame.init()

        # initialize pygame
        self.screen = pygame.display.set_mode(SIZE)

        # (set bg)
        self.screen.fill(self.bg_col)
        pygame.display.flip()

        #..

#        clock = pygame.time.Clock()

    def redraw(self):
        # "game loop"

        # (set framerate)
#        clock.tick(30)

        # clear screen
        self.screen.fill(self.bg_col)

        # draw a mark at the center
        pygame.draw.line(self.screen, self.lcol_red, [M[0]-10, M[1]], [M[0]+10, M[1]])
        pygame.draw.line(self.screen, self.lcol_red, [M[0], M[1]-10], [M[0], M[1]+10])

        # draw the plant
        for cell in self.plant_inst.cells:

            pygame.draw.circle(self.screen,
                self.col_green,
                ( cell.position[0]*G_FAC, cell.position[1]*G_FAC ), 
                self.cell_size_px, 0)

        # update display
        pygame.display.flip()
