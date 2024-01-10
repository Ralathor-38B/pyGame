import pygame

from fon import Background
from function_load_image import load_image

DAMAGE = {'wizard': [4, 4]}  # папка персонажа: кол-во фреймов в его смерти, повреждении


class Heroes(pygame.sprite.Sprite):
    GENERAL_FOLDER_FOR_HEROES = 'hero'

    def __init__(self, in_type, folder, name, columns, rows, x, y, plus=0, q_reversed=False):
        super().__init__(in_type)
        self.frames = []
        self.general_folder = f'{self.GENERAL_FOLDER_FOR_HEROES}/{folder}'
        self.sheet = load_image(folder=self.general_folder, name=name, colorkey=-1)
        self.folder = folder
        self.col = columns
        self.cut_sheet(self.sheet, columns, rows)
        self.cur_frame = 0
        if q_reversed:
            self.cur_frame = columns - 1
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(x, y)
        self.plus = plus
        self.reversed = reversed
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
        if not self.alive and self.cur_frame == DAMAGE[self.folder][0] - 1:
            self.rect.x = -357
        if self.injured and self.cur_frame == DAMAGE[self.folder][1] - 1:
            x, y = self.rect.x, self.rect.y
            self.frames.clear()
            self.cut_sheet(self.sheet, self.col, 1)
            self.rect = self.rect.move(x, y)
            self.injured = False
        if self.reversed:
            self.cur_frame = (self.cur_frame - 1) % len(self.frames)
        else:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x += self.plus

    def hurt(self):
        x, y = self.rect.x, self.rect.y
        self.frames.clear()
        self.cut_sheet(load_image(folder=self.general_folder, name='Hurt_out.png', colorkey=-1), DAMAGE[self.folder][1],
                       1)
        self.rect = self.rect.move(x, y)
        self.cur_frame = 0
        self.injured = True

    def die(self):
        x, y = self.rect.x, self.rect.y
        self.frames.clear()
        self.cut_sheet(load_image(folder=self.general_folder, name='Dead_out.png', colorkey=-1), DAMAGE[self.folder][0],
                       1)
        self.rect = self.rect.move(x, y)
        self.cur_frame = 0
        self.alive = False


if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    go = pygame.sprite.Group()
    struggle = pygame.sprite.Group()
    charges = pygame.sprite.Group()
    character_go = Heroes(go, 'wizard', "Walk_out.png", 7, 1, 100, 360)
    character_struggle = Heroes(struggle, 'wizard', "Attack_1_out.png", 7,
                                1, 100, 500)
    missile1 = Heroes(charges, 'wizard', "lightning_1.png", 3,
                      1, 300, 200, plus=0)
    missile3 = Heroes(charges, 'wizard', "lightning_3.png", 4,
                      1, 285, 430, plus=0)
    running = True
    size = width, height = 1200, 650
    screen = pygame.display.set_mode(size)
    sky = Background(all_sprites, 'sky_out.png', 'fixed', one_more=False)
    cloud1 = Background(all_sprites, 'cloud1.png', 'slow')
    cloud2 = Background(all_sprites, 'clouds2.png', 'middle')
    cloud3 = Background(all_sprites, 'clouds3.png', 'slow')
    rock1 = Background(all_sprites, 'rocks1.png', 'slow')
    rock2 = Background(all_sprites, 'rocks2.png', 'middle')
    cloud41 = Background(all_sprites, 'clouds4.png', 'fast')
    all_sprites.draw(screen)
    pygame.display.flip()
    fps = 30
    clock = pygame.time.Clock()
    fight = False
    magic = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             pygame.key.get_pressed()[pygame.K_ESCAPE]):
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_d]:
                    character_go.die()
                if pygame.key.get_pressed()[pygame.K_h]:
                    character_go.hurt()
                if pygame.key.get_pressed()[pygame.K_a]:
                    magic = True
        all_sprites.update()
        all_sprites.draw(screen)
        if not fight:
            go.draw(screen)
            go.update()
        else:
            struggle.draw(screen)
            struggle.update()
            if character_struggle.cur_frame == 0:
                fight = False
            elif character_struggle.cur_frame == 3:
                magic = True
        if magic:
            charges.draw(screen)
            charges.update()
            if missile3.cur_frame == 0:
                magic = False
        pygame.display.flip()
        clock.tick(fps)
