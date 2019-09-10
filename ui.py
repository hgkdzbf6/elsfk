import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from block import Block

class SimpleDraw(object):
    def __init__(self, one_block):
        self.figure= plt.figure()
        self.ax = self.figure.gca()
        self.width = len(one_block)
        self.height = len(one_block[0])
        for j,row in enumerate(one_block):
            for i,item in enumerate(row):
                if item == 1:
                    self._draw_one_point(i,j)
        self.ax.figure.canvas.draw()

    def draw(self):
        plt.show()

    def _draw_one_point(self, px, py):
        self.ax.add_patch(Rectangle((px,py), 1,1))

if __name__ == "__main__":
    block = Block()
    one_block = block.gen_block(4,3)
    ui = SimpleDraw(one_block)
    print(one_block)
    ui.draw()