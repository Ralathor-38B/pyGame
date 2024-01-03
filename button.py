import pygame

import game


class Button:
    def __init__(self, sc, x, y, border=None, text=None, size_t=20, color_t='white', image=None):
        self.sc = sc
        self.border = border
        self.text, self.size, self.color = text, size_t, color_t
        self.image = image

        self.left, self.top = x, y
        self.right, self.down = self.draw()

    def get_click(self, x, y):
        if self.left <= x <= self.right and self.top <= y <= self.down:
            return True

    def draw(self):
        if self.image:
            img = game.load_image(self.image)
            rect = img.get_rect()
            rect.y = self.top
            rect.x = self.left
            self.sc.blit(img, rect)
        if self.text:
            font = pygame.font.SysFont('segoeui', self.size)
            text = font.render(self.text, True, self.color)
            rect = text.get_rect()
            rect.y = self.top
            rect.x = self.left
            self.sc.blit(text, rect)
        if self.border:
            pygame.draw.rect(self.sc, self.border, ((self.left - 10, self.top - 10),
                                                (rect.width + 20, rect.height + 20)), 2)
        return rect.right + 20, rect.bottom + 20


if __name__ == '__main__':
    pygame.init()
    sc = pygame.display.set_mode((630, 600))

    b = Button(sc, 30, 30, 'yellow', image='hp_heart.png')
    t = Button(sc, 250, 250, 'blue', text='bivfaehgbiu')
    buttons = [b, t]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             pygame.key.get_pressed()[pygame.K_ESCAPE]):
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for but in buttons:
                    clicked = but.get_click(x, y)
        sc.fill('blue')
        b.draw()
        t.draw()
        pygame.display.flip()