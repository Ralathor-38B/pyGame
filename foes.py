import os
import sys
# from random import choice

import pygame

from fon import Background, HPSymbol

FOES_SPEED = 10
eng_alf = {"A": pygame.K_a,
           "B": pygame.K_b,
           "C": pygame.K_c,
           "D": pygame.K_d,
           "E": pygame.K_e,
           "F": pygame.K_f,
           "G": pygame.K_g,
           "H": pygame.K_h,
           "I": pygame.K_i,
           "J": pygame.K_j,
           "K": pygame.K_k,
           "L": pygame.K_l,
           "M": pygame.K_m,
           "N": pygame.K_n,
           "O": pygame.K_o,
           "P": pygame.K_p,
           "Q": pygame.K_q,
           "R": pygame.K_r,
           "S": pygame.K_s,
           "T": pygame.K_t,
           "U": pygame.K_u,
           "V": pygame.K_v,
           "W": pygame.K_w,
           "X": pygame.K_x,
           "Y": pygame.K_y,
           "Z": pygame.K_z
           }
reds = {'Attack.png': 13, 'Run_out.png': 7, 'Walk_out.png': 8, 'Run+Attack_out.png': 10}


def load_image(name, colorkey=None):
    fullname = os.path.join('data/foes', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Enemies(pygame.sprite.Sprite):
    def __init__(self, canvas, type, name, columns, rows, x, y, symb='A'):
        super().__init__(type)
        self.frames = []
        self.sheet = load_image(name, -1)
        self.cut_sheet(self.sheet, columns, rows)
        self.cur_frame = columns - 1
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        # self.columns, self.rows = columns, rows
        self.rect = self.rect.move(x, y)
        self.symb = symb
        self.sc = canvas
        self.type = name
        self.injured = False
        self.alive = True

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if not self.alive and self.cur_frame == 0:
            self.rect.x = -357
        if self.injured and self.cur_frame == 0:
            x, y = self.rect.x, self.rect.y
            self.frames.clear()
            self.cut_sheet(self.sheet, reds[self.type], 1)
            self.rect = self.rect.move(x, y)
            self.injured = False
        self.cur_frame = (self.cur_frame - 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)

    def print_letter(self, frame):
        font = pygame.font.SysFont('comicsansms', 25)
        text = font.render(self.symb, True, 'blue')
        match self.type:
            case 'Attack.png' | 'Run_out.png':
                self.sc.blit(text, (self.rect.x + 135, self.rect.bottom - 45))
            case 'Walk_out.png':
                self.sc.blit(text, (self.rect.x + 127, self.rect.bottom - 37))
            # case 'Jump_out.png':
            #     self.sc.blit(text, (self.rect.x + 127, self.rect.bottom - 37))
            case 'Run+Attack_out.png':
                match frame:
                    case 0:
                        self.sc.blit(text, (self.rect.x + 135, self.rect.bottom - 65))
                    case 9:
                        self.sc.blit(text, (self.rect.x + 127, self.rect.bottom - 55))
                    case 8:
                        self.sc.blit(text, (self.rect.x + 140, self.rect.bottom - 45))
                    case 7 | 6:
                        self.sc.blit(text, (self.rect.x + 150, self.rect.bottom - 45))
                    case 5:
                        self.sc.blit(text, (self.rect.x + 137, self.rect.bottom - 47))
                    case 4:
                        self.sc.blit(text, (self.rect.x + 145, self.rect.bottom - 65))
                    case 1 | 2 | 3:
                        self.sc.blit(text, (self.rect.x + 145, self.rect.bottom - 80))
        self.rect.x -= FOES_SPEED

    def hurt(self):
        x, y = self.rect.x, self.rect.y
        self.frames.clear()
        self.cut_sheet(load_image('Hurt_out.png', -1), 6, 1)
        self.rect = self.rect.move(x, y)
        self.cur_frame = 5
        self.injured = True

    def die(self):
        x, y = self.rect.x, self.rect.y
        self.frames.clear()
        self.cut_sheet(load_image('Dead_out.png', -1), 3, 1)
        self.rect = self.rect.move(x, y)
        self.cur_frame = 2
        self.alive = False


if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    slimes = pygame.sprite.Group()
    s = Enemies(screen, slimes, 'Run+Attack_out.png', 10, 1, 900, 600, 'E')
    running = True
    sky = Background(all_sprites, 'sky_out.png', 'fixed', one_more=False)
    cloud1 = Background(all_sprites, 'cloud1.png', 'slow')
    cloud2 = Background(all_sprites, 'clouds2.png', 'middle')
    cloud3 = Background(all_sprites, 'clouds3.png', 'slow')
    rock1 = Background(all_sprites, 'rocks1.png', 'slow')
    rock2 = Background(all_sprites, 'rocks2.png', 'middle')
    cloud4 = Background(all_sprites, 'clouds4.png', 'fast')
    for i in range(3):
        HPSymbol(all_sprites, 30 + i * 20, 30)
    all_sprites.draw(screen)
    pygame.display.flip()
    fps = 60
    clock = pygame.time.Clock()
    flag = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             pygame.key.get_pressed()[pygame.K_ESCAPE]):
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_d]:
                    s.die()
                if pygame.key.get_pressed()[pygame.K_h]:
                    s.hurt()

        all_sprites.update()
        all_sprites.draw(screen)
        if not flag:
            for foe in slimes:
                foe.die()
            flag = True
        slimes.draw(screen)
        slimes.update()
        for foe in slimes:
            foe.print_letter(foe.cur_frame)
        pygame.display.flip()
        clock.tick(fps)