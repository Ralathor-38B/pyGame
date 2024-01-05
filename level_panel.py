import sqlite3

import pygame

import game
import level_results as res
from button import Button
from function_load_image import load_image


def show_level_panel():
    pygame.init()
    pygame.display.set_caption("Выбор уровня")
    back_filename = 'star_sky3.jpg'
    size = width, height = 650, 640
    back_image = pygame.transform.scale(load_image(back_filename), (width, height))
    im_rect = (0, 0, width, height)
    screen = pygame.display.set_mode(size)
    screen.blit(back_image, im_rect)
    w, h = 150, 60
    start_x, start_y = 115, 200
    str_len = 16
    current_number = 1
    level_buttons = []

    con = sqlite3.connect('levels_settings')
    cur = con.cursor()
    res = cur.execute('''SELECT id FROM levels_score WHERE opened = 1 ''').fetchall()
    opened = [i[0] for i in res]
    for i in range(5):
        for j in range(3):
            x, y = start_x + w * j, start_y + h * i
            current_text = str(current_number).center(str_len)
            if current_number in opened:
                cur_button = Button(screen, x, y, (185, 139, 240), text=current_text, color_t=(240, 235, 245),
                                    size_t=25)
            else:
                cur_button = Button(screen, x, y, (185, 139, 240), text=current_text, color_t=(240, 235, 245),
                                    size_t=25, image='block.png')
            level_buttons.append(cur_button)
            current_number += 1
    title_text, title_size = "Levels", 60
    title_color = (204, 166, 245)
    title_x, title_y = width // 2 - 90, 60
    font = pygame.font.SysFont('segoeuihistoric', title_size)
    text = font.render(title_text, True, title_color)
    screen.blit(text, (title_x, title_y))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                for index in range(len(level_buttons)):
                    if level_buttons[index].get_click(x, y) and index + 1 in opened:
                        pygame.quit()
                        level_number = index + 1
                        cur.execute('''UPDATE levels_score SET current = 0 WHERE id < 16''')
                        cur.execute('''UPDATE levels_score SET current = 1 WHERE id = ?''', (index + 1,))
                        con.commit()
                        start_level(level_number)
                        running = False
        pygame.display.flip()


def start_level(number):
    reg, a, b, s = game.level(number)
    game.play(reg, a, b, s, number)


if __name__ == "__main__":
    res.start_screen()
    show_level_panel()
