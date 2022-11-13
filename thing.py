import pygame
import actor

class Thing():

    def __init__(self, attr_dict,grid_size):

        self.hidden = False
        self.description = "It's something all right."
        self.canTake = False
        self.locks = False
        self.goesTo = None
        self.actions = []
        self.on_collision = None
        self.location = [0,0]
        self.dimensions = [0,0]
        self.dx = 0
        self.dy = 0
        self.direction = 'none'
        self.sprite = None

        for key in attr_dict:
            setattr(self,key,attr_dict[key])


        self.location[0] = self.location[0]*grid_size
        self.location[1] = self.location[1]*grid_size
        pos_x = self.location[0]
        pos_y = self.location[1]

        if 'sprite_sheet_path' in attr_dict:
            self.sprite = actor.Actor(pos_x,pos_y,self.sprite_sheet_path,self.sprite_size,self.directions)

    def get_rect(self):
        return self.location + [self.location[0]+self.dimensions[0],self.location[1]+self.dimensions[1]]