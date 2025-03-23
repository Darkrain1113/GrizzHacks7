

import pygame as pg
import math
from settings import PLAYER_ROT_SPEED

class XboxController:
    def __init__(self):
        pg.joystick.init()
        self.connected = pg.joystick.get_count() > 0
        if self.connected:
            self.joystick = pg.joystick.Joystick(0)
            self.joystick.init()
            print(f"[Controller] Connected: {self.joystick.get_name()}")

    def get_movement(self, angle, delta_time, speed):
        if not self.connected:
            return 0, 0, 0, False

        # === Axis mapping ===
        move_y = -self.joystick.get_axis(1)  # Left stick Y (forward/back)
        rotate_x = self.joystick.get_axis(2)  # Right stick X (rotation)
        rt = self.joystick.get_axis(5)        # Right trigger (shoot)

        # === Deadzone handling ===
        def deadzone(val, threshold=0.15):
            return 0 if abs(val) < threshold else val

        move_y = deadzone(move_y)
        rotate_x = deadzone(rotate_x, 0.2)

        # === Movement logic (only forward/back) ===
        move_speed = speed * delta_time
        dx = math.cos(angle) * move_y * move_speed
        dy = math.sin(angle) * move_y * move_speed

        # === Rotation logic ===
        rotation = rotate_x * PLAYER_ROT_SPEED * delta_time * 1.25

        # === Shooting ===
        trigger = max(0, min((rt + 1) / 2, 1))  # Normalize -1 to 1 → 0 to 1
        shooting = trigger > 0.5

        return dx, dy, rotation, shooting
