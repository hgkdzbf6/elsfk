from cv_draw import OpenCVDraw
from logic import GameBase

def main():
    game = GameBase()
    ui = OpenCVDraw(game)
    game.init()
    game.gen_falling_blocks()
    while True:
        res = ui.test_draw_blocks()
        key = game.test_key(res)
        game.tick()
        print('tick')
        if key == 0:
            break

if __name__ == "__main__":
    main()
