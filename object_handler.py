from sprite_object import *
from npc import *
from random import choices, randrange


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]
        self.weights = [70, 20, 10]
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.enemies = 3  # Starting number of enemies
        self.last_killed_enemy = None
        self.last_killed_enemy_pos = None
        self.current_level = 1
        self.setup_level()

    def setup_level(self):
        # Clear existing NPCs
        self.npc_list.clear()
        
        # Adjust difficulty based on level
        if self.current_level == 1:
            self.enemies = 3
            self.weights = [70, 20, 10]  # More soldiers, fewer demons
        elif self.current_level == 2:
            self.enemies = 5
            self.weights = [50, 30, 20]  # More balanced distribution
        else:  # Level 3
            self.enemies = 7
            self.weights = [30, 40, 30]  # More demons, fewer soldiers

        # Spawn NPCs for current level
        self.spawn_npc()

    def spawn_npc(self):
        for i in range(self.enemies):
                npc = choices(self.npc_types, self.weights)[0]
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                while (pos in self.game.map.world_map) or (pos in self.restricted_area):
                    pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))

    def check_win(self):
        if not len(self.npc_positions):
            if self.game.map.next_level():
                self.current_level += 1
                self.setup_level()
                self.game.object_renderer.show_text_box(f"Level {self.current_level}!")
            else:
                self.game.object_renderer.win()
                pg.display.flip()
                pg.time.delay(1500)
                self.game.new_game()

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        self.check_win()

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def respawn_last_killed_enemy(self):
        if self.last_killed_enemy and self.last_killed_enemy_pos:
            # Create new instance of the same enemy type
            if isinstance(self.last_killed_enemy, SoldierNPC):
                new_enemy = SoldierNPC(self.game, pos=self.last_killed_enemy_pos)
            elif isinstance(self.last_killed_enemy, CacoDemonNPC):
                new_enemy = CacoDemonNPC(self.game, pos=self.last_killed_enemy_pos)
            else:
                new_enemy = CyberDemonNPC(self.game, pos=self.last_killed_enemy_pos)
            
            self.add_npc(new_enemy)
            self.last_killed_enemy = None
            self.last_killed_enemy_pos = None

    def store_killed_enemy(self, enemy):
        self.last_killed_enemy = enemy
        self.last_killed_enemy_pos = (enemy.x, enemy.y)