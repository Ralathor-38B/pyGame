from random import choice, randint
from alphabet_to_keys import eng_alf
from fon import Background, HPSymbol
from function_load_image import load_image
from button import Button
import character as char
import pygame
import foes


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
                        pygame.quit()
                        level_number = index + 1
                        start_level(level_number)
                        running = False
        pygame.display.flip()


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
    choose_button = Button(screen, start_x + 10, start_y + margin_y, border="white", text="Choose level",
                           color_t="white")
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
    background_images = {"win": 'fon3.jpg', "loose": "loose.jpg"}
    title_texts = {"win": "You are the winner!", "loose": "Sorry, but you lost!"}
    back_filename = background_images[key_state]
    note_filename = 'bank.png'
    size = width, height = 800, 480
    screen = pygame.display.set_mode(size)
    back_image = pygame.transform.scale(load_image(back_filename), (width, height))
    note_image = pygame.transform.scale(load_image(note_filename), (int(width * 0.6), int(height * 0.7)))
    start_note_x, start_note_y = int(width * 0.2), int(height * 0.15)
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
    button_back_to_start = Button(screen, button_x, button_y + int(margin_y * 1.8), 'brown',
                                  text="Back to the start page", color_t='brown', t_family='comicsans', size_t=20)
    button_restart_level = Button(screen, button_x, button_y, 'brown', text='Restart the level',
                                  color_t='brown', t_family='comicsans', size_t=20)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ev_x, ev_y = event.pos
                if button_back_to_start.get_click(ev_x, ev_y):
                    pygame.quit()
                    show_start_screen()
                elif button_restart_level.get_click(ev_x, ev_y):
                    pygame.quit()
                    start_level(level_number)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()


def start_level(number):
    reg, a, b, s = level(number)
    play(reg, a, b, s, number)


def level(n):
    n -= 1
    regiment = 30 + 10 * (n % 3) + 5 * (n % 5)  # amount of enemies
    a, b = 7 - n // 5, 22 - 2 * (n % 3)
    speed = 10 + n // 3  # foes speed
    return regiment, a, b, speed


def draw_hps():
    global hp_sprites, all_sprites, LIVES
    for hp_sprite in hp_sprites:
        hp_sprite.kill()
    hp_sprites = []
    start_x, start_y = 20, 20
    hp_margin = 15
    for i in range(LIVES):
        current_hp = HPSymbol(all_sprites, x=start_x, y=start_y)
        start_x += HPSymbol.width + hp_margin
        hp_sprites.append(current_hp)


def play(regiment, a, b, speed, cur_level_number):
    global hp_sprites, all_sprites, LIVES
    pygame.init()
    pygame.display.set_caption("Game")
    # start_screen()
    running = True
    hp_sprites = []
    all_sprites = pygame.sprite.Group()
    go = pygame.sprite.Group()
    struggle = pygame.sprite.Group()
    charges = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    character_go = char.Heroes(go, 'wizard', "Walk_out.png", 7, 1, 100, 370)
    character_struggle = char.Heroes(struggle, 'wizard', "Attack_1_out.png", 7,
                                     1, 100, 370)
    missile1 = char.Heroes(charges, 'wizard', "lightning_1.png", 3,
                           1, 300, 200, plus=0)
    missile2 = char.Heroes(charges, 'wizard', "lightning_3.png", 4,
                           1, 285, 430, plus=0)

    number = 0  # индекс текущего противника
    count = randint(a, b)  # через сколько смен экрана появится новый враг
    foes.FOES_SPEED = speed
    LIVES = 3
    START_LIVES = LIVES
    score_for_enemy, score_for_victory = 20, 200
    size = width, height = 1200, 650
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    # region background initialise
    Background(all_sprites, 'sky_out.png', 'fixed', one_more=False)
    Background(all_sprites, 'cloud1.png', 'slow')
    Background(all_sprites, 'clouds2.png', 'middle')
    Background(all_sprites, 'rocks1.png', 'slow')
    Background(all_sprites, 'rocks2.png', 'middle')
    Background(all_sprites, 'clouds4.png', 'fast')
    start_x, start_y = 20, 20
    hp_margin = 15
    for i in range(LIVES):
        current_hp = HPSymbol(all_sprites, x=start_x, y=start_y)
        start_x += HPSymbol.width + hp_margin
        hp_sprites.append(current_hp)
    # endregion

    kind = choice(list(foes.reds.keys()))
    symbols = eng_alf
    foes.Enemies(screen, enemies, kind, foes.reds[kind], 1, 1100, 370,
                 choice(list(symbols.keys())))
    foes_coords = [1100]

    all_sprites.draw(screen)
    pygame.display.flip()
    fps = 60
    clock = pygame.time.Clock()

    fight = False
    magic = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             pygame.key.get_pressed()[pygame.K_ESCAPE]):
                running = False
            if event.type == pygame.KEYDOWN:
                fight = True
                foe = list(enemies)[number]
                x = foes_coords[number]
                if x > 300:
                    missile1.rect.x = x + 80
                    missile2.rect.x = x + 65
                    if pygame.key.get_pressed()[symbols[foe.symb]]:
                        foe.die()
                        number += 1
                    else:
                        foe.hurt()
        all_sprites.update()
        draw_hps()
        all_sprites.draw(screen)
        if not fight:
            go.update()
            go.draw(screen)
        else:
            struggle.update()
            struggle.draw(screen)
            if character_struggle.cur_frame == 0:
                fight = False
            elif character_struggle.cur_frame == 3:
                magic = True
        enemies.update()
        enemies.draw(screen)
        e = list(enemies)
        for i in range(len(e)):
            e[i].print_letter((e[i].cur_frame - 1) % 10)  # 10 frames in file 'Run+Attack_out.png'
            foes_coords[i] -= foes.FOES_SPEED
            if pygame.sprite.collide_mask(character_go, e[i]) and i == number:
                LIVES -= 1
                if LIVES == 0:
                    character_go.die()
                    show_level_results(cur_level_number, (number + 1 - START_LIVES) * score_for_enemy,
                                       number + 1 - START_LIVES)
                    running = False
                    break
                elif LIVES > 0:
                    character_go.hurt()
                    number += 1
        if magic:
            charges.update()
            charges.draw(screen)
            if missile1.cur_frame == 0:
                magic = False
        pygame.display.flip()
        clock.tick(fps)

        if count:
            count -= 1
        else:
            count = randint(a, b)
            if number < regiment:
                kind = choice(list(foes.reds.keys()))
                foes.Enemies(screen, enemies, kind, foes.reds[kind], 1, 1300, 370,
                             choice(list(symbols.keys())))
                foes_coords.append(1300)


if __name__ == '__main__':
    level_for_launch = 1
    reg, a, b, s = level(level_for_launch)
    play(reg, a, b, s, level_for_launch)
