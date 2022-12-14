import pygame
import gui

line_height = 14
#background_color = (230,230,250)# very light blue
#border_color = (0,0,0)# black
#text_color = (0,0,0)# black
background_color = (0,0,0) # black
border_color = (0,0,0) # black
text_color = (255,255,255)# white
max_lines = 6

def build_menu(options,cursor_index):
    num_options = len(options)
    option_lines = []
    for option in options:
        option_lines.append(' '*6 + option)

    font = pygame.font.Font(None, 16)
    cursor_rect = font.render('>',1,text_color)

    build_message(option_lines,dismiss_str='A - select / B - cancel')

    cursor_pos = cursor_rect.get_rect()
    cursor_pos.topleft = (8,8+line_height*cursor_index)
    gui.message.blit(cursor_rect,cursor_pos)

# line lengths should be approximately 40 characters
# it will display no more than 6 lines of text at a time
def build_message(lines_of_text, top_line=0, dismiss_str='press B'):
    scroll = False
    if len(lines_of_text) > max_lines:
        scroll = True
    font = pygame.font.Font(None, 16)

    line_rects = []
    line_counter = 0

    if scroll:
        ls = lines_of_text[top_line:top_line+max_lines]
        while len(ls) < max_lines: # pad it out if there aren't enough lines
            ls.append('')
        line_counter = max_lines
    else:
        ls = lines_of_text

    for line in ls:
        line_rect = font.render(line,1,text_color)
        line_counter += 1
        line_rects.append(line_rect)

    if line_counter > max_lines:
        line_counter = max_lines

    # add an extra line for dismiss value
    message_box_height = (line_counter+1) * line_height + 6
    message_box = pygame.Surface((gui.WINWIDTH-16,message_box_height))
    message_box.fill(background_color)

    message_container = pygame.Surface((gui.WINWIDTH-8,message_box_height +8))
    message_container.fill(border_color)

    dismiss_text = font.render(dismiss_str,1,text_color)
    dismiss_pos = dismiss_text.get_rect()
    dismiss_pos.bottomright = (gui.WINWIDTH-20,message_box_height - 4)

    line_counter = 0
    for line_rect in line_rects:
        if line_counter == max_lines:
            break
        line_pos = line_rect.get_rect()
        line_pos.topleft = (11,4+line_height*line_counter)
        message_box.blit(line_rect,line_pos)
        line_counter += 1

    if scroll:
        scroll_percent = top_line / (len(lines_of_text))
        arrow_rect = font.render("^",1,text_color)
        up_rect = arrow_rect
        up_pos = up_rect.get_rect()
        up_pos.topleft = (1,2)
        message_box.blit(up_rect,up_pos)
        down_rect = pygame.transform.rotate(arrow_rect,180)
        down_pos = down_rect.get_rect()
        down_pos.topleft = (1,message_box_height - 24)
        message_box.blit(down_rect,down_pos)

        scroll_rect = font.render("*",1,text_color)
        scroll_pos = scroll_rect.get_rect()
        total_vertical_distance = message_box_height - 24 -2 - 4
        vertical_pos =  2 + 4 + int(total_vertical_distance*scroll_percent)
        scroll_pos.topleft = [2,vertical_pos]
        message_box.blit(scroll_rect,scroll_pos)

    message_box.blit(dismiss_text,dismiss_pos)
    message_container.blit(message_box,(4,4))

    gui.message = message_container
    gui.message_height = message_box_height+8
