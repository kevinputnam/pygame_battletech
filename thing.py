import pygame
import actor

class Thing():

    def __init__(self, attr_dict,grid_size):

        self.name = 'name'
        self.hidden = False
        self.description = "It's something all right."
        self.canTake = False
        self.locks = False
        self.goesTo = None
        self.actions = []
        self.on_collision = None
        self.trigger = False
        self.triggered = False
        self.location = [0,0]
        self.dimensions = [0,0]
        self.dx = 0
        self.dy = 0
        self.direction = 'none'
        self.sprite = None
        self.grid_size = grid_size
        self.inventory = []

        for key in attr_dict:
            setattr(self,key,attr_dict[key])

        self.location[0] = self.location[0]*grid_size
        self.location[1] = self.location[1]*grid_size

        if 'sprite_sheet_path' in attr_dict:
                self.update_sprite(self.sprite_sheet_path,self.sprite_size,self.directions)

    def get_rect(self):
        return self.location + [self.location[0]+self.dimensions[0],self.location[1]+self.dimensions[1]]

    def move(self,location,direction):
        self.location[0] = location[0]*self.grid_size
        self.location[1] = location[1]*self.grid_size
        self.direction = direction

    def update_sprite(self,path,size,directions):
        self.sprite_sheet_path = path
        self.sprite_size = size
        self.directions = directions
        self.sprite = actor.Actor(self.location[0],self.location[1],self.sprite_sheet_path,self.sprite_size,self.directions)