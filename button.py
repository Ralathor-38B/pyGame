from function_load_image import load_image
import pygame


class Button:
    def __init__(self, sc, x, y, border=None, text=None, size_t=20, color_t='white', image=None, t_family="segoeui"):
        self.sc = sc
        self.border = border
        self.text, self.size, self.color = text, size_t, color_t
        self.image = image
        self.text_family = t_family
        self.left, self.top = x, y
        self.right, self.down = self.draw()

    def get_click(self, x, y):
        if self.left <= x <= self.right and self.top <= y <= self.down:
            return True

    def draw(self):
        rect = pygame.Rect((0, 0), (1, 1))
        if self.image:
            img = load_image(self.image)
            rect = img.get_rect()
            rect.y = self.top
            rect.x = self.left
            self.sc.blit(img, rect)
        if self.text:
            font = pygame.font.SysFont(self.text_family, self.size)
            text = font.render(self.text, True, self.color)
            rect = text.get_rect()
            rect.y = self.top
            rect.x = self.left
            self.sc.blit(text, rect)
        if self.border:
            pygame.draw.rect(self.sc, self.border, ((self.left - 10, self.top - 10),
                                                    (rect.width + 20, rect.height + 20)), 2)
        return rect.right + 20, rect.bottom + 20

    def set_text_family(self, new_text_family):
        self.text_family = new_text_family


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((630, 600))

    b = Button(screen, 30, 30, 'yellow', image='hp_heart.png')
    t = Button(screen, 250, 250, 'blue', text='bivfaehgbiu')
    buttons = [b, t]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             pygame.key.get_pressed()[pygame.K_ESCAPE]):
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                cur_x, cur_y = event.pos
                for but in buttons:
                    clicked = but.get_click(cur_x, cur_y)
        screen.fill('blue')
        b.draw()
        t.draw()
        pygame.display.flip()
