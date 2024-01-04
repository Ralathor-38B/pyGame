import pygame
from button import Button
from function_load_image import load_image
import game


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
    start_x, start_y = 100, 200
    str_len = 16
    current_number = 1
    level_buttons = []
    for i in range(5):
        for j in range(3):
            x, y = start_x + w * j, start_y + h * i
            current_text = str(current_number).center(str_len)
            cur_button = Button(screen, x, y, (185, 139, 240), text=current_text, color_t=(240, 235, 245), size_t=25)
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
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for index in range(len(level_buttons)):
                    if level_buttons[index].get_click(x, y):
                        level_number = index + 1
                        start_level(level_number)
                        running = False
        pygame.display.flip()


def start_level(number):
    reg, a, b, s = game.level(number)
    game.play(reg, a, b, s)


if __name__ == "__main__":
    show_level_panel()
