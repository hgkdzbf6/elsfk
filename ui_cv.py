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
        self.width = game.width
        self.height = game.height
        self.img = np.zeros((self.width * self.ratio, 
            self.height * self.ratio),dtype=np.uint8)
        
    def _draw_one_point(self, px, py):
        cv2.rectangle(self.img,(px*self.ratio,py*self.ratio), ((px+1)*self.ratio,(py+1)*self.ratio),(255,0,0),-1)

    def draw(self, blocks):
        for j,row in enumerate(blocks):
            for i,item in enumerate(row):
                if item == 1:
                    self._draw_one_point(i,j)

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
    ui.update()
