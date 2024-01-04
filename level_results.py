from function_load_image import load_image
from random import randint
from button import Button
from level_panel import show_level_panel
from fon import HPSymbol
import pygame
import sys


def start_screen():
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
    pygame.display.set_caption("Стартовая страница")
    size = width, height = 700, 500
    screen = pygame.display.set_mode(size)
    background_filename = "opened_door2.jpg"
    background_image = pygame.transform.scale(load_image(name=background_filename, folder='start'),
                                              (width, height))
    screen.blit(background_image, (0, 0, width, height))
    title_size, title_color, title_text = 45, 'white', 'Play more - type better'
    title_font = pygame.font.SysFont("segoeui", title_size, bold=True)
    title = title_font.render(title_text, True, title_color)
    start_title_x, start_title_y = 20, 20
    screen.blit(title, (start_title_x, start_title_y))
    opened_file = open('data/start/start_text.txt', encoding='UTF-8', mode='r')
    text_lines = opened_file.readlines()
    opened_file.close()
    text_size = 20
    text_color = "white"
    font = pygame.font.SysFont("segoeui", text_size)
    margin_y = 30
    start_x, start_y = start_title_x, start_title_y + 40 + margin_y
    for index in range(len(text_lines)):
        text = font.render(text_lines[index].strip(), True, text_color)
        screen.blit(text, (start_x, start_y))
        start_y += margin_y
    choose_button = Button(screen, start_x + 10, start_y + margin_y, border="white", text="Choose level", color_t="white")
    choose_button.draw()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cur_x, cur_y = event.pos
                if choose_button.get_click(cur_x, cur_y):
                    pygame.quit()
                    show_level_panel()
        pygame.display.flip()


def show_level_results(level_number, score, killed_enemies, victory=False, current_lives=0):
    pygame.init()
    pygame.display.set_caption("Final screen")
    all_sprites = pygame.sprite.Group()
    lives = current_lives
    key_state = "win" if victory else "loose"
    background_images = {"win": 'fon3.jpg', "loose":  "loose.jpg"}
    title_texts = {"win": "You are the winner!", "loose": "Sorry, but you lost!"}
    back_filename = background_images[key_state]
    note_filename = 'bank.png'
    size = width, height = 800, 480
    screen = pygame.display.set_mode(size)
    back_image = pygame.transform.scale(load_image(back_filename), (width, height))
    note_image = pygame.transform.scale(load_image(note_filename), (int(width * 0.6), int(height * 0.6)))
    start_note_x, start_note_y = int(width * 0.2), int(height * 0.2)
    note_rect = (start_note_x, start_note_y, int(width * 0.6) + start_note_x, int(height * 0.7) + start_note_y)
    im_rect = (0, 0, width, height)
    screen = pygame.display.set_mode(size)
    screen.blit(back_image, im_rect)
    screen.blit(note_image, note_rect)
    title_size = 28
    title_length = 36
    title_text = title_texts[key_state]
    title_color = "brown"
    title_x, title_y = start_note_x + 50, start_note_y + 30
    font = pygame.font.SysFont('comicsans', title_size)
    text = font.render(title_text.center(title_length), True, title_color)
    screen.blit(text, (title_x, title_y))
    text_lines = [f"Level №: {level_number}", "HP:", f"Score: {score}",
                  f"Quantity of defeated enemies: {killed_enemies}"]
    text_size = 20
    text_color = "brown"
    cur_x, cur_y = title_x, title_y + 50
    margin_y = 30
    for index in range(len(text_lines)):
        font = pygame.font.SysFont('comicsans', text_size)
        text = font.render(text_lines[index], True, text_color)
        screen.blit(text, (cur_x, cur_y))
        cur_y += margin_y
    coord_x, coord_y = title_x + 40, title_y + 53 + margin_y
    for i in range(lives):
        cur_hp = HPSymbol(all_sprites, x=coord_x, y=coord_y)
        cur_hp.set_size(27, 27)
        coord_x += cur_hp.width
    button_x, button_y = cur_x + 10, cur_y + margin_y // 2
    button_back_to_start = Button(screen, button_x, button_y, 'brown',
                                  text="Back to the start page", color_t='brown', t_family='comicsans', size_t=20)
    """
    + int(margin_y * 1.8)
    button_restart_level = Button(screen, button_x, button_y, 'brown', text='Restart the level',
                                  color_t='brown', t_family='comicsans', size_t=20)
    """
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ev_x, ev_y = event.pos
                if button_back_to_start.get_click(ev_x, ev_y):
                    start_screen()
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    # show_level_results(1, 2024, 44)
    show_start_screen()
