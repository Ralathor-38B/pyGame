import sqlite3
from random import choice, randint

import pygame

import character as char
import foes
import level_panel as panel
import level_results as res
import start_screen as start_sc
from alphabet_to_keys import eng_alf
from fon import Background, HPSymbol
import final_screen as f_sc


# import sys


def level(n):
    n -= 1
    regiment = 17 + 10 * (n % 3) + 5 * (n % 5)  # amount of enemies
    l_bound, u_bound = 7 - n // 5, 22 - 2 * (n % 3)
    speed = 10 + n // 3
    return regiment, l_bound, u_bound, speed


def draw_hps(hp_sprites_list, main_sprites, quantity):
    for hp_sprite in hp_sprites_list:
        hp_sprite.kill()
    hp_sprites_list = []
    start_x, start_y = 20, 20
    hp_margin = 15
    for i in range(quantity):
        current_hp = HPSymbol(main_sprites, x=start_x, y=start_y)
        start_x += HPSymbol.width + hp_margin
        hp_sprites_list.append(current_hp)
    return hp_sprites_list, main_sprites


def play(regiment, l_bound, u_bound, speed, cur_level_number):
    pygame.init()
    pygame.display.set_caption(f"Level {cur_level_number}")
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
    count = randint(l_bound, u_bound)  # через сколько смен экрана появится новый враг
    foes.FOES_SPEED = speed
    lives = 3
    start_lives = lives
    score_for_enemy, score_for_victory = 20, 200
    size = 1200, 650
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    directory_music = "music"
    music_achieve = ["example.wav", "battle_for_eternity.wav", "epic_war_is_fight.wav", "gloryham.wav", "hootsforce.wav"
                     "legendary_enchanted_jetpack.wav", "masters_of_the_galaxy.wav", "power_of_dragon_fire.wav",
                     "quest_for_the_hammer.wav", "ser_proletius_returns.wav", "the_king_of_california.wav",
                     "the_land_of_unicorns.wav"]
    chosen_track = f"{directory_music}/{choice(music_achieve)}"

    # region background initialise
    n = choice([1, 2, 3])
    if n == 1:
        folder = 'backgrounds/mountains/'
        Background(all_sprites, f'{folder}sky_out.png', 'fixed', one_more=False)
        Background(all_sprites, f'{folder}cloud1.png', 'slow')
        Background(all_sprites, f'{folder}clouds2.png', 'middle')
        Background(all_sprites, f'{folder}rocks1.png', 'slow')
        Background(all_sprites, f'{folder}rocks2.png', 'middle')
        Background(all_sprites, f'{folder}clouds4.png', 'fast')
    elif n == 2:
        folder = 'backgrounds/waterfall/'
        Background(all_sprites, f'{folder}_sky.png', 'fixed', one_more=False)
        Background(all_sprites, f'{folder}_clouds_1.png', 'slow')
        Background(all_sprites, f'{folder}_rocks.png', 'slow')
        Background(all_sprites, f'{folder}_ground.png', 'middle')
        Background(all_sprites, f'{folder}_clouds_2.png', 'middle')
    elif n == 3:
        folder = 'backgrounds/forest/'
        Background(all_sprites, f'{folder}7.png', 'fixed', one_more=False)
        Background(all_sprites, f'{folder}_6.png', 'slow')
        Background(all_sprites, f'{folder}_5.png', 'slow')
        Background(all_sprites, f'{folder}_4.png', 'middle')
        Background(all_sprites, f'{folder}cloud1.png', 'slow')
        Background(all_sprites, f'{folder}_3.png', 'middle')
        Background(all_sprites, f'{folder}_2.png', 'middle')
        Background(all_sprites, f'{folder}_1.png', 'middle')
        Background(all_sprites, f'{folder}_clouds_2.png', 'fast')

    start_x, start_y = 20, 20
    hp_margin = 15
    for i in range(lives):
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

    # pygame.mixer.music.load(chosen_track)
    # pygame.mixer.music.play(-1)

    fight = False
    magic = False
    end = 'not end'

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             pygame.key.get_pressed()[pygame.K_ESCAPE]):
                running = False
                break
                f_sc.show_final_screen()
            if event.type == pygame.KEYDOWN:
                fight = True
                foe = list(enemies)[number]
                x = foes_coords[number]
                if x > 200:
                    missile1.rect.x = x + 80
                    missile2.rect.x = x + 65
                    if pygame.key.get_pressed()[symbols[foe.symb]]:
                        foe.die()
                        number += 1
                        if number == regiment:
                            count = 15
                            end = True
                    else:
                        foe.hurt()
        all_sprites.update()
        hp_sprites, all_sprites = draw_hps(hp_sprites, all_sprites, lives)
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
            if foes_coords[i] <= 200 and i == number:
                lives -= 1
                number += 1
                if lives == 0:
                    character_go.die()
                    end = False
                    count = 15
                elif lives > 0:
                    character_go.hurt()
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
            count = randint(l_bound, u_bound)
            if len(e) < regiment:
                kind = choice(list(foes.reds.keys()))
                foes.Enemies(screen, enemies, kind, foes.reds[kind], 1, 1300, 370,
                             choice(list(symbols.keys())))
                foes_coords.append(1300)
            if end != 'not end':
                pygame.quit()
                res.show_level_results(cur_level_number, (number - start_lives + lives) * score_for_enemy,
                                       number - start_lives + lives, victory=end, current_lives=lives)
                running = False


if __name__ == '__main__':
    start_sc.show_start_screen()
    con = sqlite3.connect('levels_settings')
    cur = con.cursor()
    level_for_launch = cur.execute('''SELECT id FROM levels_score WHERE current = 1''').fetchone()
    panel.show_level_panel()
    reg, a, b, s = level(level_for_launch[0])
    # play(reg, a, b, s, level_for_launch[0])
