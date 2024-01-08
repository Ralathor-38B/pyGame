from function_load_image import load_image
import pygame


def show_final_screen():
    pygame.init()
    pygame.display.set_caption("Final screen")
    back_im = load_image("back.jpg")
    size = width, height = back_im.get_size()
    screen = pygame.display.set_mode(size)
    screen.blit(back_im, (0, 0, width, height))
    b_w, b_h = 420, 240
    b_x, b_y = width // 2 - 215, height // 2 - 140
    bank_im = pygame.transform.scale(load_image("y_bank.jpg"), (b_w, b_h))
    screen.blit(bank_im, (b_x, b_y, b_x + b_w, b_y + b_h))
    final_text = ["  Thank you for your choice!", "We appreciate your support and feedback.",
                  "Our team is dedicated to improving your",
                  "experience. We hope that you will keep ", "track of further game updates.",
                  "", "Devs of 'Slaughter of slimes'"]
    title_x, title_y, title_size = b_x + 20, b_y + 20, 27
    title_color = (64, 35, 7)
    title_font = pygame.font.SysFont('comicsans', title_size)
    title_text = title_font.render(final_text[0], True, title_color)
    screen.blit(title_text, (title_x, title_y))
    font = pygame.font.SysFont('comicsans', title_size - 8)
    margin_y = 24
    cur_x, cur_y = title_x, title_y + int(margin_y * 2.1)
    for text_line in final_text[1:]:
        cur_text = font.render(text_line, True, title_color)
        screen.blit(cur_text, (cur_x, cur_y))
        cur_y += margin_y
    running = True
    tick_time = 15000
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break
                pygame.quit()
        pygame.display.flip()
        if pygame.time.get_ticks() > tick_time:
            break
            # pygame.quit()


if __name__ == "__main__":
    show_final_screen()
