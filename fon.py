from function_load_image import load_image
import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, group, file_name, state_type: str, x=0, y=0, one_more=True):
        super().__init__(group, group)
        self.image = load_image(file_name)
        self.rect = self.image.get_rect().move(x, y)
        self.state_type = state_type
        if one_more:
            Background(group, file_name, state_type, x=self.rect.width, y=y, one_more=False)

    def set_position(self, x, y):
        self.rect = self.rect.move(x, y)

    def set_size(self, cur_width, cur_height):
        self.image = pygame.transform.scale(self.image, (cur_width, cur_height))
        self.rect = self.image.get_rect()

    def update(self):
        if self.state_type == 'fixed':
            pass
        elif self.state_type == 'slow':
            self.rect.x -= 1
        elif self.state_type == 'middle':
            self.rect.x -= 2
        elif self.state_type == 'fast':
            self.rect.x -= 4
        if self.rect.x <= -self.rect.width:
            self.rect.x = self.rect.width


class HPSymbol(pygame.sprite.Sprite):
    image = load_image("hp_heart.png")
    width = 40
    height = 40

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = pygame.transform.scale(HPSymbol.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, state_type, sheet, columns, rows, x, y):
        super().__init__(state_type)
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
    size = width, height = 1200, 650
    screen = pygame.display.set_mode(size)
    Background(all_sprites, 'sky_out.png', 'fixed', one_more=False)
    Background(all_sprites, 'cloud1.png', 'slow')
    Background(all_sprites, 'clouds2.png', 'middle')
    Background(all_sprites, 'clouds4.png', 'fast')
    Background(all_sprites, 'rocks1.png', 'slow')
    Background(all_sprites, 'rocks2.png', 'middle')
    fps = 20
    clock = pygame.time.Clock()
    running = True
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
