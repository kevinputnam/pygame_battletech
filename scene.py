import pygame
import actor
import thing

class Scene:

    def __init__(self,scene_data):
        self.collisions = [] # table of 8x8 squares that match collision locations on the background
        self.triggers = [] # list of locations that trigger behaviors
        self.npcs = [] # list of npc sprites
        self.scene_type = None # tells the main loop how to handle movement of the player and other stuff
        self.actions = [] # sequential list of actions to perform when scene started
        self.player = None
        self.things = []

        for key in scene_data:
            if key != 'things':
                setattr(self,key,scene_data[key])

        if self.player:
            self.player = thing.Thing(self.player,self.grid_size)

        if 'things' in scene_data:
            for t in scene_data['things']:
                self.things.append(thing.Thing(t,self.grid_size))