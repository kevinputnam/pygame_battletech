import json
import scene
import thing
import re
import gui
import messages
from os.path import isfile

class World():

    def __init__(self,world_path):
        data = self.load(world_path)
        self.variables = {}
        for key in data:
            setattr(self,key,data[key])
        self.scenes = []
        for s in data['scenes']:
            self.scenes.append(scene.Scene(s))
        gui.initialize_display(self.gamename)
        self.initialize_scene(self.first_scene,self.start_player_pos)

        self.move_base = 1
        self.current_scene_id = 0
        self.message_topline = 0
        self.message_textlist = []
        self.menu_options = []
        self.menu_cursor_index = 0
        self.menu_option_num = 0
        self.waiting = False

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

    # main game loop
    def start(self):
        while 1:
            gui.process_user_input()
            self.process_player_collisions()
            self.run_actions()
            self.process_movement()
            gui.update_gui()

    def test_method(self,args):
        print('oh, ho! ' + args['text'] + ' pressed!')

    def move_player(self,args):
        if args['axis'] == 'y':
            self.player.dy = args['value']
        elif args['axis'] == 'x':
            self.player.dx = args['value']
        self.player.direction = args['direction']

    def initialize_scene(self,scene_id,player_pos):
        self.actions = []
        self.things = []
        self.current_scene_id = scene_id
        gui.load_new_scene(self.scenes[scene_id].background,self.scenes[scene_id].map_size)
        # reset action and thing lists
        self.player = self.scenes[scene_id].player
        if self.player:
            grid_size = self.scenes[scene_id].grid_size
            self.player.location = [player_pos[0]*grid_size,player_pos[1]*grid_size]
            if self.player.sprite:
                gui.add_player(self.player)
        self.things = []
        self.actions = []
        for action in self.scenes[scene_id].actions:
            self.actions.append(action)
        for t in self.scenes[scene_id].things:
            self.things.append(t)
            if t.sprite:
                gui.add_thing(t)
        self.set_map_nav_button_behaviors()

    def set_map_nav_button_behaviors(self):
        gui.button_behaviors['start'] = [self.test_method,{'text':'start'}]
        gui.button_behaviors['select'] = [self.test_method,{'text':'select'}]
        gui.button_behaviors['a'] = [self.test_method,{'text':'a'}]
        gui.button_behaviors['b'] = [self.test_method,{'text':'b'}]
        gui.button_behaviors['e_up'] = [self.test_method,{'text':'up'}]
        gui.button_behaviors['e_down'] = [self.test_method,{'text':'down'}]
        gui.button_behaviors['left'] = [self.move_player,{'axis':'x','value':-1,'direction':'left'}]
        gui.button_behaviors['right'] = [self.move_player,{'axis':'x','value':1,'direction':'right'}]
        gui.button_behaviors['up'] = [self.move_player,{'axis':'y','value':-1,'direction':'up'}]
        gui.button_behaviors['down'] = [self.move_player,{'axis':'y','value':1,'direction':'down'}]

    def message_display(self, text_list):
        self.message_topline = 0
        self.message_textlist = text_list
        messages.build_message(text_list)
        self.waiting = True
        self.set_message_button_behaviors()

    def message_dismiss(self,args):
        gui.message = None
        self.message_topline = 0
        self.message_textlist = []
        self.waiting = False
        self.set_map_nav_button_behaviors()

    def message_scroll(self,args):
        if 'direction' in args:
            if args['direction'] == 'up':
                self.message_topline -= messages.max_lines
                if self.message_topline < 0:
                    self.message_topline = 0
            elif args['direction'] == 'down':
                self.message_topline += messages.max_lines
                if self.message_topline > len(self.message_textlist):
                    self.message_topline = len(self.message_textlist) - 1
        messages.build_message(self.message_textlist,self.message_topline)

    def set_message_button_behaviors(self):
        gui.button_behaviors['start'] = [self.test_method,{'text':'start'}]
        gui.button_behaviors['select'] = [self.test_method,{'text':'select'}]
        gui.button_behaviors['a'] = [self.test_method,{'text':'a'}]
        gui.button_behaviors['b'] = [self.message_dismiss,{}]
        gui.button_behaviors['e_up'] = [self.message_scroll,{'direction':'up'}]
        gui.button_behaviors['e_down'] = [self.message_scroll,{'direction':'down'}]
        gui.button_behaviors['left'] = [self.test_method,{'text':'left'}]
        gui.button_behaviors['right'] = [self.test_method,{'text':'right'}]
        gui.button_behaviors['up'] = [self.test_method,{'text':'up'}]
        gui.button_behaviors['down'] = [self.test_method,{'text':'down'}]

    def menu_display(self,options,variable):
        self.waiting = True
        self.menu_option_num = len(options)
        self.menu_options = options
        messages.build_menu(options,0)
        self.set_menu_button_behaviors(variable)

    def menu_select(self,args):
        self.variables[args['variable']] = self.menu_cursor_index
        print(self.menu_cursor_index)
        self.message_dismiss(args)

    def menu_nav(self,args):
        if 'direction' in args:
            if args['direction'] == 'up':
                self.menu_cursor_index -= 1
                if self.menu_cursor_index < 0:
                    self.menu_cursor_index = self.menu_option_num - 1
            elif args['direction'] == 'down':
                self.menu_cursor_index += 1
                if self.menu_cursor_index >= self.menu_option_num:
                    self.menu_cursor_index = 0
        messages.build_menu(self.menu_options,self.menu_cursor_index)

    def set_menu_button_behaviors(self,variable):
        self.set_message_button_behaviors()
        gui.button_behaviors['e_up'] = [self.menu_nav,{'direction':'up'}]
        gui.button_behaviors['e_down'] = [self.menu_nav,{'direction':'down'}]
        gui.button_behaviors['a'] = [self.menu_select,{'variable':variable}]

    def player_off_map(self):
        if self.player:
            if self.player.location[0] + self.player.dx > self.scenes[self.current_scene_id].map_size[0] - self.player.dimensions[0] or self.player.location[0] + self.player.dx  < 0:
                self.player.dx = 0
            elif self.player.location[1] + self.player.dy > self.scenes[self.current_scene_id].map_size[1] - self.player.dimensions[1] or self.player.location[1] + self.player.dy < 0:
                self.player.dy = 0

    def process_movement(self):
        if self.player:
            self.player.location = [self.player.location[0] + self.player.dx,self.player.location[1]+self.player.dy]
            self.player.dx = 0
            self.player.dy = 0
            if self.player.sprite:
                self.player.sprite.update(self.player.direction,self.player.location[0],self.player.location[1])
            self.player.direction = 'none'

            gui.update_camera_pos(self.player.location[0],self.player.location[1])

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
                    if t.trigger and t.triggered:
                        return
                    if t.on_collision:
                        for action in t.on_collision['actions']:
                            self.actions.append(action)
                        getattr(self,'collision_'+t.on_collision['name'],self.collision_default)(self.player,t,None)
                else:
                    if t.trigger:
                        t.triggered = False

    def collision(self,rect1,rect2):
        dx = min(rect1[2], rect2[2]) - max(rect1[0], rect2[0])
        dy = min(rect1[3], rect2[3]) - max(rect1[1], rect2[1])
        if (dx>0) and (dy>0):
            return True
        else:
            return False

    #### Action Handler

    def run_actions(self):
        if not gui.timer_active and not self.waiting:
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
                    if t.on_collision['name'] == 'block':
                        actor.dx = 0
                        actor.dy = 0
                        return
        receiver.dx = actor.dx
        receiver.dy = actor.dy

    def collision_block(self,actor,reciever,arg_list):
        actor.dx = 0
        actor.dy = 0

    def collision_once(self,actor,receiver,arg_list):
        receiver.triggered = True

    def collision_default(self,actor,receiver,arg_list):
        print("Invalid collision: " + receiver.on_collision['name'])

    #### Actions

    def action_start_timer(self,action):
        gui.start_timer(int(self.get_param(action['milliseconds'])))

    def action_change_scene(self,action):
        player_pos = [0,0]
        if 'player_pos' in action:
            player_pos = action['player_pos']
        self.initialize_scene(action['scene_id'],player_pos)

    def action_message(self,action):
        self.message_display(action['text_lines'])

    def action_menu(self,action):
        self.menu_display(action['options'],action['variable'])

    def action_default(self,action):
        print("Invalid action: " + action['name'])