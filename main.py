import pygame as pg
import sys
import math

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


def show_main_menu(screen):
    font_title = pg.font.Font(None, 100)
    font_option = pg.font.Font(None, 48)
    font_instructions = pg.font.Font(None, 30)

    clock = pg.time.Clock()
    selected = 0
    options = ["Start Game", "Quit"]

    # Load background image once before the loop
    try:
        background_image = pg.image.load('Clone update/resources/textures/Background2.png')
        background_image = pg.transform.scale(background_image, (WIDTH, HEIGHT))
    except Exception as e:
        background_image = None
        print("Background image failed to load:", e)

    while True:
        # Draw background or fallback
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill((10, 10, 10))  # Solid color fallback

        # Title text
        title_text = font_title.render("CODE DUNGEON", True, (255, 0, 0))
        title_shadow = font_title.render("CODE DUNGEON", True, (50, 0, 0))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_shadow, title_rect.move(3, 3))
        screen.blit(title_text, title_rect)

        # Draw menu options
        for i, text in enumerate(options):
            is_selected = (i == selected)
            color = (255, 255, 255) if is_selected else (120, 120, 120)
            prefix = "▶ " if is_selected else "   "
            full_text = font_option.render(prefix + text, True, color)
            label_rect = full_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
            screen.blit(full_text, label_rect)

        # Instructions
        instruction = font_instructions.render("Use ↑ ↓ to navigate, Enter to select", True, (200, 200, 200))
        instruction_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(instruction, instruction_rect)

        pg.display.flip()
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pg.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pg.K_RETURN:
                    if options[selected] == "Start Game":
                        return
                    elif options[selected] == "Quit":
                        pg.quit()
                        sys.exit()


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
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw_minimap(self):
        map_width = self.map.cols * MINIMAP_CELL_SIZE
        map_height = self.map.rows * MINIMAP_CELL_SIZE
        minimap_surface = pg.Surface((map_width, map_height))
        minimap_surface.fill((0, 0, 0))

        for pos in self.map.world_map:
            x, y = pos
            pg.draw.rect(minimap_surface, MINIMAP_WALL_COLOR,
                         (x * MINIMAP_CELL_SIZE, y * MINIMAP_CELL_SIZE,
                          MINIMAP_CELL_SIZE, MINIMAP_CELL_SIZE))

        player_x = int(self.player.pos[0] * MINIMAP_CELL_SIZE)
        player_y = int(self.player.pos[1] * MINIMAP_CELL_SIZE)
        pg.draw.circle(minimap_surface, MINIMAP_PLAYER_COLOR,
                       (player_x, player_y), MINIMAP_CELL_SIZE // 2)

        end_x = player_x + int(math.cos(self.player.angle) * MINIMAP_CELL_SIZE * 2)
        end_y = player_y + int(math.sin(self.player.angle) * MINIMAP_CELL_SIZE * 2)
        pg.draw.line(minimap_surface, MINIMAP_PLAYER_COLOR,
                     (player_x, player_y), (end_x, end_y), 1)

        self.screen.blit(minimap_surface, MINIMAP_POS)

        pg.draw.rect(self.screen, MINIMAP_BORDER_COLOR,
                     (MINIMAP_POS[0] - 2, MINIMAP_POS[1] - 2,
                      map_width + 4, map_height + 4), 2)

    def draw(self):
        self.object_renderer.draw()
        if not self.paused:
            self.weapon.draw()
        self.draw_minimap()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True

            self.player.single_fire_event(event)
            self.object_renderer.handle_question_input(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode(RES)
    show_main_menu(screen)
    game = Game()
    game.run()
