import pygame
import world
import scene
import actor
import collision_maps
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

class GameWorld(world.World):

    def __init__(self,game_world_path):
        self.current_scene_id = 0
        self.collision_rects = []
        self.npcs = []
        self.player = None
        self.player_pos = (0,0)
        self.current_scene = None
        self.actions = []
        self.clock = pygame.time.Clock()
        self.moving_sprites = pygame.sprite.Group()
        super().__init__(game_world_path)

    def start_scene(self,scene_id,player_x,player_y):
        self.collision_rects = []
        self.npcs = []
        self.actions = []
        self.player = None
        self.current_scene_id = scene_id
        self.current_scene = self.scenes[scene_id]
        scene_columns = self.current_scene.background.get_width()/8
        cur_col = 0
        cur_row = 0

        #draw transparent collision blocks
        for tile in self.current_scene.collisions:
            if tile != 0:
                colBlock  = pygame.Surface((8,8))
                colBlock.set_alpha(128)
                colBlock.fill((255,255,255))
                collision = (cur_col,cur_row)
                self.collision_rects.append({'surface':colBlock,'location':collision})
            cur_col += 1
            if cur_col >= scene_columns:
                cur_col = 0
                cur_row += 1

        # fill the action queue
        for action in self.current_scene.actions:
            self.actions.append(action)

        if self.current_scene.player:
            self.player = self.current_scene.player
            self.player.rect.topleft = [player_x*8,player_y*8]
            self.player_pos = [player_x*8,player_y*8]

            self.moving_sprites.add(self.current_scene.player)

    def main(self):
        pygame.init()
        screen = pygame.display.set_mode((winWidth*scaling, winHeight*scaling))
        pygame.display.set_caption(gameName)
        win = pygame.Surface((winWidth,winHeight))

        text = None
        current_action = None
        waiting = False
        wait_end_time = 0
        background_x = 0
        background_y = 0
        controller_d = 2
        offset_x = 0
        offset_y = 0
        player_offset_x = 0
        player_offset_y = 0
        player_direction = 'none'
        self.start_scene(0,0,0)

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
                player_direction = 'none'
                if keys[b_left]:
                    dx += controller_d
                    player_direction = 'left'
                if keys[b_right]:
                    dx -= controller_d
                    player_direction = 'right'
                if keys[b_up]:
                    dy += controller_d
                    player_direction = 'up'
                if keys[b_down]:
                    dy -= controller_d
                    player_direction = 'down'
                if self.current_scene.actions:
                    current_action = self.actions.pop(0)
                else:
                    current_action = None
                if current_action:
                    if current_action['name'] == 'start_timer':
                        wait_end_time = int(self.getParam(current_action['milliseconds'])) + pygame.time.get_ticks()
                        waiting = True
                        print('timer ending: ' + str(wait_end_time))

                    if current_action['name'] == 'change_scene':
                        print('changing scene')
                        pos_x = 0
                        pos_y = 0
                        if 'player_pos' in current_action:
                            pos_x = current_action['player_pos'][0]
                            pos_y = current_action['player_pos'][1]
                        self.start_scene(current_action['scene_id'],pos_x,pos_y)

                        if self.player:

                            map_size_x = self.current_scene.background.get_width()
                            map_size_y = self.current_scene.background.get_height()
                            p_x = pos_x*8
                            p_y = pos_y*8

                            #maximum offsets for the map
                            max_map_x = winWidth - map_size_x
                            max_map_y = winHeight - map_size_y

                            # shift map under player at center screen
                            offset_x = int(winWidth/2 - p_x)
                            offset_y = int(winHeight/2 - p_y)

                            # if the map needs to move to the right - move player left (-)
                            if offset_x > 0:
                                player_offset_x = -1 * offset_x
                            # if the map has gone as far as it can - move the player right (+)
                            elif offset_x < max_map_x:
                                player_offset_x = -1*(offset_x - max_map_x)
                                offset_x = max_map_x

                            # if the map needs to move down - move player up (-)
                            if offset_y > 0:
                                player_offset_y = -1 * offset_y
                            # if the map has gone as far up as it can - move the player down (+)
                            elif offset_y < max_map_y:
                                player_offset_y = -1*(offset_y - max_map_y)
                                offset_y = max_map_y

            else:
                if pygame.time.get_ticks() >= wait_end_time:
                    waiting = False
                    print('timer ended')

            if self.player:
                player_rect = self.player.rect
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
                    if self.player_pos[0] - dx <= winWidth - self.player.sprite_size and self.player_pos[0] -dx >= 0:
                        player_offset_x -= dx

                if offset_player_y:
                    if self.player_pos[1] - dy <= winHeight - self.player.sprite_size and self.player_pos[1] - dy >= 0:
                        player_offset_y -= dy

            else:
                offset_x = 0
                offset_y = 0

            win.blit(self.current_scene.background,(background_x + offset_x,background_y+offset_y))

            for collision in self.collision_rects:
                win.blit(collision['surface'],(collision['location'][0]*8 + offset_x,collision['location'][1]*8 + offset_y))
            if self.player:
                self.player_pos = (win.get_rect().centerx+player_offset_x,win.get_rect().centery+player_offset_y)
            self.moving_sprites.draw(win)
            self.moving_sprites.update(player_direction,self.player_pos[0],self.player_pos[1])
            if text:
                win.blit(text, textpos)
            scaled_win = pygame.transform.scale(win,screen.get_size())
            screen.blit(scaled_win, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

game = GameWorld('test_world.json')
game.main()