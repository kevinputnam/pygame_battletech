import pygame


# line lengths should be approximately 40 characters
# it will display no more than 6 lines of text
def build_message(lines_of_text):
    max_lines = 6
    line_height = 14
    font = pygame.font.Font(None, 16)

    line_rects = []
    line_counter = 0
    for line in lines_of_text:
        line_rect = font.render(line,1,(0,0,0))
        line_counter += 1
        line_rects.append(line_rect)

    if line_counter > max_lines:
        line_counter = max_lines

    # add an extra line for dismiss value
    message_box_height = (line_counter+1) * line_height + 6
    message_box = pygame.Surface((224,message_box_height))
    message_box.fill((255, 255, 240))

    message_container = pygame.Surface((232,message_box_height + 8))
    message_container.fill((136, 8, 8))

    dismiss_text = font.render("press B",1,(0,0,0))
    dismiss_pos = dismiss_text.get_rect()
    dismiss_pos.bottomright = (220,message_box_height - 4)

    line_counter = 0
    for line_rect in line_rects:
        if line_counter == max_lines:
            break
        line_pos = line_rect.get_rect()
        line_pos.topleft = (4,4+line_height*line_counter)
        message_box.blit(line_rect,line_pos)
        line_counter += 1

    message_box.blit(dismiss_text,dismiss_pos)
    message_container.blit(message_box,(4,4))

    return (message_box_height+8, message_container)