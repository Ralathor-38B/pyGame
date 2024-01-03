from func_load_image import load_image
import pygame


class HPSymbol(pygame.sprite.Sprite):
    image = load_image("hp_heart.png")
    width = 40
    height = 40

    def __init__(self, group):
        super().__init__(group, group)
        self.image = pygame.transform.scale(HPSymbol.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


class BackgroundObject(pygame.sprite.Sprite):
    speeds_x = {"fixed": 0, "slow": -1, "middle": -2, "fast": -4}
    border_margin = 10

    def __init__(self, group: pygame.sprite.Group, filename: str, type_of_state: str, to_full_screen: bool = False):
        super().__init__(group, group)
        self.image = load_image(filename)
        self.width, self.height = self.image.get_size()
        self.rect = self.image.get_rect()
        self.type_of_state = type_of_state
        self.rect.x = 0
        self.rect.y = 0
        self.filename = filename
        self.group = group
        self.to_full_screen = to_full_screen

    def convert_image(self):
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def set_position(self, x, y=0):
        self.rect.x = x
        self.rect.y = y

    def set_size(self, cur_width, cur_height):
        self.width = cur_width
        self.height = cur_height
        self.convert_image()

    def update(self):
        current_speed = self.speeds_x[self.type_of_state]
        self.rect.x += current_speed
        if self.rect.x <= -self.rect.width:
            self.rect.x = self.rect.width
        if self.to_full_screen and self.type_of_state == "fixed":
            for cur_x in range(self.rect.x, width + self.rect.width, self.width):
                the_same_object = BackgroundObject(self.group, self.filename, self.type_of_state)
                the_same_object.set_size(self.width, self.height)
                the_same_object.set_position(cur_x, self.rect.y)


def draw_background():
    pygame.display.set_caption("Игра")
    hp_x, hp_y = 20, 20
    for sprite in hp_sprites:
        sprite.kill()
    for i in range(LIVES):
        current_hp = HPSymbol(all_sprites)
        current_hp.update_pos(hp_x, hp_y)
        hp_sprites.append(current_hp)
        hp_x += HPSymbol.width
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    all_sprites = pygame.sprite.Group()
    running = True
    LIVES = 3
    hp_sprites = []
    size = width, height = 1200, 650
    screen = pygame.display.set_mode(size)
    BackgroundObject(all_sprites, 'sky_out.png', 'fixed')
    BackgroundObject(all_sprites, 'cloud1.png', 'slow')
    BackgroundObject(all_sprites, 'clouds2.png', 'middle')
    BackgroundObject(all_sprites, 'clouds4.png', 'fast')
    first_rock = BackgroundObject(all_sprites, 'rocks1.png', 'slow')
    second_rock = BackgroundObject(all_sprites, 'rocks2.png', 'middle')
    first_rock_w, first_rock_h = 1300, 500
    second_rock_w, second_rock_h = 1300, 400
    first_rock_x, first_rock_y = width - first_rock_w, height - first_rock_h
    second_rock_x, second_rock_y = width - second_rock_w, height - second_rock_h
    first_rock.set_size(first_rock_w, first_rock_h)
    second_rock.set_size(second_rock_w, second_rock_h)
    first_rock.set_position(first_rock_x, first_rock_y)
    second_rock.set_position(second_rock_x, second_rock_y)
    fps = 70
    clock = pygame.time.Clock()
    flag = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    LIVES += 1
                elif event.key == pygame.K_b:
                    LIVES -= 1
        draw_background()
        clock.tick(fps)
