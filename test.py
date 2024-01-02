from func_load_image import load_image
import pygame

pygame.init()


# region Background static objects
class Castle(pygame.sprite.Sprite):
    image = load_image("cas2.png", -1)
    width = 500
    height = 450

    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(Castle.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = height - self.height

    def update_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Ground:
    def __init__(self):
        self.width = width
        self.height = 40
        self.x = 0
        self.y = height - self.height

    def update_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self, sc):
        pygame.draw.rect(sc, "green", (self.x, self.y, self.width, self.height))


class HPSymbol(pygame.sprite.Sprite):
    image = load_image("hp_heart.png")
    width = 20
    height = 20

    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(HPSymbol.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Roll(pygame.sprite.Sprite):
    image = load_image("svitok.png", -1)
    width = 500
    height = 200

    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(Roll.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, *args, **kwargs) -> None:
        brown = (61, 26, 2)
        header_shift_x, header_shift_y = 75, 35
        shift_x, shift_y = header_shift_x, header_shift_y + 30
        standard_margin = 20
        standard_string_capacity = 47
        header_font = pygame.font.SysFont('arial', 30)
        standard_font = pygame.font.SysFont('arial', 20)
        header_info = "Уровень #1"
        prepared_info = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt 
        ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ul"""
        for i in range(0, len(prepared_info) - standard_string_capacity, standard_string_capacity):
            standard_info = prepared_info[i:i + standard_string_capacity]
            standard_text = standard_font.render(standard_info, True, brown)
            self.image.blit(standard_text, (self.rect.x + shift_x, self.rect.y +
                                            shift_y + standard_margin * (i // standard_string_capacity)))
        header_text = header_font.render(header_info, True, brown)
        self.image.blit(header_text, (self.rect.x + header_shift_x, self.rect.y + header_shift_y))
        hp_x, hp_y = shift_x, shift_y + (len(prepared_info) // 47) * standard_margin
        hp_margin = standard_margin
        for i in range(3):
            hp_symbol = HPSymbol(all_sprites)
            hp_symbol.update_pos(hp_x, hp_y)
            hp_x += hp_margin


class Balloon(pygame.sprite.Sprite):
    image = load_image('balloon.png', -1)
    width = 250
    height = 220

    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(Balloon.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 + width // 4 - self.width // 2
        self.rect.y = height // 2 - self.height

    def update(self, *args, **kwargs) -> None:
        pygame.draw.circle(self.image, "brown",
                           (self.width // 2, self.height // 2 - self.height // 8), 43)
        pygame.draw.circle(self.image, "white",
                           (self.width // 2, self.height // 2 - self.height // 8), 40)
        standard_font = pygame.font.SysFont("ComicSans", 50)
        current_letter = "A"
        current_text = standard_font.render(current_letter, True, "brown")
        self.image.blit(current_text, (self.width // 2 - self.width // 16, self.height // 2 -
                                       int((self.height // 8) * 2.5)))

    def update_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y
# endregion


def draw_background(sc):
    pygame.display.set_caption("Example")
    screen.fill("light blue")
    ground.draw(sc)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()


# region Launch of background canvas
all_sprites = pygame.sprite.Group()
running = True
size = width, height = 900, 600
screen = pygame.display.set_mode(size)
Castle(all_sprites)
Roll(all_sprites)
Balloon(all_sprites)
ground = Ground()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_background(screen)
# endregion
