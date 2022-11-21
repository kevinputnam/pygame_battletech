import pygame
import actor
import thing
import ui

class Scene:

    def __init__(self,scene_data):
        # table of 8x8 squares that match collision locations on the background
        self.id = 0
        self.collisions = []
        self.things = []
        self.map_size = [0,0]
        self.background_image_path = None
        self.grid_size = 8

        for key in scene_data:
            if key != 'things':
                setattr(self,key,scene_data[key])

        if 'things' in scene_data:
            for t in scene_data['things']:
                self.things.append(thing.Thing(t,self.grid_size))

        self.add_collisions()
        ui.load_scene(self.background_image_path,self.map_size)

    def run(self,user_input):
        if len(user_input) > 0:
            print(user_input)

    def add_collisions(self):
        num_cols = int(self.map_size[0]/self.grid_size)
        cur_row = 0
        cur_col = 0
        for c in self.collisions:
            if c == 1:
                self.things.append(thing.Thing({'location':[cur_col,cur_row],'dimensions':[self.grid_size,self.grid_size],"on_collision":{"type":"block","actions":[]}},self.grid_size))
            cur_col += 1
            if cur_col >= num_cols:
                cur_col = 0
                cur_row += 1
        num_rows = cur_row

        #create borders around edge of map
        top_n_bottom = (-1,num_rows)
        for i in top_n_bottom:
            for j in range(-1,num_cols+1):
                self.things.append(thing.Thing({'location':[j,i],'dimensions':[self.grid_size,self.grid_size],"on_collision":{"type":"block","actions":[]}},self.grid_size))
        sides = (-1,num_cols)
        for i in range(0,num_rows):
            for j in sides:
                self.things.append(thing.Thing({'location':[j,i],'dimensions':[self.grid_size,self.grid_size],"on_collision":{"type":"block","actions":[]}},self.grid_size))


class CombatScene(Scene):

    def __init__(self):
        data = {"background_image_path":"../assets/backgrounds/combat.png"}
        super().__init__(data)


