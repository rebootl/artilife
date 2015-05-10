#!/usr/bin/python
#
# artificial life simulation
#

import time
import random

random.seed()

### globals

# first there was light...
# (emmiting light at a constant rate)
LIGHT = 1.0


# boundary ?



### lifeforms

## a plant cell

class PlantCell():

    def __init__(self, plant, x, y):

        self.plant = plant
        self.plant.cells.append(self)

        self.position = (x, y)

        self.energy = 0.0

        self.energy_crit = 1.0

    def live(self):

        # collect energy from light
        self.energy = self.energy + LIGHT / 10

        # if energy reaches critical level, split !
        if self.energy > self.energy_crit:
            self.split()

    def split(self):

        new_pos_x = self.position[0] + random.randint(-1,1)
        new_pos_y = self.position[1] + random.randint(-1,1)

        c_n = PlantCell(self.plant, new_pos_x, new_pos_y)

        self.energy = self.energy - self.energy_crit

## a plant

class Plant():

    def __init__(self, x, y):

        self.position = (x, y)

        self.cells = []

        first_cell = PlantCell(self, x, y)

    def live(self):

        for cell in self.cells:
            cell.live()


def world_loop():

    p1 = Plant(10, 10)

    while True:

        time.sleep(0.5)

        p1.live()

        for cell_num, cell in enumerate(p1.cells):

            print("cell: {} energy: {}".format(cell_num+1, cell.energy))


world_loop()
