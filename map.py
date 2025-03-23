import pygame as pg

_ = False

# Level 1 Map (Original)
mini_map_1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, 2, 2, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 4, _, _, _, 4, _, _, _, _, _, _, 1],
    [1, 1, 1, 3, 1, 3, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 3, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 4, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, 3, 4, _, 4, 3, _, 1],
    [1, _, _, 5, _, _, _, _, _, _, 3, _, 3, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 4, _, _, _, _, _, _, 4, _, _, 4, _, _, _, 1],
    [1, 1, 3, 3, _, _, 3, 3, 1, 3, 3, 1, 3, 1, 1, 1],
    [1, 1, 1, 3, _, _, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 4, _, _, 4, 3, 3, 3, 3, 3, 3, 3, 3, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, 5, _, _, _, 5, _, _, _, 5, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]

# Level 2 Map (More complex layout)
mini_map_2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 2, 2, 2, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 2, _, 3, 3, 3, _, _, _, _, _, _, _, _, 1],
    [1, _, 2, _, 3, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 2, _, 3, _, 4, 4, 4, _, _, _, _, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, _, _, _, _, _, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, 5, 5, _, _, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, _, _, _, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, 2, 2, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, _, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, 3, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, 4, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 2, _, 3, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Level 3 Map (Most complex layout)
mini_map_3 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, _, _, 1],
    [1, _, 3, _, _, _, _, _, _, _, _, _, 3, _, _, 1],
    [1, _, 3, _, 4, 4, 4, 4, 4, 4, 4, _, 3, _, _, 1],
    [1, _, 3, _, 4, _, _, _, _, _, 4, _, 3, _, _, 1],
    [1, _, 3, _, 4, _, 5, 5, 5, _, 4, _, 3, _, _, 1],
    [1, _, 3, _, 4, _, 5, _, _, _, 4, _, 3, _, _, 1],
    [1, _, 3, _, 4, _, 5, _, 2, _, 4, _, 3, _, _, 1],
    [1, _, 3, _, 4, _, 5, _, _, _, 4, _, 3, _, _, 1],
    [1, _, 3, _, 4, _, 5, 5, 5, _, 4, _, 3, _, _, 1],
    [1, _, 3, _, 4, _, _, _, _, _, 4, _, 3, _, _, 1],
    [1, _, 3, _, 4, 4, 4, 4, 4, 4, 4, _, 3, _, _, 1],
    [1, _, 3, _, _, _, _, _, _, _, _, _, 3, _, _, 1],
    [1, _, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, _, _, 1],
    [1, _, 2, _, _, _, _, _, _, _, _, _, 2, _, _, 1],
    [1, _, 2, _, 3, 3, 3, 3, 3, 3, 3, _, 2, _, _, 1],
    [1, _, 2, _, 3, _, _, _, _, _, 3, _, 2, _, _, 1],
    [1, _, 2, _, 3, _, 4, 4, 4, _, 3, _, 2, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, _, _, 3, _, 2, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, 5, _, 3, _, 2, _, _, 1],
    [1, _, 2, _, 3, _, 4, _, _, _, 3, _, 2, _, _, 1],
    [1, _, 2, _, 3, _, 4, 4, 4, _, 3, _, 2, _, _, 1],
    [1, _, 2, _, 3, _, _, _, _, _, 3, _, 2, _, _, 1],
    [1, _, 2, _, 3, 3, 3, 3, 3, 3, 3, _, 2, _, _, 1],
    [1, _, 2, _, _, _, _, _, _, _, _, _, 2, _, _, 1],
    [1, _, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Map:
    def __init__(self, game):
        self.game = game
        self.current_level = 1
        self.maps = {
            1: mini_map_1,
            2: mini_map_2,
            3: mini_map_3
        }
        self.mini_map = self.maps[self.current_level]
        self.world_map = {}
        self.rows = len(self.mini_map)
        self.cols = len(self.mini_map[0])
        self.get_map()

    def get_map(self):
        self.world_map = {}
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def next_level(self):
        if self.current_level < 3:
            self.current_level += 1
            self.mini_map = self.maps[self.current_level]
            self.get_map()
            return True
        return False

    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.world_map]