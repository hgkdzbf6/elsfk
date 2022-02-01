from abc import abstractmethod
import numpy as np
from block import Blocks
from logic import GameBase
import random
import time


class MyDraw(object):
    def __init__(self, game: GameBase):
        self.ratio = 100
        self.game = game
        self.cols = game.width
        self.rows = game.height
        self.right_width = 4
        self.text_height = 2
        self.padding = 1
        self.width = self.padding * 3 + self.cols + self.right_width
        self.height = self.padding * 3 + self.rows

    def __create_empty(self, width, height):
        '''
        创建全0的矩阵
        '''
        return np.zeros((height * self.ratio, width * self.ratio, 3), dtype=np.uint8)

    def __create_one(self, width, height, val):
        '''
        创建全1的矩阵
        '''
        return np.ones((height * self.ratio, width * self.ratio, 3), dtype=np.uint8)*val

    def _set_patch_pos(self, start_x, start_y, width, height, val):
        '''
        把变化的方块，放到对应位置
        '''
        self.img[
            start_y * self.ratio: start_y * self.ratio + height * self.ratio,
            start_x * self.ratio: start_x * self.ratio + width * self.ratio, :] = val

    @abstractmethod
    def _draw_rectangle_by_absolute_pos(self, img, px1, py1, px2, py2, color, thickness):
        pass

    def _draw_one_block(self, px, py, color=(255, 0, 0)):
        '''
        画一个方块
        '''
        self._draw_rectangle_by_absolute_pos(self.img, px * self.ratio,
                                             py *
                                             self.ratio, (px + 1) *
                                             self.ratio, (py + 1) * self.ratio,
                                             color, -1)
        '''
        画黑色边框
        '''
        self._draw_rectangle_by_absolute_pos(self.img, px * self.ratio, py * self.ratio,
                                             (px + 1) * self.ratio, (py + 1) * self.ratio, (0, 0, 0), 1)

    def _draw_one_block_at(self, img, px, py, color=(255, 0, 0)):
        self._draw_rectangle_by_absolute_pos(
            img, px * self.ratio, py * self.ratio, (px + 1) * self.ratio, (py + 1) * self.ratio, color, -1)
        self._draw_rectangle_by_absolute_pos(img, px * self.ratio, py * self.ratio, (
            px + 1) * self.ratio, (py + 1) * self.ratio, (0, 0, 0), int(self.ratio * 0.15))

    def _draw_falling_blocks(self, img):
        pass

    def _draw_blocks(self, blocks, img):
        for j in range(blocks.shape[0]):
            for i in range(blocks.shape[1]):
                if blocks[j, i] == 1:
                    self._draw_one_block_at(img, i, j)

    def _draw_all_blocks(self, blocks, falling_blocks, px, py, img):
        for j in range(blocks.shape[0]):
            for i in range(blocks.shape[1]):
                if blocks[j, i] == 1:
                    self._draw_one_block_at(img, i, j)

        for j in range(falling_blocks.shape[0]):
            for i in range(falling_blocks.shape[1]):
                if falling_blocks[j, i] == 1:
                    self._draw_one_block_at(img, i + px, j + py, (0, 0, 255))

    @abstractmethod
    def _draw_text(self, img, text):
        pass

    def draw_blocks(self):
        blocks_img = self.__create_one(self.cols, self.rows, 128)
        next_block_img = self.__create_one(
            self.right_width, self.right_width, 33)
        score_img = self.__create_one(self.right_width, self.text_height, 88)
        speed_img = self.__create_one(self.right_width, self.text_height, 200)

        self._draw_all_blocks(
            self.game.ui_data.blocks,
            self.game.ui_data.falling_blocks,
            self.game.falling_blocks.x,
            self.game.falling_blocks.y,
            blocks_img)
        self._draw_blocks(
            self.game.ui_data.next_blocks,
            next_block_img)
        self._draw_text(
            score_img,
            'score:'+str(self.game.ui_data.score)
        )
        self._draw_text(
            speed_img,
            'speed:'+str(round(400 / self.game.ui_data.speed, 2))
        )

        # 图像的横纵是相反的
        self._set_patch_pos(
            self.padding,
            self.padding,
            self.cols,
            self.rows,
            blocks_img)
        self._set_patch_pos(
            self.padding*2+self.cols,
            self.padding,
            self.right_width,
            self.right_width,
            next_block_img)
        self._set_patch_pos(
            self.padding*2+self.cols,
            self.padding*2 + self.right_width,
            self.right_width,
            self.text_height,
            score_img)
        self._set_patch_pos(
            self.padding*2+self.cols,
            self.padding*3 + self.right_width + self.text_height,
            self.right_width,
            self.text_height,
            speed_img)

    def test_draw_blocks(self):
        self.draw_blocks()
        self._show('img')
        return self._waitkey()

    def draw(self, blocks):
        for j, row in enumerate(blocks):
            for i, item in enumerate(row):
                if item == 1:
                    self._draw_one_block(i, j)
        self._show('img')
        return self._waitkey()

    @abstractmethod
    def _show(self, title):
        pass

    @abstractmethod
    def _waitkey(self):
        pass

    def update(self):
        while True:
            msg = self.game.tick()
            time.sleep(0.1)
            res = self.draw(msg)
            print(msg)

    def test_key(self, key):
        return self.game.test_key(key)
