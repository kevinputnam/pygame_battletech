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
        self.items = []

        for key in scene_data:
            setattr(self,key,scene_data[key])

        self.background = pygame.image.load(scene_data['background'])
        if self.player:
            self.player = actor.Actor(0,0,self.player['sprite_sheet_path'],self.player['sprite_size'],self.player['directions'])

        if 'things' in scene_data:
            for item in scene_data['things']:
                self.items.append(thing.Thing(item))