import watcher
import numpy as np
import unittest
import logic

class TestAI(unittest.TestCase):

    def setUp(self):
        self.game = logic.GameBase.fast_gen()
        self.watcher = watcher.Watcher.construct_from_game(self.game)
        self.ai = AI(self.watcher)
    
    def test_calc_center(self):
        avg = self.ai.calc_center()
        print(avg)


class AI(object):

    def __init__(self, watcher:watcher.Watcher):
        '''
        测试数据格式
        '''
        self.watcher = watcher
        self.command = 0

    def test_combine(self):
        '''
        测试下落到底部之后的可行性
        '''
        pass
    
    def calc_center(self, falling_block = True):
        '''
        计算重心
        '''
        h,w = self.watcher.blocks.shape
        blocks = self.watcher.blocks
        row_avg_ = np.mean(blocks, axis = 1)
        avg_ = np.multiply(list(range(0,h)),row_avg_)
        return avg_

    def evaluate_func(self):
        '''
        对于某种特定的情况，测试这个评价函数
        参数：
            px: 横坐标
            block_type: 类型
            direction: 方向
        '''
        pxs = range(-1,9)
        directions = range(0,4)
        for px in pxs:
            for direction in directions:
                pass

if __name__ == "__main__":
    unittest.main()