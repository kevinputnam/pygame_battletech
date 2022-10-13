import pygame
import scene
from pygame.locals import *

# Globals
gameName = "Battletech : Pirate's Bane"
scaling = 3
winWidth = 240
winHeight = 160

# main buttons
b_start = pygame.K_RETURN
b_select = pygame.K_RSHIFT

# game buttons
b_left = pygame.K_LEFT
b_right = pygame.K_RIGHT
b_up = pygame.K_UP
b_down = pygame.K_DOWN
b_a = pygame.K_a
b_b = pygame.K_s

debug_wait_time = 500

class GameWorld():


    def __init__(self):

        self.current_scene_id = 0
        self.collision_rects = []
        self.npcs = []
        self.player = None
        self.player_pos = (0,0)
        self.current_scene = None

    def setup_scenes(self):
        # setup scenes
        scene0 = scene.Scene(0,"my logo",'assets/backgrounds/logoscreen.bmp',None)
        scene0.actions = [{'name':'start_timer','milliseconds':debug_wait_time},
                          {'name':'change_scene','scene_id':1}]
        scene1 = scene.Scene(1,"battletech logo",'assets/backgrounds/titlescreen.bmp',None)
        scene1.actions = [{'name':'start_timer','milliseconds':debug_wait_time},
                          {'name':'change_scene','scene_id':2}]
        scene2 = scene.Scene(2,"jamie grear splash",'assets/backgrounds/jamie_grear.png',None)
        scene2.actions = [{'name':'start_timer','milliseconds':debug_wait_time},
                          {'name':'change_scene','scene_id':3}]
        scene3 = scene.Scene(3,"campus map",'assets/backgrounds/campus.png','assets/sprites/dog.png')
        scene3.collisions = [(6,28),(7,28),(8,28),(9,28),(10,28),(11,28),
                             (12,28),(13,28),(14,28),(15,28),(16,28),(17,28),
                             (6,29),(6,30),(6,31),(6,32),(6,33),(6,34),(6,35),
                             (7,35),(8,35),(9,35),(10,35),(11,35),(12,35),
                             (13,35),(13,34),(13,33),(14,33),(15,33),(16,33),
                             (17,33),(17,32),(17,31),(17,30),(17,29),
                             (22,42),(23,42),(24,42),(25,42),(26,42),(27,42),
                             (22,43),(23,43),(24,43),(25,43),(26,43),(27,43),
                             (22,44),(23,44),(24,44),(25,44),(26,44),(27,44),
                             (22,45),(23,45),(24,45),(25,45),(26,45),(27,45)]
        return {0:scene0,1:scene1,2:scene2,3:scene3}

    def start_scene(self,scene_id):
        self.collision_rects = []
        self.npcs = []
        self.player = None
        self.current_scene_id = scene_id
        self.current_scene = self.scenes[scene_id]
        for collision in self.current_scene.collisions:
            colBlock = pygame.Surface((8,8))
            colBlock.set_alpha(128)
            colBlock.fill((255,255,255))
            self.collision_rects.append({'surface':colBlock,'location':collision
                })
        if self.current_scene.player:
            self.player = self.current_scene.player

    def main(self):
        # Initialise screen
        pygame.init()
        screen = pygame.display.set_mode((winWidth*scaling, winHeight*scaling))
        pygame.display.set_caption(gameName)
        win = pygame.Surface((winWidth,winHeight))

        self.scenes = self.setup_scenes()

        text = None
        current_action = None
        waiting = False
        wait_end_time = 0
        background_x = 0
        background_y = 0
        controller_dx = 1
        controller_dy = 1
        offset_x = 0
        offset_y = 0
        player_offset_x = 0
        player_offset_y = 0
        self.start_scene(0)

        # Main event loop
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == b_start:
                        print('return key pressed.')
                    if event.key == b_select:
                        print('select key pressed.')
                    if not waiting:
                        if event.key == b_a:
                            # Display some text
                            font = pygame.font.Font(None, 24)
                            text = font.render("Hello There", 1, (255, 255, 255))
                            textpos = text.get_rect()
                            textpos.centerx = win.get_rect().centerx
                            print('a button pressed.')
                        if event.key == b_b:
                            text = None
                            print('b button pressed.')


            if not waiting:
                keys = pygame.key.get_pressed()
                dx = 0
                dy = 0
                if keys[b_left]:
                    dx += controller_dx
                if keys[b_right]:
                    dx -= controller_dx
                if keys[b_up]:
                    dy += controller_dy
                if keys[b_down]:
                    dy -= controller_dy
                if self.current_scene.actions:
                    current_action = self.current_scene.actions.pop(0)
                else:
                    current_action = None
                if current_action:
                    if current_action['name'] == 'start_timer':
                        wait_end_time = current_action['milliseconds'] + pygame.time.get_ticks()
                        waiting = True
                        print('timer ending: ' + str(wait_end_time))

                    if current_action['name'] == 'change_scene':
                        print('changing scene')
                        self.start_scene(current_action['scene_id'])
            else:
                if pygame.time.get_ticks() >= wait_end_time:
                    waiting = False
                    print('timer ended')

            if self.player:
                player_rect = self.player.get_rect(topleft =self.player_pos)
                for collision in self.collision_rects:
                    col_rect_dx = collision['surface'].get_rect(topleft=(collision['location'][0]*8+offset_x+dx,collision['location'][1]*8+offset_y))
                    col_rect_dy = collision['surface'].get_rect(topleft=(collision['location'][0]*8+offset_x,collision['location'][1]*8+offset_y+dy))
                    if player_rect.colliderect(col_rect_dx):
                        dx = 0
                    if player_rect.colliderect(col_rect_dy):
                        dy = 0

            offset_player_x = True
            if offset_x + dx > 0:
                offset_x = 0
            elif offset_x + dx < winWidth - self.current_scene.background.get_width():
                offset_x = winWidth - self.current_scene.background.get_width()
            else:
                offset_x += dx
                offset_player_x = False

            offset_player_y = True
            if offset_y + dy > 0:
                offset_y = 0
            elif offset_y + dy < winHeight - self.current_scene.background.get_height():
                offset_y = winHeight - self.current_scene.background.get_height()
            else:
                offset_y += dy
                offset_player_y = False

            if offset_player_x:
                if self.player_pos[0] - dx <= winWidth - self.player.get_width() and self.player_pos[0] -dx >= 0:
                    player_offset_x -= dx

            if offset_player_y:
                if self.player_pos[1] - dy <= winHeight - self.player.get_height() and self.player_pos[1] - dy >= 0:
                    player_offset_y -= dy

            win.blit(self.current_scene.background,(background_x + offset_x,background_y+offset_y))

            for collision in self.collision_rects:
                win.blit(collision['surface'],(collision['location'][0]*8 + offset_x,collision['location'][1]*8 + offset_y))
            if self.player:
                self.player_pos = (win.get_rect().centerx+player_offset_x,win.get_rect().centery+player_offset_y)
                win.blit(self.player,self.player_pos)
            if text:
                win.blit(text, textpos)
            scaled_win = pygame.transform.scale(win,screen.get_size())
            screen.blit(scaled_win, (0, 0))
            pygame.display.flip()

game = GameWorld()
game.main()