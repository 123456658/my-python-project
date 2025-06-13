import pygame
from settings import *

class Overlay:
    def __init__(self,player):

        self.display_surface = pygame.display.get_surface()
        self.player = player


        #工具和种子
        overlay_path = '../graphics/overlay/'
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha()
                           for tool in player.tools}
        self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha()
                           for seed in player.seeds}

        #字体
        self.font = pygame.font.SysFont(None, 28)  # 默认字体，字号 28
        self.text_color = (255, 255, 255)  # 白色
        self.inventory_start = (20, 20)  # 物品清单起始坐标
        self.line_height = 30  # 每行间距

    def display(self):

        #工具
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surf,tool_rect)

        #种子
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = tool_surf.get_rect(midbottom=OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surf,seed_rect)

        # ---------- 物品清单 ----------
        x, y = self.inventory_start
        for item, count in self.player.item_inventory.items():
            text = f"{item}: {count}"
            text_surf = self.font.render(text, True, self.text_color)
            self.display_surface.blit(text_surf, (x, y))
            y += self.line_height