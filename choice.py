import pygame

from button import Button


def choice_page():
    pygame.init()
    sc = pygame.display.set_mode((500, 670))
    play = Button(sc, 150, 135, image='play_btn.png')
    char = Button(sc, 100, 420, border='blue', text='Выбрать персонажа', size_t=15)
    ground = Button(sc, 270, 420, border='blue', text='Выбрать локацию', size_t=15)
    level = Button(sc, 200, 500, border='red', text='Настройки уровня', size_t=13)
    buttons = [play, char, ground, level]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             pygame.key.get_pressed()[pygame.K_ESCAPE]):
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play.get_click(x, y):
                    pass
                if char.get_click(x, y):
                    pass
                if ground.get_click(x, y):
                    pass
                if level.get_click(x, y):
                    pass
        sc.fill((20, 0, 50))
        for b in buttons:
            b.draw()
        pygame.display.flip()


if __name__ == '__main__':
    choice_page()
