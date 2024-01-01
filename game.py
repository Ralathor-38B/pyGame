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


def amount(num, n):
    if num < n:
        kind = choice(list(foes.reds.keys()))
        foes.Enemies(screen, enemies, kind, foes.reds[kind], 1, 1300, 600,
                            choice(list(foes.eng_alf.keys())))
        foes_coords.append(1300)
        return randint(7, 20)


if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    go = pygame.sprite.Group()
    struggle = pygame.sprite.Group()
    charges = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    character_go = char.Heroes(go, 'wizard', "Walk_out.png", 7, 1, 100, 600)
    character_struggle = char.Heroes(struggle, 'wizard', "Attack_1_out.png", 7,
                                1, 100, 600)
    missile1 = char.Heroes(charges, 'wizard', "lightning_1.png", 3,
                      1, 300, 200, plus=0)
    missile2 = char.Heroes(charges, 'wizard', "lightning_3.png", 4,
                      1, 285, 730, plus=0)

    running = True
    number = 0  # индекс текущего противника
    count = randint(7, 20)  # через сколько смен экрана появится новый враг
    REGIMENT = 30  # количество врагов в уровне
    LIVES = 3
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)

    # region background initialise
    Background(all_sprites, 'sky_out.png', 'fixed', one_more=False)
    Background(all_sprites, 'cloud1.png', 'slow')
    Background(all_sprites, 'clouds2.png', 'middle')
    Background(all_sprites, 'rocks1.png', 'slow')
    Background(all_sprites, 'rocks2.png', 'middle')
    Background(all_sprites, 'clouds4.png', 'fast')
    # endregion

    for i in range(3):
        HPSymbol(all_sprites, 30 + i * 20, 50)

    kind = choice(list(foes.reds.keys()))
    foes.Enemies(screen, enemies, kind, foes.reds[kind], 1, 1100, 600,
                            choice(list(foes.eng_alf.keys())))
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
                    if pygame.key.get_pressed()[foes.eng_alf[foe.symb]]:
                        foe.die()
                        number += 1
                    else:
                        foe.hurt()
        all_sprites.update()
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
            e[i].print_letter((e[i].cur_frame - 1) % 10)
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
            count = amount(number, REGIMENT)
