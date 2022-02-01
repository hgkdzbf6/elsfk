from my_draw import MyDraw
import cv2

class OpenCVDraw(MyDraw):
    def __init__(self, game: GameBase):
        super().__init__(game)
        self.img = self.__create_empty(self.width, self.height)

    def _draw_rectangle_by_absolute_pos(self, img, px1, py1, px2, py2, color, thickness):
        cv2.rectangle(img, (py1, px1), (py2, px2), color, thickness)

    def _draw_text(self, img, text):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, text, (0, int(1 * self.ratio)), font, float(0.02 * self.ratio),  (255,255,0), int(0.1 * self.ratio))
        # return super()._draw_text(img, text)
    
    def _show(self, title):
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        cv2.imshow('img',self.img)
    
    def _waitkey(self):
        return cv2.waitKeyEx()