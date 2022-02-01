import copy
import numpy as np
from block import Blocks

DEFAULT_SPEED = 20


class UiData(object):
    def __init__(self, height, width):
        self.blocks = np.zeros((height, width), dtype=np.uint8)
        self.falling_blocks = np.zeros((4, 4), dtype=np.uint8)
        self.next_blocks = np.zeros((4, 4), dtype=np.uint8)
        self.score = 0
        self.speed = DEFAULT_SPEED


class GameBase(object):
    def __init__(self):
        self.height = 30
        self.width = 20
        self.ui_data = UiData(self.height, self.width)
        '''
        -1: 未初始化
        0: 和平
        1: 下落
        '''
        self.status = 0
        self.control_cmd = 0
        '''
        10次才更新一次，如果falling为true的话，速度加倍
        '''
        self.timestamp = 0
        self.falling_blocks = None
        self.next_blocks = None
        '''
        0：不向任何方向移动
        1：向右移动
        -1：向左移动
        '''
        self.move_flag = 0
        '''
        0：No block
        1：
        '''
        self.block_reason = 0
        self.goto_bottom = 0

    def gen_falling_blocks(self):
        if self.falling_blocks == None:
            if self.next_blocks == None:
                self.gen_next_shape()
        self.falling_blocks = self.next_blocks
        self.ui_data.falling_blocks = self.falling_blocks.blocks
        self.gen_next_shape()

    def gen_next_shape(self):
        self.next_blocks = Blocks(width=self.width)
        self.next_blocks.gen_new_block()
        self.ui_data.next_blocks = self.next_blocks.blocks

    def _update_blocks(self):
        shape = self.falling_blocks
        for i in range(shape.blocks.shape[0]):
            for j in range(shape.blocks.shape[1]):
                if self._test_shape(shape, i, j):
                    self._set_block(shape.x + i, shape.y + j)

    def update_once(self):
        # 1. 先把原来的下落的方块放到里面原始的block里面
        self._update_blocks()
        # 2. 消失线
        self._vanish_line()
        # 3. 下一个方块补上
        self.gen_falling_blocks()
        # 4. 提高速度
        self.change_speed()

    def change_speed(self):
        self.ui_data.speed = int(
            DEFAULT_SPEED * 100 / (100 + self.ui_data.score))

    def _vanish_line(self):
        '''
        等下落完成的时候才去判断
        '''
        if self.status == 0:
            vanish_lines = []
            for i, row in enumerate(self.ui_data.blocks):
                if row.all() == 1:
                    vanish_lines.append(i)

            self.ui_data.score += 2**len(vanish_lines) - 1

            for vanish_item in vanish_lines:
                self.ui_data.blocks = np.delete(
                    self.ui_data.blocks, vanish_item, 0)
                self.ui_data.blocks = np.insert(
                    self.ui_data.blocks, 0, [0]*self.width, axis=0)

    def test_vanish_line(self):
        self.status = 0
        self.ui_data.blocks = np.ones(
            (self.height, self.width), dtype=np.uint8)
        self.ui_data.blocks[1, 2] = 0
        print(self.ui_data.blocks)
        self._vanish_line()
        print(self.ui_data.blocks)

    def init(self):
        self.status = 0
        self.ui_data.blocks = np.zeros(
            (self.height, self.width), dtype=np.uint8)

    def _test_block(self, px, py):
        return self.ui_data.blocks[py, px] == 1

    def _validate_block(self, px, py):
        h, w = self.ui_data.blocks.shape
        return px >= 0 and px < w and py >= 0 and py < h

    def _set_block(self, px, py):
        self.ui_data.blocks[py, px] = 1

    def _test_shape(self, shape, px, py):
        return shape.blocks[py, px] == 1

    def move_left(self):
        shape = self.falling_blocks
        shape.move_left()
        if self.test_conflict(0):
            shape.undo()

    def move_right(self):
        shape = self.falling_blocks
        shape.move_right()
        if self.test_conflict(0):
            shape.undo()

    def fall(self):
        shape = self.falling_blocks
        shape.fall()
        if self.test_conflict(0):
            self.update_once()
            shape.undo()

    def change(self):
        shape = self.falling_blocks
        shape.change()
        self.ui_data.falling_blocks = shape.blocks
        if self.test_conflict(0):
            shape.undo()
            self.ui_data.falling_blocks = self.falling_blocks.blocks

    @staticmethod
    def fast_gen(args=[(0, 5), (2, 5), (1, 5), (1, 8), (3, 4)]):
        game = GameBase()
        game.init()
        game.gen_falling_blocks()
        h, w = game.height, game.width
        for row, col in args:
            if np.sum(game.ui_data.blocks[h-row-1, :]) == 0:
                game.ui_data.blocks[h-row-1, :] = 1
            game.ui_data.blocks[h-row-1, col] = 0
        game._vanish_line()
        return game

    def test_conflict(self, behavior=0):
        '''
        behavior: 
        0: 什么都不做
        1: 向左移动
        2: 向右移动
        3: 向下移动
        4: 旋转
        '''
        res = False
        shape = self.falling_blocks
        # if behavior == 0:
        #     shape.init()
        # elif behavior == 1:
        #     shape.move_left()
        # elif behavior == 2:
        #     shape.move_right()
        # elif behavior == 3:
        #     shape.fall()
        # elif behavior == 4:
        #     shape.change()
        for i in range(shape.blocks.shape[0]):
            for j in range(shape.blocks.shape[1]):
                if self._test_shape(shape, i, j):
                    if self._validate_block(i + shape.x, j + shape.y):
                        if self._test_block(i + shape.x, j + shape.y):
                            res = True
                            print('发生碰撞，碰撞的位置为')
                            print(shape.blocks)
                    else:
                        res = True
                        print('移动超出范围')
                        print(shape.x, shape.y)
                        print(shape.blocks)
        if res:
            shape.undo()
        return res

    def test_test_conflict(self):
        self.status = 0
        self.ui_data.blocks = np.ones(
            (self.height, self.width), dtype=np.uint8)
        self.ui_data.blocks[11, 2] = 0
        self.ui_data.blocks[16, 4] = 0
        self.ui_data.blocks[7, 3] = 0
        self.ui_data.blocks[7, 4] = 0
        self.ui_data.blocks[7, 0] = 0
        self.ui_data.blocks[7, 6] = 0
        print('before vanish line')
        print(self.ui_data.blocks)
        self._vanish_line()
        print('after vanish line')
        print(self.ui_data.blocks)
        self.gen_falling_blocks()
        self.falling_blocks._move_to(3, 10)
        print(self.test_conflict(1))

    def tick(self):
        if (self.timestamp % int(self.ui_data.speed)) == 1:
            print('tick', self.timestamp)
            self.fall()
            if self.test_conflict():
                self.update_once()
        self.timestamp += 1

    def test_key(self, key):
        if key == 119:  # 上
            self.change()
            return 1
        elif key == 115:
            self.fall()
            return 2
        elif key == 97:
            self.move_left()
            return 3
        elif key == 100:
            self.move_right()
            return 4
        # elif key == 102:
        #     self.update_once()
        #     return 5
        elif key == 32:
            return 0


if __name__ == "__main__":
    game = GameBase()
    game.test_test_conflict()
