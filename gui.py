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

def initialize_display(gameName):
    global screen
    global win
    global clock

    pygame.init()
    screen = pygame.display.set_mode((WINWIDTH*SCALING, WINHEIGHT*SCALING))
    pygame.display.set_caption(gameName)
    win = pygame.Surface((WINWIDTH,WINHEIGHT))
    clock = pygame.time.Clock()

def update_gui():
    global timer_active
    global timer_end_time

    if timer_end_time != 0:
        if pygame.time.get_ticks() >= timer_end_time:
            timer_active = False
            timer_end_time = 0
    win.blit(background,(0,0))
    the_sprites.draw(win)
    scaled_win = pygame.transform.scale(win,screen.get_size())
    screen.blit(scaled_win, (0, 0))
    pygame.display.flip()
    clock.tick(60)

def add_thing(thing):
    the_sprites.add(thing.sprite)


def process_user_input():

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == B_START:
                button_behaviors['start'][0](button_behaviors['start'][1])
            if event.key == B_SELECT:
                button_behaviors['select'][0](button_behaviors['select'][1])
            if event.key == B_A:
                button_behaviors['a'][0](button_behaviors['a'][1])
            if event.key == B_B:
                button_behaviors['b'][0](button_behaviors['b'][1])

    keys = pygame.key.get_pressed()
    if keys[B_LEFT]:
        button_behaviors['left'][0](button_behaviors['left'][1])
    if keys[B_RIGHT]:
        button_behaviors['right'][0](button_behaviors['right'][1])
    if keys[B_UP]:
        button_behaviors['up'][0](button_behaviors['up'][1])
    if keys[B_DOWN]:
        button_behaviors['down'][0](button_behaviors['down'][1])

def load_new_scene(background_path):
    global background

    background = pygame.image.load(background_path)

def show_modal():
    pass

def start_timer(milliseconds):
    global timer_active
    global timer_end_time

    timer_active = True
    timer_end_time = milliseconds + pygame.time.get_ticks()