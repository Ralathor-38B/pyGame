from function_load_image import load_image
from random import randint
from button import Button
import pygame
import level_panel
import sys


def alter_start_screen():
    intro_text = ["Когда-нибудь", "здесь будет название"]
    screen = pygame.display.set_mode((500, 500))
    running = True

    fon = pygame.transform.scale(load_image(f'start/img{randint(1, 6)}.jpg'), (500, 500))
    screen.blit(fon, (0, 0))

    font1 = pygame.font.SysFont('comicsansms', 32)
    font2 = pygame.font.SysFont('comicsansms', 33)
    text_coord = 100

    for line in intro_text:
        text = font2.render(line, True, 'blue')
        intro_rect = text.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = (500 - intro_rect.width) // 2
        screen.blit(text, intro_rect)

        text = font1.render(line, 1, (255, 0, 255))
        intro_rect = text.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = (500 - intro_rect.width) // 2
        text_coord += intro_rect.height
        screen.blit(text, intro_rect)

        pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                running = False


def show_start_screen():
    pygame.init()
    pygame.display.set_caption("Start page")
    size = width, height = 800, 550
    screen = pygame.display.set_mode(size)
    background_filename = "whale_in_clouds.jpg" if randint(1, 100) == 27 else "clouds.jpg"
    background_image = pygame.transform.scale(load_image(name=background_filename, folder='start'),
                                              (width, height))
    screen.blit(background_image, (0, 0, width, height))
    title_size, title_color, title_text = 35, (1, 35, 107), 'Slaughter of slimes'
    title_font = pygame.font.SysFont("comicsans", title_size, bold=True)
    title = title_font.render(title_text, True, title_color)
    start_title_x, start_title_y = width // 2 - 250, 140
    bank_w, bank_h = 580, 350
    bank_im = pygame.transform.scale(load_image(name="bank2.jpg", folder='start'), (bank_w, bank_h))
    screen.blit(bank_im, (start_title_x - 45, start_title_y - 30))
    screen.blit(title, (start_title_x, start_title_y))
    opened_file = open('data/start/start_text.txt', encoding='UTF-8', mode='r')
    text_lines = opened_file.readlines()
    opened_file.close()
    text_size = 20
    text_color = (1, 35, 107)
    font = pygame.font.SysFont("comicsans", text_size)
    margin_y = 30
    start_x, start_y = start_title_x, start_title_y + 25 + margin_y
    for index in range(len(text_lines)):
        text = font.render(text_lines[index].strip(), True, text_color)
        screen.blit(text, (start_x, start_y))
        start_y += margin_y
    choose_button = Button(screen, start_x + 10, start_y + margin_y, border=(1, 35, 107), text="Choose level",
                           color_t=(1, 35, 107), t_family='comicsans')
    choose_button.draw()
    running = True
    """
    chosen_track = "music/"
    pygame.mixer.music.load(chosen_track)
    pygame.mixer.music.play(-1)
    """
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cur_x, cur_y = event.pos
                if choose_button.get_click(cur_x, cur_y):
                    pygame.quit()
                    level_panel.show_level_panel()
        pygame.display.flip()


if __name__ == "__main__":
    show_start_screen()
