import pygame

from button import Button
from function_load_image import load_image

CURRENT = [0, 2]  # cur character, cur location


def right_ar(sc, n, stop):
    if n < stop:
        return Button(sc, 430, 220, image='right.png')


def left_ar(sc, n):
    if n > 0:
        return Button(sc, 50, 220, image='left.png')


def draw(sc, width, title, folder_list, n, ind=0):
    chosen = CURRENT[ind] == n

    font = pygame.font.SysFont('constantia', 25)
    text = font.render(title, True, 'white')
    rect = text.get_rect()
    rect.x, rect.y = (width - rect.width) // 2, 70
    sc.blit(text, rect)
    btn = None

    if n < len(folder_list):
        folder = folder_list[n]
        img = load_image('Idle.png', folder, -1)
        w = img.get_width()
        sc.blit(img, ((width - w) // 2, 150))
        if chosen:
            btn = Button(sc, 230, 400, (0, 250, 255), '  Chosen  ', t_family='constantia')
        else:
            btn = Button(sc, 230, 400, (250, 0, 255), '  Select  ', t_family='constantia')

    left = left_ar(sc, n)
    right = right_ar(sc, n, len(folder_list))

    if n >= len(folder_list):
        text1 = font.render('end', True, 'white')
        rect = text1.get_rect()
        rect.x, rect.y = (width - rect.width) // 2, 200
        sc.blit(text1, rect)

    return btn, left, right


def pick_page(title, folder_list, n, ind=0):
    pygame.init()
    size = width, height = 540, 500
    sc = pygame.display.set_mode(size)
    sc.fill((10, 0, 50))
    running = True

    btn, left, right = draw(sc, width, title, folder_list, n, ind)
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             pygame.key.get_pressed()[pygame.K_ESCAPE]):
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if btn and btn.get_click(x, y):
                    CURRENT[ind] = n
                    sc.fill((10, 0, 50))
                    btn, left, right = draw(sc, width, title, folder_list, n, ind)
                    pygame.display.flip()
                if left and left.get_click(x, y):
                    sc.fill((10, 0, 50))
                    btn, left, right = draw(sc, width, title, folder_list, n - 1, ind)
                    pygame.display.flip()
                if right and right.get_click(x, y):
                    sc.fill((10, 0, 50))
                    btn, left, right = draw(sc, width, title, folder_list, n + 1, ind)
                    pygame.display.flip()


if __name__ == '__main__':
    # pick_page('Choose your character', ['hero/wizard'], 0)
    pick_page('Choose location', ['backgrounds'], 0, ind=1)
