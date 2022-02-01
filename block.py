import random
import copy
import numpy as np


class Blocks(object):
    def __init__(self, width=10):
        self.x = 5
        self.y = 0
        self.width = width
        self.min_x = 0
        self.max_x = 0
        self.lock = False
        self.block_type = 0
        self.blocks = np.zeros((4, 4), dtype=np.uint8)
        self.direction = 0
        self.pre = (0, 0, 0, 0)
        self.sparse = []

    def change(self):
        self.restore_current_status()
        self.direction += 1
        self.gen_block(self.block_type, self.direction)

    def gen_new_block(self):
        self.block_type = random.randint(0, 6)
        self.direction = random.randint(0, 3)
        self.gen_block(self.block_type, self.direction)

    def _move_to(self, px, py):
        self.x = px
        self.y = py
        self.restore_current_status()

    def restore_current_status(self):
        self.pre = (self.x, self.y, self.direction, self.block_type)

    def fall(self):
        self.restore_current_status()
        self.y += 1

    def move_left(self):
        self.restore_current_status()
        self.x -= 1

    def move_right(self):
        self.restore_current_status()
        self.x += 1

    def undo(self):
        (self.x, self.y, self.direction, self.block_type) = self.pre
        self.gen_block(self.block_type, self.direction)
        (self.x, self.y, self.direction, self.block_type) = self.pre

    def get_sparse(self):
        for j, row in enumerate(self.blocks):
            for i, item in enumerate(row):
                if item == 1:
                    self.sparse.append((i, j))

    def gen_block(self, block_type=None, direction=None):
        if block_type == None:
            block_type = self.block_type
        if direction == None:
            direction = self.direction
        '''
        正方形小块
        '''
        if block_type == 0:
            if direction % 1 == 0:
                self.blocks = np.array(
                    [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]])

        elif block_type == 1:
            '''
            长条形
            '''
            if direction % 2 == 0:
                self.blocks = np.array(
                    [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]])
            elif direction % 2 == 1:
                self.blocks = np.array(
                    [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]])

        elif block_type == 2:
            '''
            T形
            '''
            if direction % 4 == 0:
                self.blocks = np.array(
                    [[0, 1, 0, 0], [0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]])
            elif direction % 4 == 1:
                self.blocks = np.array(
                    [[0, 1, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
            elif direction % 4 == 2:
                self.blocks = np.array(
                    [[0, 0, 1, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]])
            elif direction % 4 == 3:
                self.blocks = np.array(
                    [[0, 0, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]])

        elif block_type == 3:
            '''
            Z形
            '''
            if direction % 2 == 0:
                self.blocks = np.array(
                    [[0, 0, 1, 0], [0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]])
            elif direction % 2 == 1:
                self.blocks = np.array(
                    [[0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 0, 0]])
        elif block_type == 4:
            '''
            倒z形
            '''
            if direction % 2 == 0:
                self.blocks = np.array(
                    [[0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]])
            elif direction % 2 == 1:
                self.blocks = np.array(
                    [[0, 0, 0, 0], [0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0]])
        elif block_type == 5:
            '''
            7形
            '''
            if direction % 4 == 0:
                self.blocks = np.array(
                    [[0, 0, 0, 0], [1, 1, 1, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
            elif direction % 4 == 1:
                self.blocks = np.array(
                    [[1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]])
            elif direction % 4 == 2:
                self.blocks = np.array(
                    [[0, 0, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
            elif direction % 4 == 3:
                self.blocks = np.array(
                    [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]])
        elif block_type == 6:
            '''
            反7形
            '''
            if direction % 4 == 0:
                self.blocks = np.array(
                    [[0, 0, 0, 0], [1, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]])
            elif direction % 4 == 1:
                self.blocks = np.array(
                    [[0, 1, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0]])
            elif direction % 4 == 2:
                self.blocks = np.array(
                    [[1, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
            elif direction % 4 == 3:
                self.blocks = np.array(
                    [[0, 1, 1, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]])
        return self.blocks


if __name__ == "__main__":
    block = Blocks()
