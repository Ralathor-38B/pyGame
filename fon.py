import pygame
import os
import sys


class Background(pygame.sprite.Sprite):
    def __init__(self, group, file_name, type: str, x=0, one_more=True):
        super().__init__(group, group)
        self.image = load_image(file_name)
        self.rect = self.image.get_rect().move(x, 0)
        self.type = type  # type of move i.e. with which speed sprite will get going
        # (e.g. fixed, slow, middle, fast)
        if one_more:
            Background(group, file_name, type, x=self.rect.width, one_more=False)

    def update(self):
        match self.type:
            case 'fixed':
                pass
            case 'slow':
                self.rect.x -= 1
            case 'middle':
                self.rect.x -= 2
            case 'fast':
                self.rect.x -= 4
        if self.rect.x <= -self.rect.width:
            self.rect.x = self.rect.width


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


class HPSymbol(pygame.sprite.Sprite):
    image = load_image("hp_heart.png")
    width = 20
    height = 20

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = pygame.transform.scale(HPSymbol.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, type, sheet, columns, rows, x, y):
        super().__init__(type)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    fly = pygame.sprite.Group()
    flame = pygame.sprite.Group()
    running = True
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    Background(all_sprites, 'sky_out.png', 'fixed', one_more=False)
    Background(all_sprites, 'cloud1.png', 'slow')
    Background(all_sprites, 'clouds2.png', 'middle')
    Background(all_sprites, 'rocks1.png', 'slow')
    Background(all_sprites, 'rocks2.png', 'middle')
    Background(all_sprites, 'clouds4.png', 'fast')
    for i in range(3):
        HPSymbol(all_sprites, 30 + i * 20, 50)
    all_sprites.draw(screen)
    pygame.display.flip()
    fps = 20
    clock = pygame.time.Clock()
    flag = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                flag = bool(abs(flag - 1))
        if flag:
            all_sprites.update()
            all_sprites.draw(screen)
            pygame.display.flip()
        clock.tick(fps)
