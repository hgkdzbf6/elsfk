import copy
from block import Block

class GameBase(object):
    def __init__(self):
        self.height = 20
        self.width = 10
        self.show_blocks = []
        self.solid_blocks = [[0] * self.width] * self.height
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
        self.speed = 10
        self.score = 0
        self.shape = None
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

    def gen_new_shape(self):
        self.shape = Block(width = self.width)
        self.shape.gen_new_block()

    def _vanish_line(self):
        '''
        等下落完成的时候才去判断
        '''
        if self.status == 0:
            vanish_lines = []
            for i,row in enumerate(self.solid_blocks):
                erase_this_line = True
                for item in row:
                    if item == 0:
                        erase_this_line = False
                        break
                if erase_this_line == True:
                    vanish_lines.append(i)
            for vanish_item in vanish_lines:
                self.solid_blocks.pop(vanish_item)
                self.solid_blocks.insert(0,[0]*self.width)

    def test_conflict(self, shape = None):
        if shape == None:
            shape = self.shape
        for item_x, item_y in shape.sparse:
            if shape.x + item_x < 0:
                pass
            if self.solid_blocks[shape.x + item_x][shape.y + item_y] == 1:
                return True
        return False

    def falling(self):
        if self.test_conflict() == False:
            self.shape.fall()

    def combine(self):
        self.show_blocks = copy.deepcopy(self.solid_blocks)
        for item_x, item_y in self.shape.sparse:
            self.show_blocks[self.shape.x+item_x][self.shape.y+item_y] = 1

    def move(self):
        self.shape.move(self.move_flag)
        if self.test_conflict() == True:
            self.shape.undo_move(self.move_flag)

    def tick(self):
        if (self.timestamp % int(self.speed) * 100) == 0:
            self.falling()
            self.timestamp += 1

        self.combine()
        return self.show_blocks