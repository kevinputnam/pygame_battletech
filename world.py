import json
import scene
import re
import gui
from os.path import isfile

class World():

    def __init__(self,world_path):
        data = self.load(world_path)
        #temporary workaround
        self.scene_backgrounds = []
        for key in data:
            setattr(self,key,data[key])
        self.scenes = []
        for s in data['scenes']:
            #temporary workaround
            self.scene_backgrounds.append(s['background'])
            self.scenes.append(scene.Scene(s))
        ## added for refactor
        self.actions = []
        gui.initialize_display(self.gamename)
        self.initialize_scene(self.first_scene,self.start_player_pos)

    def load(self, path):
        world_data = {}
        if isfile(path):
            with open(path) as jsonFile:
                world_data = json.load(jsonFile)
        return world_data

    def get_param(self,value):
        new_val = value
        for var in self.variables:
            new_val = new_val.replace('`$'+var+'`',str(self.variables[var]))
        return new_val

#### In Development - Major Refactor - Not used by main.py

    # main game loop
    def start(self):
        while 1:
            gui.process_user_input()
            self.run_actions()
            gui.update_gui()

    def test_method(self,arg):
        print('oh, ho! ' + arg + ' pressed!')

    def initialize_scene(self,scene_id,player_pos):
        #temporary workaround
        gui.load_new_scene(self.scene_backgrounds[scene_id])
        for action in self.scenes[scene_id].actions:
            self.actions.append(action)
        gui.button_behaviors['start'] = [self.test_method,['start']]
        gui.button_behaviors['select'] = [self.test_method,['select']]
        gui.button_behaviors['a'] = [self.test_method,['a']]
        gui.button_behaviors['b'] = [self.test_method,['b']]
        gui.button_behaviors['left'] = [self.test_method,['left']]
        gui.button_behaviors['right'] = [self.test_method,['right']]
        gui.button_behaviors['up'] = [self.test_method,['up']]
        gui.button_behaviors['down'] = [self.test_method,['down']]

#### Action Handler

    def run_actions(self):
        if not gui.timer_active:
            if self.actions:
                action = self.actions.pop(0)
                getattr(self,'action_'+action['name'],self.action_default)(action)


#### Actions

    def action_start_timer(self,action):
        gui.start_timer(int(self.get_param(action['milliseconds'])))

    def action_change_scene(self,action):
        print(action['name'])

    def action_default(self,action):
        print("Invalid action: " + action['name'])