import json
import scene
import thing
import re
import gui
from os.path import isfile

class World():

    def __init__(self,world_path):
        data = self.load(world_path)
        for key in data:
            setattr(self,key,data[key])
        self.scenes = []
        for s in data['scenes']:
            self.scenes.append(scene.Scene(s))
        ## added for refactor
        self.actions = []
        self.actors = []
        self.things = []
        gui.initialize_display(self.gamename)
        self.initialize_scene(self.first_scene,self.start_player_pos)

        self.move_base = 1

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
            self.process_player_collisions()
            self.run_actions()
            self.process_movement()
            gui.update_gui()

    def test_method(self,args):
        print('oh, ho! ' + args['text  '] + ' pressed!')

    def move_player(self,args):
        if args['axis'] == 'y':
            self.player.dy = args['value']
        elif args['axis'] == 'x':
            self.player.dx = args['value']
        self.player.direction = args['direction']


    def initialize_scene(self,scene_id,player_pos):
        gui.load_new_scene(self.scenes[scene_id].background)
        # reset action and thing lists
        self.player = self.scenes[scene_id].player
        if self.player:
            grid_size = self.scenes[scene_id].grid_size
            self.player.location = [player_pos[0]*grid_size,player_pos[1]*grid_size]
            if self.player.sprite:
                gui.add_thing(self.player)
        self.things = []
        self.actions = []
        for action in self.scenes[scene_id].actions:
            self.actions.append(action)
        for t in self.scenes[scene_id].things:
            self.things.append(t)
            if t.sprite:
                gui.add_thing(t)
        gui.button_behaviors['start'] = [self.test_method,{'text':'start'}]
        gui.button_behaviors['select'] = [self.test_method,{'text':'select'}]
        gui.button_behaviors['a'] = [self.test_method,{'text':'a'}]
        gui.button_behaviors['b'] = [self.test_method,{'text':'b'}]
        gui.button_behaviors['left'] = [self.move_player,{'axis':'x','value':-1,'direction':'left'}]
        gui.button_behaviors['right'] = [self.move_player,{'axis':'x','value':1,'direction':'right'}]
        gui.button_behaviors['up'] = [self.move_player,{'axis':'y','value':-1,'direction':'up'}]
        gui.button_behaviors['down'] = [self.move_player,{'axis':'y','value':1,'direction':'down'}]

    def process_movement(self):
        if self.player:
            self.player.location = [self.player.location[0] + self.player.dx,self.player.location[1]+self.player.dy]
            self.player.dx = 0
            self.player.dy = 0
            if self.player.sprite:
                self.player.sprite.update(self.player.direction,self.player.location[0],self.player.location[1])
            self.player.direction = 'none'

        for t in self.things:
            t.location = [t.location[0]+t.dx,t.location[1]+t.dy]
            t.dx = 0
            t.dy = 0
            if t.sprite:
                t.sprite.update('none',t.location[0],t.location[1])

    #### Collision Handler
    def process_player_collisions(self):
        # is it going to collide?
        if self.player:
            player_rect = self.player.get_rect()
            player_rect[0] += self.player.dx
            player_rect[1] += self.player.dy
            player_rect[2] += self.player.dx
            player_rect[3] += self.player.dy
            for t in self.things:
                if self.collision(player_rect,t.get_rect()):
                    if t.on_collision:
                        getattr(self,'collision_'+t.on_collision[0],self.collision_default)(self.player,t,t.on_collision[1])

    def collision(self,rect1,rect2):
        dx = min(rect1[2], rect2[2]) - max(rect1[0], rect2[0])
        dy = min(rect1[3], rect2[3]) - max(rect1[1], rect2[1])
        if (dx>0) and (dy>0):
            return True
        else:
            return False

    #### Action Handler

    def run_actions(self):
        if not gui.timer_active:
            if self.actions:
                action = self.actions.pop(0)
                getattr(self,'action_'+action['name'],self.action_default)(action)

    #### Collisions

    def collision_push(self,actor,receiver,arg_list):
        # will need to check to see if this will collide into anything
        receiver_rect = receiver.get_rect()
        receiver_rect[0] += actor.dx
        receiver_rect[1] += actor.dy
        receiver_rect[2] += actor.dx
        receiver_rect[3] += actor.dy

        for t in self.things:
            if self.collision(receiver_rect,t.get_rect()):
                if t.on_collision:
                    if t.on_collision[0] == 'block':
                        actor.dx = 0
                        actor.dy = 0
                        return
        receiver.dx = actor.dx
        receiver.dy = actor.dy



    def collision_block(self,actor,reciever,arg_list):
        actor.dx = 0
        actor.dy = 0

    def collision_default(self,actor,receiver,arg_list):
        print("Invalid collision: " + receiver.on_collision[0])

    #### Actions

    def action_start_timer(self,action):
        gui.start_timer(int(self.get_param(action['milliseconds'])))

    def action_change_scene(self,action):
        player_pos = [0,0]
        if 'player_pos' in action:
            player_pos = action['player_pos']
        self.initialize_scene(action['scene_id'],player_pos)

    def action_default(self,action):
        print("Invalid action: " + action['name'])