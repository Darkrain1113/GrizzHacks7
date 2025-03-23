from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = 700
        self.time_prev = pg.time.get_ticks()
        # diagonal movement correction
        self.diag_move_corr = 1 / math.sqrt(2)
        # Controller settings
        self.controller = None
        self.controller_connected = False
        self.check_controller()

    def check_controller(self):
        if pg.joystick.get_count() > 0:
            self.controller = pg.joystick.Joystick(0)
            self.controller.init()
            self.controller_connected = True
            print(f"Controller connected: {self.controller.get_name()}")

    def handle_controller_input(self):
        if not self.controller_connected:
            return

        # Movement
        left_stick_x = -self.controller.get_axis(0)  # Invert X axis
        left_stick_y = -self.controller.get_axis(1)  # Invert Y axis
        right_stick_x = -self.controller.get_axis(2)  # Invert look rotation

        # Increased deadzone for better drift handling
        deadzone = 0.15  # Increased from 0.1 to 0.15
        
        # Apply deadzone with smooth transition
        if abs(left_stick_x) < deadzone:
            left_stick_x = 0
        else:
            left_stick_x = (abs(left_stick_x) - deadzone) * (1 / (1 - deadzone)) * (1 if left_stick_x > 0 else -1)
            
        if abs(left_stick_y) < deadzone:
            left_stick_y = 0
        else:
            left_stick_y = (abs(left_stick_y) - deadzone) * (1 / (1 - deadzone)) * (1 if left_stick_y > 0 else -1)
            
        if abs(right_stick_x) < deadzone:
            right_stick_x = 0
        else:
            right_stick_x = (abs(right_stick_x) - deadzone) * (1 / (1 - deadzone)) * (1 if right_stick_x > 0 else -1)

        # Movement speed
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * math.sin(self.angle)
        speed_cos = speed * math.cos(self.angle)

        # Calculate movement based on stick input
        dx = (left_stick_x * speed_cos - left_stick_y * speed_sin)
        dy = (left_stick_x * speed_sin + left_stick_y * speed_cos)

        # Apply diagonal movement correction if both axes are active
        if abs(left_stick_x) > deadzone and abs(left_stick_y) > deadzone:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        # Rotation based on right stick (reduced sensitivity for better control)
        self.angle += right_stick_x * PLAYER_ROT_SPEED * self.game.delta_time * 1.5

        # Check for shooting (right trigger)
        if self.controller.get_axis(5) > 0.5 and not self.shot and not self.game.weapon.reloading:
            self.game.sound.shotgun.play()
            self.shot = True
            self.game.weapon.reloading = True

        # Check wall collision and move
        self.check_wall_collision(dx, dy)

    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def check_game_over(self):
        if self.health < 1:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def get_damage(self, damage):
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()
        self.check_game_over()

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True

    def movement(self):
        if self.controller_connected:
            self.handle_controller_input()
            return

        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        num_key_pressed = -1
        if keys[pg.K_w]:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos

        # diag move correction
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        self.check_wall_collision(dx, dy)

        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                    (self.x * 100 + WIDTH * math.cos(self.angle),
                     self.y * 100 + WIDTH * math. sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        if self.controller_connected:
            return
            
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        self.movement()
        self.mouse_control()
        self.recover_health()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)