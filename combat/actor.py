import pygame
import ui

class Actor(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, sprite_sheet_path, sprite_size, directions):
        super().__init__()
        self.directions = {}
        self.sprite_sheet = pygame.image.load(sprite_sheet_path)
        self.sprite_width = sprite_size[0]
        self.sprite_height = sprite_size[1]
        self.sprites = []
        self.camera_focus = False
        for y in range(int(self.sprite_sheet.get_height()/self.sprite_height)):
            for x in range(int(self.sprite_sheet.get_width()/self.sprite_width)):
                self.sprites.append(pygame.Surface.subsurface(self.sprite_sheet,self.sprite_width*x,self.sprite_height*y,self.sprite_width,self.sprite_height))
        self.directions = directions
        self.current_dir_index = 0
        self.image = self.sprites[self.current_dir_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]

    def update(self,direction,pos_x,pos_y):

        self.rect.topleft = [pos_x, pos_y]

        if direction in self.directions:

            if self.current_dir_index in self.directions[direction]:
                direction_index = self.directions[direction].index(self.current_dir_index) + 1
                if direction_index >= len(self.directions[direction]):
                    self.current_dir_index = self.directions[direction][0]
                else:
                    self.current_dir_index = self.directions[direction][direction_index]
            else:
                self.current_dir_index = self.directions[direction][0]

            self.image = self.sprites[self.current_dir_index]

        # move with the map
        if not self.camera_focus:
            pos_x = self.rect.topleft[0]
            pos_y = self.rect.topleft[1]
            self.rect.topleft = (pos_x+ui.map_offset_x,pos_y+ui.map_offset_y)

