
import logic

class Watcher(object):
    def __init__(self):
        self.falling_blocks = None
        self.next_blocks = None
        self.blocks = None

        self.direction = 0
        self.px = 0

    @staticmethod
    def construct_from_game(game:logic.GameBase):
        watcher = Watcher()
        watcher.falling_blocks = game.falling_blocks
        watcher.next_blocks = game.next_blocks
        watcher.blocks = game.ui_data.blocks
        watcher.direction = game.falling_blocks.direction
        watcher.px = game.falling_blocks.direction
        return watcher