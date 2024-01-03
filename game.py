import os
import sys
from random import choice, randint

import pygame

import character as char
import foes
from fon import Background, HPSymbol


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


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

def play(regiment, a, b, speed):
    global hp_sprites, all_sprites, LIVES
    pygame.init()
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
    symbols = foes.eng_alf
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
    reg, a, b, s = level(1)
    play(reg, a, b, s)