import sqlite3

import pygame

import level_panel as panel
import selection as sel
from button import Button


def choice_page():
    pygame.init()
    sc = pygame.display.set_mode((500, 670))
    play = Button(sc, 150, 135, image='play_btn.png')
    char = Button(sc, 100, 420, border='blue', text='Выбрать персонажа', size_t=15)
    ground = Button(sc, 270, 420, border='blue', text='Выбрать локацию', size_t=15)
    level = Button(sc, 200, 500, border='red', text='Настройки уровня', size_t=13)
    buttons = [play, char, ground, level]
    con = sqlite3.connect('levels_settings')
    cur = con.cursor()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             pygame.key.get_pressed()[pygame.K_ESCAPE]):
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play.get_click(x, y):
                    panel.start_level(cur.execute('''SELECT id FROM levels_score WHERE current = 1''').fetchone()[0])
                if char.get_click(x, y):
                    sel.pick_page('Choose your character', ['hero/wizard'], 0)
                if ground.get_click(x, y):
                    sel.pick_page('Choose location', ['backgrounds'], 0, ind=1)
                if level.get_click(x, y):
                    panel.show_level_panel()
        sc.fill((20, 0, 50))
        for b in buttons:
            b.draw()
        pygame.display.flip()


if __name__ == '__main__':
    choice_page()
