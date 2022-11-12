import pygame
import actor

class Thing(actor.Actor):

    def __init__(self, attr_dict):

        self.hidden = False
        self.description = "It's something all right."
        self.canTake = False
        self.locks = False
        self.goesTo = None
        self.actions = []
        self.on_collision = None
        self.location = [0,0]
        self.dimensions = [0,0]


        for key in attr_dict:
            setattr(self,key,attr_dict[key])

        pos_x = self.location[0]
        pos_y = self.location[1]

        if 'sprite_sheet_path' in attr_dict:
            super().__init__(pos_x,pos_y,self.sprite_sheet_path,self.sprite_size,self.directions)

    def get_rect(self):
        return self.location + [self.location[0]+self.dimensions[0],self.location[1]+self.dimensions[1]]