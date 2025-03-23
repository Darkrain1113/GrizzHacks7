import math

# game settings
RES = WIDTH, HEIGHT = 1600, 900
# RES = WIDTH, HEIGHT = 1920, 1080
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 0

PLAYER_POS = 1.5, 5  # mini_map
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
PLAYER_SIZE_SCALE = 60
PLAYER_MAX_HEALTH = 100

MOUSE_SENSITIVITY = 0.0003
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

FLOOR_COLOR = (30, 30, 30)

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

# mini-map settings
MINIMAP_SCALE = 0.2  # Scale of the mini-map relative to the screen
MINIMAP_CELL_SIZE = 8  # Size of each cell in the mini-map
MINIMAP_POS = (WIDTH - (32 * MINIMAP_CELL_SIZE) - 20, 10)  # Position of the mini-map in the top-right corner
MINIMAP_BORDER_COLOR = (100, 100, 100)  # Color of the mini-map border
MINIMAP_WALL_COLOR = (200, 200, 200)  # Color of walls in the mini-map
MINIMAP_PLAYER_COLOR = (255, 0, 0)  # Color of the player dot in the mini-map