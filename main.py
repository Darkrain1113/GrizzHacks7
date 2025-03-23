import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
import math


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.paused = False
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        if not self.paused:
            self.player.update()
            self.raycasting.update()
            self.object_handler.update()
            self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw_minimap(self):
        # Calculate mini-map dimensions
        map_width = self.map.cols * MINIMAP_CELL_SIZE
        map_height = self.map.rows * MINIMAP_CELL_SIZE
        
        # Create a surface for the mini-map
        minimap_surface = pg.Surface((map_width, map_height))
        minimap_surface.fill((0, 0, 0))  # Black background
        
        # Draw walls
        for pos in self.map.world_map:
            x, y = pos
            pg.draw.rect(minimap_surface, MINIMAP_WALL_COLOR,
                        (x * MINIMAP_CELL_SIZE, y * MINIMAP_CELL_SIZE,
                         MINIMAP_CELL_SIZE, MINIMAP_CELL_SIZE))
        
        # Draw player
        player_x = int(self.player.pos[0] * MINIMAP_CELL_SIZE)
        player_y = int(self.player.pos[1] * MINIMAP_CELL_SIZE)
        pg.draw.circle(minimap_surface, MINIMAP_PLAYER_COLOR,
                      (player_x, player_y), MINIMAP_CELL_SIZE // 2)
        
        # Draw player direction line
        end_x = player_x + int(math.cos(self.player.angle) * MINIMAP_CELL_SIZE * 2)
        end_y = player_y + int(math.sin(self.player.angle) * MINIMAP_CELL_SIZE * 2)
        pg.draw.line(minimap_surface, MINIMAP_PLAYER_COLOR,
                    (player_x, player_y), (end_x, end_y), 1)
        
        # Draw the mini-map on the screen
        self.screen.blit(minimap_surface, MINIMAP_POS)
        
        # Draw border
        pg.draw.rect(self.screen, MINIMAP_BORDER_COLOR,
                    (MINIMAP_POS[0] - 2, MINIMAP_POS[1] - 2,
                     map_width + 4, map_height + 4), 2)

    def draw(self):
        self.object_renderer.draw()
        if not self.paused:
            self.weapon.draw()
        self.draw_minimap()  # Add mini-map drawing

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)
            # Handle question input
            self.object_renderer.handle_question_input(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
