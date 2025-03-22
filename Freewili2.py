import pygame
import math
import sys

# === Game Constants ===
WIDTH, HEIGHT = 800, 600
HALF_HEIGHT = HEIGHT // 2
FPS = 60
FOV = math.pi / 3
NUM_RAYS = 120
MAX_DEPTH = 20
DELTA_ANGLE = FOV / NUM_RAYS
SCALE = WIDTH // NUM_RAYS

MAP_SCALE = 8
MAP_TILE = 64 // MAP_SCALE
CELL_SIZE = 64

# === Map Layout ===
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

# === Player State ===
player_x, player_y = 3.5, 3.5
player_angle = 0

# === Pygame Init ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raycasting Weapon Demo")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 14)

# === Joystick Init ===
pygame.joystick.init()
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Controller: {joystick.get_name()}")

# === Load and Slice Weapon Frames ===
sprite_sheet = pygame.image.load("Gun Sprites/PIST2.png").convert_alpha()
FRAME_W, FRAME_H = 254, 302
weapon_frames = []

for i in range(5):
    x = (i % 3) * FRAME_W
    y = (i // 3) * FRAME_H
    frame = sprite_sheet.subsurface(pygame.Rect(x, y, FRAME_W, FRAME_H))
    scaled = pygame.transform.scale(frame, (300, 200))
    weapon_frames.append(scaled)

weapon_index = 0
weapon_animating = False
weapon_timer = 0
ANIM_SPEED = 50  # ms per frame

# === Draw Minimap ===
def draw_map():
    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            color = (200, 200, 200) if game_map[y][x] else (50, 50, 50)
            rect = (x * MAP_TILE, y * MAP_TILE, MAP_TILE, MAP_TILE)
            pygame.draw.rect(screen, color, rect)
    pygame.draw.circle(screen, (255, 0, 0), (int(player_x * MAP_TILE), int(player_y * MAP_TILE)), 5)

# === Cast Rays ===
def cast_rays():
    angle = player_angle - FOV / 2
    for ray in range(NUM_RAYS):
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)

        for depth in range(1, MAX_DEPTH * 100):
            depth /= 100
            tx = player_x + cos_a * depth
            ty = player_y + sin_a * depth
            mx, my = int(tx), int(ty)

            if game_map[my][mx] == 1:
                proj_h = min(HEIGHT, 500 / (depth + 0.0001))
                shade = 255 / (1 + depth * depth * 0.1)
                pygame.draw.rect(screen, (shade, shade, shade),
                                 (ray * SCALE, HALF_HEIGHT - proj_h // 2, SCALE, proj_h))
                break
        angle += DELTA_ANGLE

# === HUD ===
def draw_weapon():
    frame = weapon_frames[weapon_index]
    x = WIDTH // 2 - frame.get_width() // 2
    y = HEIGHT - frame.get_height()
    screen.blit(frame, (x, y))

def draw_position():
    text = f"X:{player_x:.2f} Y:{player_y:.2f} A:{math.degrees(player_angle)%360:.1f}°"
    surf = font.render(text, True, (255, 255, 255))
    screen.blit(surf, (10, HEIGHT - 20))

# === Player Movement ===
def move_player(keys, dt):
    global player_x, player_y, player_angle
    speed = 2 * dt
    rot = 2 * dt
    forward = 0
    turn = 0
    DZ = 0.15

    if joystick:
        forward = -joystick.get_axis(1)
        turn = joystick.get_axis(2)
        if abs(forward) < DZ: forward = 0
        if abs(turn) < DZ: turn = 0
    else:
        if keys[pygame.K_w]: forward = 1
        if keys[pygame.K_s]: forward = -1
        if keys[pygame.K_LEFT]: turn = -1
        if keys[pygame.K_RIGHT]: turn = 1

    player_angle += turn * rot
    dx = math.cos(player_angle) * forward * speed
    dy = math.sin(player_angle) * forward * speed

    if game_map[int(player_y)][int(player_x + dx)] == 0: player_x += dx
    if game_map[int(player_y + dy)][int(player_x)] == 0: player_y += dy

# === Main Loop ===
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not weapon_animating:
            weapon_animating = True
            weapon_index = 0
        elif joystick and event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0 and not weapon_animating:
                weapon_animating = True
                weapon_index = 0

    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    dt = clock.tick(FPS) / 1000
    move_player(keys, dt)
    cast_rays()
    draw_map()
    draw_position()

    # Animate weapon
    if weapon_animating:
        weapon_timer += clock.get_time()
        if weapon_timer >= ANIM_SPEED:
            weapon_timer = 0
            weapon_index += 1
            if weapon_index >= len(weapon_frames):
                weapon_index = 0
                weapon_animating = False

    draw_weapon()
    pygame.display.flip()
