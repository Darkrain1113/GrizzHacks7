import pygame as pg
from settings import *
import time
from coding_questions import CodingQuestions
import textwrap


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)
        
        # Text box settings
        self.font = pg.font.Font(None, 74)
        self.small_font = pg.font.Font(None, 36)
        self.text_box_active = False
        self.text_box_start_time = 0
        self.text_box_duration = 3  # seconds
        self.text_box_text = ""
        
        # Question settings
        self.question_active = False
        self.current_question = None
        self.questions = CodingQuestions()
        self.user_input = ""
        self.input_active = True
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval = 500  # milliseconds

    def show_text_box(self, text):
        self.text_box_active = True
        self.text_box_start_time = time.time()
        self.text_box_text = text

    def draw_text_box(self):
        if self.text_box_active:
            current_time = time.time()
            if current_time - self.text_box_start_time < self.text_box_duration:
                # Create semi-transparent black background
                text_box_surface = pg.Surface((WIDTH, 200))
                text_box_surface.fill((0, 0, 0))
                text_box_surface.set_alpha(180)
                self.screen.blit(text_box_surface, (0, HEIGHT//2 - 100))

                # Render text
                text = self.font.render(self.text_box_text, True, (255, 255, 255))
                text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
                self.screen.blit(text, text_rect)
            else:
                self.text_box_active = False
                self.game.paused = False

    def show_question(self, enemy_type):
        self.question_active = True
        self.current_question = self.questions.get_random_question(self.game.object_handler.current_level)
        self.user_input = ""
        self.input_active = True
        self.cursor_visible = True
        self.cursor_timer = pg.time.get_ticks()

    def draw_question_box(self):
        if self.question_active and self.current_question:
            # Create semi-transparent black background
            question_box_surface = pg.Surface((WIDTH, HEIGHT))
            question_box_surface.fill((0, 0, 0))
            question_box_surface.set_alpha(200)
            self.screen.blit(question_box_surface, (0, 0))

            # Wrap the question text
            max_width = WIDTH - 100  # Leave some margin
            wrapped_text = textwrap.fill(self.current_question["question"], width=40)
            
            # Split the wrapped text into lines
            lines = wrapped_text.split('\n')
            
            # Calculate total height needed for the question
            line_height = 60
            total_height = len(lines) * line_height
            
            # Render each line of the question
            for i, line in enumerate(lines):
                question = self.font.render(line, True, (255, 255, 255))
                question_rect = question.get_rect(center=(WIDTH//2, HEIGHT//3 - total_height//2 + i * line_height))
                self.screen.blit(question, question_rect)

            # Render input box
            input_box = pg.Surface((400, 50))
            input_box.fill((50, 50, 50))
            input_box_rect = input_box.get_rect(center=(WIDTH//2, HEIGHT//2))
            self.screen.blit(input_box, input_box_rect)

            # Render user input
            current_time = pg.time.get_ticks()
            if current_time - self.cursor_timer > self.cursor_interval:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = current_time

            display_text = self.user_input
            if self.cursor_visible:
                display_text += "|"

            input_text = self.small_font.render(display_text, True, (255, 255, 255))
            input_rect = input_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            self.screen.blit(input_text, input_rect)

            # Render instructions
            instructions = self.small_font.render("Type your answer and press Enter", True, (200, 200, 200))
            instructions_rect = instructions.get_rect(center=(WIDTH//2, HEIGHT - 100))
            self.screen.blit(instructions, instructions_rect)

    def handle_question_input(self, event):
        if not self.question_active:
            return

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if self.user_input.strip() == self.current_question["answer"]:
                    self.question_active = False
                    self.game.paused = False
                    return True
                else:
                    # Wrong answer - enemy respawns
                    self.game.object_handler.respawn_last_killed_enemy()
                    self.question_active = False
                    self.game.paused = False
                    return False
            elif event.key == pg.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            else:
                if event.unicode.isprintable():
                    self.user_input += event.unicode

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_text_box()
        self.draw_question_box()

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }