import cv2 
import numpy as np
from block import Block
from logic import GameBase
import random
import time

class OpenCVDraw(object):
    def __init__(self, game:GameBase):
        self.ratio = 100
        self.game = game
        self.cols = game.width
        self.rows = game.height
        self.right_width = 4 
        self.text_height = 2
        self.padding = 1
        self.width = self.padding * 3 + self.cols + self.right_width
        self.height = self.padding * 3 + self.rows  
        self.img = self.__create_empty(self.width, self.height)

    def __create_empty(self, width,height):
        return np.zeros((height * self.ratio, width* self.ratio, 3),dtype=np.uint8)

    def __create_one(self, width,height, val):
        return np.ones((height * self.ratio, width* self.ratio, 3),dtype=np.uint8)*val

    def __set(self, start_x, start_y, width, height, val):
        print(start_x, start_y, width, height, val.shape)
        print(self.img.shape)
        self.img[
            start_y * self.ratio : start_y * self.ratio + height * self.ratio, 
            start_x * self.ratio : start_x * self.ratio + width * self.ratio, :] = val
        
    def _draw_one_block(self, px, py, color = (255,0,0)):
        cv2.rectangle(self.img,(px*self.ratio,py*self.ratio), ((px+1)*self.ratio,(py+1)*self.ratio),color,-1)
        cv2.rectangle(self.img,(px*self.ratio,py*self.ratio), ((px+1)*self.ratio,(py+1)*self.ratio),(0,0,0),1)

    def _draw_one_block_at(self, img, px, py):
        cv2.rectangle(img,(px*self.ratio,py*self.ratio), ((px+1)*self.ratio,(py+1)*self.ratio),(255,0,0),-1)
        cv2.rectangle(img,(px*self.ratio,py*self.ratio), ((px+1)*self.ratio,(py+1)*self.ratio),(0,0,0),int(self.ratio*0.15))

    def _draw_falling_blocks(self):
        pass

    def _draw_blocks(self):
        pass

    def draw_blocks(self):
        blocks_img = self.__create_one(self.cols, self.rows, 128)
        next_block_img = self.__create_one(self.right_width, self.right_width, 33)
        score_img = self.__create_one(self.right_width,self.text_height, 88)
        speed_img = self.__create_one(self.right_width,self.text_height, 200)

        self._draw_one_block_at(blocks_img, 0,0)
        self._draw_one_block_at(blocks_img, 0,1)
        self._draw_one_block_at(blocks_img, 0,2)

        # 图像的横纵是相反的
        self.__set(self.padding,self.padding, self.cols, self.rows,  blocks_img)
        self.__set(self.padding*2+self.cols,self.padding, self.right_width, self.right_width,  next_block_img)
        self.__set(self.padding*2+self.cols,self.padding*2 + self.right_width, self.right_width, self.text_height,  score_img)
        self.__set(self.padding*2+self.cols,self.padding*3 + self.right_width +self.text_height, self.right_width, self.text_height,  speed_img)

    def test_draw_blocks(self):
        self.draw_blocks()
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        cv2.imshow('img',self.img)
        cv2.waitKey()

    def draw(self, blocks):
        for j,row in enumerate(blocks):
            for i,item in enumerate(row):
                if item == 1:
                    self._draw_one_block(i,j)

        cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        cv2.imshow('img',self.img)
        cv2.waitKey()

    def update(self):
        while True:
            msg = self.game.tick()
            time.sleep(0.1)
            self.draw(msg)
            print(msg)
            
if __name__ == "__main__":
    game = GameBase()
    game.gen_new_shape()
    ui = OpenCVDraw(game)
    ui.test_draw_blocks()
    # ui.update()
