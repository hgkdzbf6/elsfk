import copy
import numpy as np
from block import Blocks

class UiData(object):
    def __init__(self,height, width):
        self.blocks = np.zeros((height, width), dtype=np.uint8)
        self.falling_blocks = np.zeros((4, 4), dtype=np.uint8)
        self.next_blocks = np.zeros((4, 4), dtype=np.uint8)
        self.score = 0
        self.speed = 10
    
class GameBase(object):
    def __init__(self):
        self.height = 20
        self.width = 10
        self.ui_data = UiData(self.height,self.width)
        '''
        -1: 未初始化
        0: 和平
        1: 下落
        '''
        self.status = 0
        self.next_block = 0
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

    def gen_falling_blocks(self):
        if self.falling_blocks == None:
            if self.next_blocks == None:
                self.gen_next_shape()
            self.falling_blocks = self.next_blocks
            self.falling_blocks.gen_new_block()
            self.ui_data.falling_blocks = self.falling_blocks.blocks
            self.gen_next_shape()

    def gen_next_shape(self):
        self.next_blocks = Blocks(width = self.width)
        self.next_blocks.gen_new_block()
        self.ui_data.next_blocks = self.next_blocks.blocks

    def _vanish_line(self):
        '''
        等下落完成的时候才去判断
        '''
        if self.status == 0:
            vanish_lines = []
            for i,row in enumerate(self.ui_data.blocks):
                if row.all() == 1:
                    vanish_lines.append(i)

            for vanish_item in vanish_lines:
                self.ui_data.blocks = np.delete(self.ui_data.blocks, vanish_item, 0)
                self.ui_data.blocks = np.insert(self.ui_data.blocks, 0, [0]*self.width, axis=0)

    def test_vanish_line(self):
        self.status = 0
        self.ui_data.blocks = np.ones((self.height, self.width), dtype=np.uint8)
        self.ui_data.blocks[1,2] = 0
        print(self.ui_data.blocks)
        self._vanish_line()
        print(self.ui_data.blocks)

    def _test_block(self, px, py):
        return self.ui_data.blocks[py,px] == 1 

    def _test_shape(self,shape, px, py):
        return shape.blocks[py,px] == 1 

    def _test_one_conflict(self,shape, px, py):
        for j in shape.shape[0]:
            for i in shape.shape[1]:
                if shape[i + shape.x, j + shape.y] == 1 and self._test_block(px,py):
                    return 

    def test_conflict(self, shape = None):
        if shape == None:
            shape = self.falling_blocks
        for j in range(shape.blocks.shape[0]):
            for i in range(shape.blocks.shape[1]):
                if self._test_shape(shape, i, j) and self._test_block(i + shape.x, j + shape.y):
                    return True
        return False

    def test_test_conflict(self):
        self.status = 0
        self.ui_data.blocks = np.ones((self.height, self.width), dtype=np.uint8)
        self.ui_data.blocks[11,2] = 0
        self.ui_data.blocks[16,4] = 0
        self.ui_data.blocks[7,3] = 0
        self.ui_data.blocks[7,4] = 0
        self.ui_data.blocks[7,0] = 0
        self.ui_data.blocks[7,6] = 0
        self._vanish_line()
        print(self.ui_data.blocks)
        self.gen_falling_blocks()
        self.falling_blocks.x = 3
        self.falling_blocks.y = 15
        print(self.test_conflict())

    def falling(self):
        if self.test_conflict() == False:
            self.shape.fall()

    def move(self):
        self.shape.move(self.move_flag)
        if self.test_conflict() == True:
            self.shape.undo_move(self.move_flag)

    def tick(self):
        if (self.timestamp % int(self.ui_data.speed) * 100) == 0:
            self.falling()
            self.timestamp += 1

        self.combine()
        return self.show_blocks

if __name__ == "__main__":
    game = GameBase()
    game.test_test_conflict()