#!/usr/bin/python
#
# artificial life simulation
#

import time
import random
import draw_artilife

random.seed()


### globals

# first there was light...
# (emmiting light at a constant rate)
LIGHT = 1.0


### world

class World():

    def __init__(self, size):

        self.size_x = size[0]
        self.size_y = size[1]

        self.num_of_fields = self.size_x * self.size_y

        # initialize field matrix
        self.occ_matrix = [ [ False for i in range(size[0]) ] for j in range(size[1]) ]

#    def field_occupied(self, pos_x, pos_y):
#        '''Return whether a field is occupied (True).'''
#        print("field matrix: ", self.occupied_fields_matrix)
#        print("field: ", self.occupied_fields_matrix[pos_y][pos_x])
#        return self.occupied_fields_matrix[pos_y][pos_x]


### lifeforms

## a plant cell

class PlantCell():

    def __init__(self, plant, position):

        self.plant = plant
        self.plant.cells.append(self)

        self.position = position

        plant.world.occ_matrix[position[0]][position[1]] = True

        self.energy = 0.0

        self.energy_crit = 1.0

    def live(self):

        # collect energy from light
        self.energy = self.energy + LIGHT / 2

        # if energy reaches critical level, split !
        if self.energy > self.energy_crit:
            self.split()

    def split(self):

        off_x = random.randint(-1,1)

        if off_x == 0:
            # (cannot be 0 as well !)
            off_y = random.randrange(-1,2,2)
        else:
            off_y = random.randint(-1,1)

        new_pos_x = self.position[0] + off_x
        new_pos_y = self.position[1] + off_y

        # check if position occupied
        # (get the field number)
#        print("new pos: {} {}".format(new_pos_x, new_pos_y))
#        pos_occupied = self.plant.world.field_occupied(new_pos_x, new_pos_y)
#        print("pos occupied: ", pos_occupied)

        # if not create new cell here
        if not self.plant.world.occ_matrix[new_pos_x][new_pos_y]:
            c_n = PlantCell(self.plant, (new_pos_x, new_pos_y))

        self.energy = self.energy - self.energy_crit

## a plant

class Plant():

    def __init__(self, world, position):

        self.world = world

        self.position = position

        self.cells = []

        first_cell = PlantCell(self, position)

    def live(self):

        for cell in self.cells:
            cell.live()


def world_loop():

    w = World((1000, 1000))

    p1 = Plant(w, (50, 50))

    d1 = draw_artilife.DrawArtilife(p1)

    while True:

        time.sleep(0.1)

        p1.live()

        for cell_num, cell in enumerate(p1.cells):
            pass
            #print("cell: {} energy: {}".format(cell_num+1, cell.energy))

        d1.redraw()

#        if len(p1.cells) >= 4:
#            time.sleep(1000)

world_loop()
