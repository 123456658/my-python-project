import pygame
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, interaction, soil_layer):
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        self.z = LAYERS['main']

        #运动
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        #碰撞
        self.hitbox = self.rect.copy().inflate((-126, -70))
        self.collision_sprites = collision_sprites


        #计时器
        self.timers = {
            'tool use': Timer(350,self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200)
        }

        #工具
        self.tools = ['hoe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        #种子
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        #inventory
        self.item_inventory = {
            'corn': 0,
            'tomato': 0
        }

        #interaction
        self.interaction = interaction
        self.sleep = False
        self.soil_layer = soil_layer

        #音效
        self.watering = pygame.mixer.Sound('../audio/water.mp3')
        self.watering.set_volume(0.2)



    def use_tool(self):
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)


        if self.selected_tool == 'water':
            self.soil_layer.water(self.target_pos)
            self.watering.play()





    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

    def use_seed(self):
        self.soil_layer.plant_seed(self.target_pos, self.selected_seed)

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                           'up_hoe': [], 'down_hoe': [], 'left_hoe': [], 'right_hoe': [],
                           'up_water': [], 'down_water': [], 'left_water': [], 'right_water': []}

        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self,dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]





    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active and not self.sleep:
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'

            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'

            else:
                self.direction.y = 0



            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'

            else:
                self.direction.x = 0

            #使用工具
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            #更换工具
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                self.tool_index =  self.tool_index if self.tool_index < len(self.tools) else 0
                self.selected_tool = self.tools[self.tool_index]

            #使用种子
            if keys[pygame.K_LCTRL]:
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            #更换种子
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index += 1
                self.seed_index =  self.seed_index if self.seed_index < len(self.seeds) else 0
                self.selected_seed = self.seeds[self.seed_index]

            if keys[pygame.K_RETURN]:
                collided_interaction_sprite = pygame.sprite.spritecollide(self,self.interaction,False)
                if collided_interaction_sprite:
                        self.status = 'left_idle'
                        self.sleep = True

    def get_status(self):
        #idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        #使用工具
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:#正在向右移动
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:#正在向左移动
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == 'vertical':
                        if self.direction.y > 0:#正在向下移动
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:#正在向上移动
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery







    def move(self,dt):
        #使向量大小为一
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = round(self.pos.x)
        self.hitbox.centerx = round(self.pos.x)
        self.collision('horizontal')

        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = round(self.pos.y)
        self.hitbox.centery = round(self.pos.y)
        self.collision('vertical')



    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()

        self.move(dt)
        self.animate(dt)