import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Interaction
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer

class Level:
     def __init__(self):

         self.display_surface = pygame.display.get_surface()

         #groups
         self.all_sprites = CameraGroup()
         self.collision_sprites = pygame.sprite.Group()
         self.interaction_sprites = pygame.sprite.Group()

         self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
         self.setup()
         self.overlay = Overlay(self.player)
         self.transition = Transition(self.reset, self.player)

         #music
         self.music = pygame.mixer.Sound('../audio/music.mp3')
         self.music.set_volume(0.1)
         self.music.play(loops = -1)

     def setup(self):
         tmx_data = load_pygame('../data/map(真）.tmx')

         #fence
         for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
             Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

         #地面
         Generic(
             pos = (0,0),
             surf = pygame.image.load('../graphics/world/ground.png').convert_alpha(),
             groups = self.all_sprites,
             z = LAYERS['ground']
         )

         #碰撞图块
         for x, y ,surf in tmx_data.get_layer_by_name('Collision').tiles():
             Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

         #玩家
         for obj in tmx_data.get_layer_by_name('Player'):
             if obj.name == 'Start':
                self.player = Player(pos =(obj.x, obj.y),
                                     group = self.all_sprites,
                                     collision_sprites = self.collision_sprites,
                                     interaction = self.interaction_sprites,
                                     soil_layer = self.soil_layer)

             if obj.name == 'Bed':
                 Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)

     def player_add(self,item):

         self.player.item_inventory[item] += 1

     def reset(self):
         self.soil_layer.update_plants()

         self.soil_layer.remove_water()


     def plant_collision(self):
         if self.soil_layer.plant_sprites.sprites():
             for plant in self.soil_layer.plant_sprites.sprites():
                 if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                     self.player_add(plant.plant_type)
                     plant.kill()
                     self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')


     def run(self,dt):

         self.all_sprites.custom_draw(self.player)


         self.all_sprites.update(dt)
         self.plant_collision()

         self.overlay.display()
         if self.player.sleep:
             self.transition.play()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()


    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)