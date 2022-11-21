import sys
import pygame
from pygame.locals import *

SCALING = 2
WINWIDTH = 360
WINHEIGHT = 240

# Controller buttons
B_START = pygame.K_RETURN
B_SELECT = pygame.K_RSHIFT
B_LEFT = pygame.K_LEFT
B_RIGHT = pygame.K_RIGHT
B_UP = pygame.K_UP
B_DOWN = pygame.K_DOWN
B_A = pygame.K_a
B_B = pygame.K_s

win = None
screen = None
background= None
clock = None
timer_active = False
timer_end_time = 0
button_behaviors = {}
the_sprites = pygame.sprite.Group()
player_sprite = None
map_size_x = 0
map_offset_x = 0
map_offset_y = 0
message = None
message_height = 0

def initialize_screen(gameName):
    global screen
    global win
    global clock

    pygame.init()
    screen = pygame.display.set_mode((WINWIDTH*SCALING, WINHEIGHT*SCALING))
    pygame.display.set_caption(gameName)
    win = pygame.Surface((WINWIDTH,WINHEIGHT))
    clock = pygame.time.Clock()

def update_camera_pos(player_x,player_y):
    global map_offset_x
    global map_offset_y
    global player_sprite

    p_x = player_x
    p_y = player_y

    #maximum offsets for the map
    max_map_x = WINWIDTH - map_size_x
    max_map_y = WINHEIGHT - map_size_y

    # shift map under player at center screen
    map_offset_x = int(WINWIDTH/2 - p_x)
    map_offset_y = int(WINHEIGHT/2 - p_y)

    player_offset_x = 0
    player_offset_y = 0

    # if the map needs to move to the right - move player left (-)
    if map_offset_x > 0:
        player_offset_x = -1 * map_offset_x
        map_offset_x = 0
    # if the map has gone as far as it can - move the player right (+)
    elif map_offset_x < max_map_x:
        player_offset_x = -1*(map_offset_x - max_map_x)
        map_offset_x = max_map_x

    # if the map needs to move down - move player up (-)
    if map_offset_y > 0:
        player_offset_y = -1 * map_offset_y
        map_offset_y = 0
    # if the map has gone as far up as it can - move the player down (+)
    elif map_offset_y < max_map_y:
        player_offset_y = -1*(map_offset_y - max_map_y)
        map_offset_y = max_map_y
    if player_sprite:
        player_sprite.rect.topleft = (win.get_rect().centerx+player_offset_x, win.get_rect().centery+player_offset_y)


def update_screen():
    global timer_active
    global timer_end_time

    if timer_end_time != 0:
        if pygame.time.get_ticks() >= timer_end_time:
            timer_active = False
            timer_end_time = 0
    win.blit(background,(map_offset_x,map_offset_y))
    the_sprites.draw(win)
    if player_sprite:
        win.blit(player_sprite.image,player_sprite.rect.topleft)
    if message:
        win.blit(message,(4,WINHEIGHT - message_height - 4))
    scaled_win = pygame.transform.scale(win,screen.get_size())
    screen.blit(scaled_win, (0, 0))
    pygame.display.flip()
    clock.tick(60)

def add_sprite(thing):
    the_sprites.add(thing.sprite)

def remove_sprite(thing):
    the_sprites.remove(thing.sprite)

def add_player(thing):
    global player_sprite

    player_sprite = thing.sprite
    player_sprite.camera_focus = True

def process_user_input():
    button_pushes = []
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == B_START:
                button_pushes.append("start")
            if event.key == B_SELECT:
                button_pushes.append("select")
            if event.key == B_A:
                button_pushes.append("a")
            if event.key == B_B:
                button_pushes.append("b")
            if event.key == B_UP:
                button_pushes.append("event_up")
            if event.key == B_DOWN:
                button_pushes.append("event_down")
            if event.key == B_RIGHT:
                button_pushes.append("event_right")
            if event.key == B_LEFT:
                button_pushes.append("event_left")


    keys = pygame.key.get_pressed()
    if keys[B_LEFT]:
        button_pushes.append("left")
    if keys[B_RIGHT]:
        button_pushes.append("right")
    if keys[B_UP]:
        button_pushes.append("up")
    if keys[B_DOWN]:
        button_pushes.append("down")

    return button_pushes

def load_scene(background_path,map_size):
    global background
    global map_size_x
    global map_size_y
    global map_offset_x
    global map_offset_y
    global player_sprite

    if background_path:
        map_offset_x = 0
        map_offset_y = 0
        map_size_x = map_size[0]
        map_size_y = map_size[1]
        background = pygame.image.load(background_path)
    the_sprites.empty()
    player_sprite = None

def start_timer(milliseconds):
    global timer_active
    global timer_end_time

    timer_active = True
    timer_end_time = milliseconds + pygame.time.get_ticks()