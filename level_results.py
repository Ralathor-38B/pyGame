from function_load_image import load_image
from button import Button
from fon import HPSymbol
import start_screen
import game
import pygame


def show_level_results(level_number, score, killed_enemies, victory=False, current_lives=0):
    pygame.init()
    pygame.display.set_caption("Final screen")
    all_sprites = pygame.sprite.Group()
    lives = current_lives
    key_state = "win" if victory else "loose"
    background_images = {"win": 'fon3.jpg', "loose":  "loose.jpg"}
    title_texts = {"win": "You are the winner!", "loose": "Sorry, but you lost!"}
    back_filename = background_images[key_state]
    note_filename = 'bank.png'
    size = width, height = 800, 480
    screen = pygame.display.set_mode(size)
    back_image = pygame.transform.scale(load_image(back_filename), (width, height))
    note_image = pygame.transform.scale(load_image(note_filename), (int(width * 0.6), int(height * 0.7)))
    start_note_x, start_note_y = int(width * 0.2), int(height * 0.15)
    note_rect = (start_note_x, start_note_y, int(width * 0.6) + start_note_x, int(height * 0.7) + start_note_y)
    im_rect = (0, 0, width, height)
    screen = pygame.display.set_mode(size)
    screen.blit(back_image, im_rect)
    screen.blit(note_image, note_rect)
    title_size = 28
    title_length = 36
    title_text = title_texts[key_state]
    title_color = "brown"
    title_x, title_y = start_note_x + 50, start_note_y + 30
    font = pygame.font.SysFont('comicsans', title_size)
    text = font.render(title_text.center(title_length), True, title_color)
    screen.blit(text, (title_x, title_y))
    text_lines = [f"Level №: {level_number}", "HP:", f"Score: {score}",
                  f"Quantity of defeated enemies: {killed_enemies}"]
    text_size = 20
    text_color = "brown"
    cur_x, cur_y = title_x, title_y + 50
    margin_y = 30
    for index in range(len(text_lines)):
        font = pygame.font.SysFont('comicsans', text_size)
        text = font.render(text_lines[index], True, text_color)
        screen.blit(text, (cur_x, cur_y))
        cur_y += margin_y
    coord_x, coord_y = title_x + 40, title_y + 53 + margin_y
    for i in range(lives):
        cur_hp = HPSymbol(all_sprites, x=coord_x, y=coord_y)
        cur_hp.set_size(27, 27)
        coord_x += cur_hp.width
    button_x, button_y = cur_x + 10, cur_y + margin_y // 2
    button_back_to_start = Button(screen, button_x, button_y + int(margin_y * 1.8), 'brown',
                                  text="Back to the start page", color_t='brown', t_family='comicsans', size_t=20)

    button_restart_level = Button(screen, button_x, button_y, 'brown', text='Restart the level',
                                  color_t='brown', t_family='comicsans', size_t=20)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ev_x, ev_y = event.pos
                if button_back_to_start.get_click(ev_x, ev_y):
                    pygame.quit()
                    start_screen.show_start_screen()
                if button_restart_level.get_click(ev_x, ev_y):
                    pygame.quit()
                    game.start_level(level_number)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    show_level_results(1, 2024, 44)
