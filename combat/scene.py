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
        self.map_based = False

        for key in scene_data:
            if key != 'things':
                setattr(self,key,scene_data[key])

        if 'things' in scene_data:
            for t in scene_data['things']:
                self.things.append(thing.Thing(t,self.grid_size))

        if self.map_based:
            self.add_collisions()
        ui.load_scene(self.background_image_path,self.map_size)

    def run(self,user_input):
        pass

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

    def __init__(self,args):
        self.player_mechs = args['player_mechs']
        self.opposing_mechs = args['opposing_mechs']
        self.head_counter = 0
        self.torso_counter = 0
        self.l_arm_counter = 0
        self.r_arm_counter = 0
        self.l_leg_counter = 0
        self.r_leg_counter = 0
        self.heat_level = 0
        self.heat_bar = None

        data = {"background_image_path":"../assets/backgrounds/combat.png"}
        super().__init__(data)

        self.player_mechs[0].sprite.update('right',17,10)
        self.opposing_mechs[0].sprite.update('left',217,10)

        mech_shadow_1 = actor.Actor(17,166,"../assets/sprites/mech_shadow.png", [128,32],{"none":[0]})
        mech_shadow_2 = actor.Actor(217,166,"../assets/sprites/mech_shadow.png", [128,32],{"none":[0]})

        status_bkg = actor.Actor(17,200,"../assets/sprites/status_mech_bkg.png", [16,25], {"none":[0]})
        self.status_head = actor.Actor(22,201,"../assets/sprites/status_mech_head.png", [6,6], {"green":[0],"yellow":[1],"red":[2],"black":[3]})
        self.status_l_arm = actor.Actor(17,206,"../assets/sprites/status_mech_l_arm.png", [4,10], {"green":[0],"yellow":[1],"red":[2],"black":[3]})
        self.status_torso = actor.Actor(21,206,"../assets/sprites/status_mech_torso.png", [8,8], {"green":[0],"yellow":[1],"red":[2],"black":[3]})
        self.status_r_arm = actor.Actor(29,206,"../assets/sprites/status_mech_r_arm.png", [4,10], {"green":[0],"yellow":[1],"red":[2],"black":[3]})
        self.status_l_leg = actor.Actor(21,213,"../assets/sprites/status_mech_l_leg.png", [4,11], {"green":[0],"yellow":[1],"red":[2],"black":[3]})
        self.status_r_leg = actor.Actor(25,213,"../assets/sprites/status_mech_r_leg.png", [4,11], {"green":[0],"yellow":[1],"red":[2],"black":[3]})
        ui.add_sprite(status_bkg)
        ui.add_sprite(self.status_head)
        ui.add_sprite(self.status_l_arm)
        ui.add_sprite(self.status_torso)
        ui.add_sprite(self.status_r_arm)
        ui.add_sprite(self.status_l_leg)
        ui.add_sprite(self.status_r_leg)
        ui.add_sprite(mech_shadow_1)
        ui.add_sprite(mech_shadow_2)
        ui.add_sprite(self.player_mechs[0].sprite)
        ui.add_sprite(self.opposing_mechs[0].sprite)

        ui.draw_rectangle([10,195],[340,40],(0,0,0))
        ui.draw_rectangle([39,200],[7,32],(89,86,82))


    def run(self,user_input):
        statuses = ["green","yellow","red","black"]

        if "a" in user_input:
            self.head_counter += 1
            if self.head_counter >= 4:
                self.head_counter =0
            status = statuses[self.head_counter]
            self.status_head.update(status,None,None)

        if "b" in user_input:
            self.l_arm_counter += 1
            if self.l_arm_counter >= 4:
                self.l_arm_counter = 0
            status = statuses[self.l_arm_counter]
            self.status_l_arm.update(status,None,None)

        if "event_left" in user_input:
            self.heat_level -= 1
            if self.heat_level < 0:
                self.heat_level = 0

        if "event_right" in user_input:
            self.heat_level += 1
            if self.heat_level >= 11:
                self.heat_level = 10

        heat_bar_height = 3*self.heat_level
        heat_bar_y_offset = 30 - heat_bar_height
        heat_bar_width = 5
        heat_bar_color = (0,255,0) #green
        if self.heat_level > 3 and self.heat_level <= 6:
            heat_bar_color = (255,255,0) #yellow
        elif self.heat_level > 6:
            heat_bar_color = (255,0,0)
        location = [40,201+heat_bar_y_offset]
        dimensions = [heat_bar_width,heat_bar_height]

        if self.heat_bar:
            ui.remove_rectangle(self.heat_bar)
        self.heat_bar = ui.draw_rectangle(location,dimensions,heat_bar_color)


