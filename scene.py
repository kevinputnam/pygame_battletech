import pygame

class Scene:

    def __init__(self,ID, name, background_file_path):
        self.id = ID
        self.name = name
        self.background = pygame.image.load(background_file_path)
        self.collisions = [] # table of 8x8 squares that match collision locations on the background
        self.triggers = [] # list of locations that trigger behaviors
        self.npcs = [] # list of npc sprites
        self.scene_type = None # tells the main loop how to handle movement of the player and other stuff
        self.actions = [] # sequential list of actions to perform when scene started
        self.player = None