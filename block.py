import random
import copy

class Block(object):
    def __init__(self,width=10):
        self.x = 5
        self.y = 0
        self.width = width
        self.min_x = 0
        self.max_x = 0
        self.lock = False
        self.block_type = 0
        self.blocks = []
        self.direction = 0
        self.sparse = []

    def change(self):
        self.direction += 1
        self.gen_block(self.block_type, self.direction)
    
    def gen_new_block(self):
        self.gen_block(random.randint(0,6),random.randint(0,3))

    def fall(self):
        self.y += 1
    
    def move(self, move_direction):
        self.x += move_direction

    def undo_move(self, move_direction):
        self.x -= move_direction
    
    def get_sparse(self):
        for j, row in enumerate(self.blocks):
            for i, item in enumerate(row):
                if item == 1:
                    self.sparse.append((i,j))
        

    def gen_block(self, block_type= None, direction=None):
        if block_type == None:
            block_type = self.block_type
        if direction == None:
            direction = self.direction
        '''
        正方形小块
        '''
        if block_type == 0:
            self.blocks = [[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]

        elif block_type == 1:
            '''
            长条形
            '''
            if direction % 2 == 0:
                self.blocks = [[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]]
            elif direction % 2 == 1:
                self.blocks = [[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]]

        elif block_type == 2:
            '''
            T形
            '''
            if direction % 4 == 0:
                self.blocks = [[0,1,0,0],[0,1,1,0],[0,1,0,0],[0,0,0,0]]
            elif direction % 4 == 1:
                self.blocks = [[0,1,0,0],[1,1,1,0],[0,0,0,0],[0,0,0,0]]
            elif direction % 4 == 2:
                self.blocks = [[0,0,1,0],[0,1,1,0],[0,0,1,0],[0,0,0,0]]
            elif direction % 4 == 3:
                self.blocks = [[0,0,0,0],[1,1,1,0],[0,1,0,0],[0,0,0,0]]

        elif block_type == 3:        
            '''
            Z形
            '''
            if direction % 2 == 0:
                self.blocks = [[0,0,1,0],[0,1,1,0],[0,1,0,0],[0,0,0,0]]
            elif direction % 2 == 1:
                self.blocks = [[0,0,0,0],[0,1,1,0],[0,0,1,1],[0,0,0,0]]
        elif block_type == 4:
            '''
            倒z形
            '''
            if direction % 2 == 0:
                self.blocks = [[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,0,0]]
            elif direction % 2 == 1:
                self.blocks = [[0,0,0,0],[0,1,1,0],[1,1,0,0],[0,0,0,0]]
        elif block_type == 5:
            '''
            7形
            '''
            if direction % 4 == 0:
                self.blocks = [[0,0,0,0],[1,1,1,0],[1,0,0,0],[0,0,0,0]]
            elif direction % 4 == 1:
                self.blocks = [[1,1,0,0],[0,1,0,0],[0,1,0,0],[0,0,0,0]]
            elif direction % 4 == 2:
                self.blocks = [[0,0,1,0],[1,1,1,0],[0,0,0,0],[0,0,0,0]]
            elif direction % 4 == 3:
                self.blocks = [[0,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,0,0]]
        elif block_type == 6:
            '''
            反7形
            '''
            if direction % 4 == 0:
                self.blocks = [[0,0,0,0],[1,1,1,0],[0,0,1,0],[0,0,0,0]]
            elif direction % 4 == 1:
                self.blocks = [[0,1,0,0],[0,1,0,0],[1,1,0,0],[0,0,0,0]]
            elif direction % 4 == 2:
                self.blocks = [[0,0,0,0],[1,1,1,0],[0,0,1,0],[0,0,0,0]]
            elif direction % 4 == 3:
                self.blocks = [[0,1,1,0],[0,1,0,0],[0,1,0,0],[0,0,0,0]]
        self.get_sparse()
        return self.blocks

if __name__ == "__main__":
    block = Block()
    