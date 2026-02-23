import pygame
import random
import sys
import time

speed = 20
x = 500
y = 500

pygame.init()

pygame.display.set_caption('Sho_vidbulosya')
game_window = pygame.display.set_mode((x, y))

night = pygame.Color(15, 0, 20)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

fps_controller = pygame.time.Clock()

s_pos = [100, 50]
s_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

food_pos = [random.randrange(1, (x // 10)) * 10, random.randrange(1, (y // 10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


def dead():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('lol, u dead', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (x / 2, y / 4)
    game_window.fill(night)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (x / 10, 15)
    else:
        score_rect.midtop = (x / 2, y / 1.25)
    game_window.blit(score_surface, score_rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'

            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        s_pos[1] -= 10
    if direction == 'DOWN':
        s_pos[1] += 10
    if direction == 'LEFT':
        s_pos[0] -= 10
    if direction == 'RIGHT':
        s_pos[0] += 10

    s_body.insert(0, list(s_pos))
    if s_pos[0] == food_pos[0] and s_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        s_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (x // 10)) * 10, random.randrange(1, (y // 10)) * 10]
    food_spawn = True

    game_window.fill(night)
    for pos in s_body:
        pygame.draw.rect(game_window, white, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, green, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    if s_pos[0] < 0 or s_pos[0] > x - 10:
        dead()
    if s_pos[1] < 0 or s_pos[1] > y - 10:
        dead()

    show_score(1, white, 'consoles', 20)

    pygame.display.update()

    fps_controller.tick(speed)