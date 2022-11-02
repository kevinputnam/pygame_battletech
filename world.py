import json
import scene
import re
from os.path import isfile

class World():

    def __init__(self,world_path):
        data = self.load(world_path)
        self.variables = data['variables']
        self.scenes = []
        for s in data['scenes']:
            self.scenes.append(scene.Scene(s))

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


