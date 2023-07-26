import pygame
import button
import sys
import mysql.connector as c
from random import randint
from pygame import mixer

pygame.init()
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
WINDOW = pygame.display.set_mode((900, 500))
pygame.display.set_caption("Nox")

# icon
icon = pygame.image.load('images/spirit_3.png')
pygame.display.set_icon(icon)

# game variables
FPS = 60
clock = pygame.time.Clock()
start = 0

# define fonts
font_normal = pygame.font.Font('images/Pixeltype.ttf', 50)
font_title = pygame.font.Font('images/Pixeltype.ttf', 65)

# define colours
TEXT_COL = (255, 255, 255)
WHITE = (255, 255, 255)
BLUE = (124, 188, 204)
PINK = (255, 182, 193)
BLACK = (0, 0, 0)

# load images
start_background_image = pygame.transform.scale(pygame.image.load('images/bluesky_03.png').convert_alpha(), (900, 500))
menu_image = pygame.transform.scale(pygame.image.load('images/bluesky_02.png').convert_alpha(), (900, 500))
nox_image = pygame.transform.scale(pygame.image.load('images/spirit_3.png').convert_alpha(), (200, 200))
user_name_image = pygame.transform.scale(pygame.image.load('images/username_sky.jpg').convert_alpha(), (900, 500))
username_score_image = pygame.transform.scale(pygame.image.load('images/username_score.jpg').convert_alpha(),
                                              (900, 500))
todo_background = pygame.transform.scale(pygame.image.load('images/todosky.jpeg').convert_alpha(), (900, 500))
health_background = pygame.transform.scale(pygame.image.load('images/sky2.jpg').convert_alpha(), (900, 500))

SKY = pygame.transform.scale(pygame.image.load('images/spirit_sky.jpg'), (900, 500)).convert_alpha()
GROUND = pygame.Surface((900, 150))
GROUND.fill('Black')

PURPLEBALL_SURFACE = pygame.transform.scale(pygame.image.load('images/purple ball.png'), (40, 40)).convert_alpha()
PINKBALL_SURFACE = pygame.transform.scale(pygame.image.load('images/pink ball.png'), (40, 40)).convert_alpha()

NOX_SURFACE = pygame.image.load('images/spirit_3.png').convert_alpha()
NOX_RECT = NOX_SURFACE.get_rect(midbottom=(80, 350))

# load button images
quit_img = pygame.transform.scale(pygame.image.load("images/quit_white.png").convert_alpha(), (100, 35))
back_img = pygame.transform.scale(pygame.image.load('images/back.png').convert_alpha(), (100, 30))
game_img = pygame.transform.scale(pygame.image.load('images/gamecorner.png').convert_alpha(), (300, 30))
health_img = pygame.transform.scale(pygame.image.load('images/mentalhealth.png').convert_alpha(), (300, 30))
todo_img = pygame.transform.scale(pygame.image.load('images/todolist.png').convert_alpha(), (300, 30))
music1_img = pygame.transform.scale(pygame.image.load('images/trackone.png').convert_alpha(), (300, 30))
music2_img = pygame.transform.scale(pygame.image.load('images/tracktwo.png').convert_alpha(), (300, 30))
music3_img = pygame.transform.scale(pygame.image.load('images/trackthree.png').convert_alpha(), (300, 30))
pause_img = pygame.transform.scale(pygame.image.load('images/pause.png').convert_alpha(), (100, 30))
resume_img = pygame.transform.scale(pygame.image.load('images/resume.png').convert_alpha(), (120, 30))

# create button instances
quit_button = button.Button(770, 450, quit_img, 1)
back_button = button.Button(30, 450, back_img, 1)
game_button = button.Button(320, 170, game_img, 1)
mentalhealth_button = button.Button(320, 275, health_img, 1)
todo_button = button.Button(320, 70, todo_img, 1)
music1_button = button.Button(300, 150, music1_img, 1)
music2_button = button.Button(300, 250, music2_img, 1)
music3_button = button.Button(300, 350, music3_img, 1)
pause_button = button.Button(320, 450, pause_img, 1)
resume_button = button.Button(500, 450, resume_img, 1)

# Introduction
NOX_SCREEN = pygame.transform.scale(pygame.image.load('images/spirit_3.png'), (150, 150)).convert_alpha()
NOX_SCREEN_RECT = NOX_SCREEN.get_rect(center=(450, 250))

GAME_HEAD = font_normal.render("Nox's Adventure", False, WHITE)
GAME_HEAD_RECT = GAME_HEAD.get_rect(center=(450, 100))

MESSAGE = font_normal.render('Press Space To Run', False, WHITE)
MESSAGE_RECT = MESSAGE.get_rect(center=(450, 400))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
obstacle_rect_list = []

# animation start screen
spirit_0_start = pygame.transform.scale(pygame.image.load('images/spirit_3.png').convert_alpha(), (200, 200))
spirit_1_start = pygame.transform.scale(pygame.image.load('images/spirit_3.png').convert_alpha(), (200, 200))
spirit_2_start = pygame.transform.scale(pygame.image.load('images/spirit_0.png').convert_alpha(), (200, 200))
spirit_3_start = pygame.transform.scale(pygame.image.load('images/spirit_1.png').convert_alpha(), (200, 200))
spirit_4_start = pygame.transform.scale(pygame.image.load('images/spirit_2.png').convert_alpha(), (200, 200))
spirit_move_start = [spirit_0_start, spirit_1_start, spirit_2_start, spirit_3_start, spirit_4_start]
spirit_index_start = 0
spirit_surf_start = spirit_move_start[spirit_index_start]


def spirit_animation_start():
    global spirit_index_start, spirit_surf_start
    spirit_index_start += 0.01
    if spirit_index_start >= len(spirit_move_start):
        spirit_index_start = 0
    spirit_surf_start = spirit_move_start[int(spirit_index_start)]


spirit_0_game = pygame.transform.scale(pygame.image.load('images/spirit_3.png').convert_alpha(), (150, 150))
spirit_1_game = pygame.transform.scale(pygame.image.load('images/spirit_3.png').convert_alpha(), (150, 150))
spirit_2_game = pygame.transform.scale(pygame.image.load('images/spirit_0.png').convert_alpha(), (150, 150))
spirit_3_game = pygame.transform.scale(pygame.image.load('images/spirit_1.png').convert_alpha(), (150, 150))
spirit_4_game = pygame.transform.scale(pygame.image.load('images/spirit_2.png').convert_alpha(), (150, 150))
spirit_move_game = [spirit_0_game, spirit_1_game, spirit_2_game, spirit_3_game, spirit_4_game]
spirit_index_game = 0
spirit_surf_game = spirit_move_game[spirit_index_game]


def nox_animation_game_screen():
    global spirit_index_game, spirit_surf_game
    spirit_index_game += 0.1
    if spirit_index_game >= len(spirit_move_game):
        spirit_index_game = 0
    spirit_surf_game = spirit_move_game[int(spirit_index_game)]


nox1 = pygame.transform.scale(pygame.image.load('images/spirit_3.png').convert_alpha(), (65, 65))
nox2 = pygame.transform.scale(pygame.image.load('images/spirit_3.png').convert_alpha(), (65, 65))
nox3 = pygame.transform.scale(pygame.image.load('images/spirit_0.png').convert_alpha(), (65, 65))
nox4 = pygame.transform.scale(pygame.image.load('images/spirit_1.png').convert_alpha(), (65, 65))
nox5 = pygame.transform.scale(pygame.image.load('images/spirit_2.png').convert_alpha(), (65, 65))
NOX_JUMP = pygame.transform.scale(pygame.image.load('images/spirit_1.png').convert_alpha(), (65, 65))
NOX_MOVE = [nox1, nox2, nox3, nox4, nox5]
NOX_INDEX = 0
NOX_SCREEN_SURF = NOX_MOVE[NOX_INDEX]


def nox_small_animation():
    global NOX_SCREEN_SURF, NOX_INDEX

    if NOX_RECT.bottom < 350:
        NOX_SCREEN_SURF = NOX_JUMP
    else:
        NOX_INDEX += 0.1
        if NOX_INDEX >= len(NOX_MOVE):
            NOX_INDEX = 0
        NOX_SCREEN_SURF = NOX_MOVE[int(NOX_INDEX)]


def sql_score():
    con = c.connect(host="localhost", user="root", password="292005", database="nox")
    cursor = con.cursor()
    cursor.execute("insert into score (Name, Score) values ('{}', {})".format(user_name_score, score))
    con.commit()


def sql_high_score_display():
    con = c.connect(host="localhost", user="root", password="292005", database="nox")
    cursor = con.cursor()
    cursor.execute('select MAX(Score) from score')
    high_score = list(cursor.fetchone())
    return high_score


def display_score():
    CURRENT = int(pygame.time.get_ticks() / 1000) - start
    SCORE_SURF = font_normal.render(f'Score: {CURRENT}', False, WHITE)
    SCORE_RECT = SCORE_SURF.get_rect(center=(450, 40))
    WINDOW.blit(SCORE_SURF, SCORE_RECT)
    return CURRENT


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 345:
                WINDOW.blit(PURPLEBALL_SURFACE, obstacle_rect)
            else:
                WINDOW.blit(PINKBALL_SURFACE, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


def collision(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


user_name_score = ''


def username_score():
    global user_name_score
    SCREEN.blit(username_score_image, (0, 0))
    draw_text('Enter your Name: ', font_title, WHITE, 300, 200)
    user_name_rect = pygame.Rect(200, 280, 500, 50)
    active = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if user_name_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        active = False
                    elif event.key == pygame.K_RETURN:
                        noxrun()
                    else:
                        user_name_score += event.unicode
        if active:
            color = BLACK
        else:
            color = WHITE
        pygame.draw.rect(SCREEN, color, user_name_rect, 2)
        string_surf = font_normal.render(user_name_score, True, 'white')
        SCREEN.blit(string_surf, (user_name_rect.x + 10, user_name_rect.y + 10))

        if back_button.draw(SCREEN):
            main()
        pygame.display.flip()


score = 0


def noxrun():
    NOX_GRAVITY = 0
    GAME_ACTIVE = False
    global score
    global obstacle_rect_list

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sql_score()
                pygame.quit()
                sys.exit()

            if GAME_ACTIVE:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if NOX_RECT.collidepoint(e.pos):
                        NOX_GRAVITY = -20
                if e.type == pygame.KEYDOWN and NOX_RECT.bottom >= 350:
                    if e.key == pygame.K_SPACE:
                        pygame.mixer.Sound('audios/jump_sound.mp3').play()
                        NOX_GRAVITY = -20
            else:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        GAME_ACTIVE = True
                        global start
                        start = int(pygame.time.get_ticks() / 1000)

            if e.type == obstacle_timer and GAME_ACTIVE:
                if randint(0, 2):
                    obstacle_rect_list.append(PURPLEBALL_SURFACE.get_rect(bottomright=(randint(900, 1100), 345)))
                else:
                    obstacle_rect_list.append(PINKBALL_SURFACE.get_rect(bottomright=(randint(900, 1100), 230)))

        if GAME_ACTIVE:
            WINDOW.blit(SKY, (0, 0))
            WINDOW.blit(GROUND, (0, 350))
            score = display_score()

            # Nox
            NOX_GRAVITY += 1
            NOX_RECT.y += NOX_GRAVITY
            if NOX_RECT.bottom >= 350:
                NOX_RECT.bottom = 350
            nox_small_animation()
            WINDOW.blit(NOX_SCREEN_SURF, NOX_RECT)

            # Obstacle mt
            obstacle_rect_list = obstacle_movement(obstacle_rect_list)

            # Collision
            GAME_ACTIVE = collision(NOX_RECT, obstacle_rect_list)
        else:
            WINDOW.fill(BLUE)
            nox_animation_game_screen()
            WINDOW.blit(spirit_surf_game, NOX_SCREEN_RECT)
            obstacle_rect_list.clear()
            NOX_RECT.midbottom = (80, 350)

            SCORE_MSG = font_normal.render(f'Your Score: {score}', False, WHITE)
            SCORE_MSG_RECT = SCORE_MSG.get_rect(center=(450, 400))

            high_score = sql_high_score_display()
            HIGH_SCORE = font_normal.render(f'High Score: {high_score}', False, WHITE)
            HIGH_SCORE_RECT = HIGH_SCORE.get_rect(center=(450, 450))

            NEW_HIGH_SCORE = font_normal.render(f'{score}! New Highscore!', False, WHITE)
            NEW_HIGH_SCORE_RECT = NEW_HIGH_SCORE.get_rect(center=(450, 400))
            WINDOW.blit(GAME_HEAD, GAME_HEAD_RECT)
            if score == 0:
                WINDOW.blit(MESSAGE, MESSAGE_RECT)
            elif score > high_score[0]:
                WINDOW.blit(NEW_HIGH_SCORE, NEW_HIGH_SCORE_RECT)
            else:
                WINDOW.blit(SCORE_MSG, SCORE_MSG_RECT)
                WINDOW.blit(HIGH_SCORE, HIGH_SCORE_RECT)
            if quit_button.draw(WINDOW):
                sql_score()
                main()
        pygame.display.update()
        clock.tick(FPS)


user_string = ''
input_string = ''
new_string = ''

user_name = ''


def username():
    global user_name
    SCREEN.blit(user_name_image, (0, 0))
    draw_text('Enter your Name: ', font_title, WHITE, 300, 200)
    user_name_rect = pygame.Rect(200, 280, 500, 50)
    active = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if user_name_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        active = False
                    elif event.key == pygame.K_RETURN:
                        todo()
                    else:
                        user_name += event.unicode
        if active:
            color = BLACK
        else:
            color = WHITE
        pygame.draw.rect(SCREEN, color, user_name_rect, 2)
        string_surf = font_normal.render(user_name, True, 'white')
        SCREEN.blit(string_surf, (user_name_rect.x + 10, user_name_rect.y + 10))

        if back_button.draw(SCREEN):
            main()
        pygame.display.flip()


def taskbox1():
    global user_string, input_string, new_string

    user_rect = pygame.Rect(200, 100, 500, 50)
    input_rect = pygame.Rect(200, 200, 500, 50)
    new_rect = pygame.Rect(200, 300, 500, 50)

    active1 = False
    active2 = False
    active3 = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # task box 1
                if user_rect.collidepoint(event.pos):
                    active1 = True
                else:
                    active1 = False
                # task box 2
                if input_rect.collidepoint(event.pos):
                    active2 = True
                else:
                    active2 = False
                # task box 3
                if new_rect.collidepoint(event.pos):
                    active3 = True
                else:
                    active3 = False

            if event.type == pygame.KEYDOWN:
                # task box 1
                if active1:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_BACKSPACE:
                        active1 = False
                    else:
                        user_string += event.unicode
                # task box 2
                if active2:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_BACKSPACE:
                        active2 = False
                    else:
                        input_string += event.unicode

                # task box 3
                if active3:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_BACKSPACE:
                        active3 = False
                        sql_task()
                    else:
                        new_string += event.unicode
        # task box 1
        if active1:
            color1 = PINK
        else:
            color1 = WHITE
        # task box 2
        if active2:
            color2 = PINK
        else:
            color2 = WHITE
        # task box 3
        if active3:
            color3 = PINK
        else:
            color3 = WHITE

        # draw objects on the screen
        pygame.draw.rect(SCREEN, color1, user_rect, 2)
        pygame.draw.rect(SCREEN, color2, input_rect, 2)
        pygame.draw.rect(SCREEN, color3, new_rect, 2)
        string_surf_1 = font_normal.render(user_string, True, 'white')
        string_surf_2 = font_normal.render(input_string, True, 'white')
        string_surf_3 = font_normal.render(new_string, True, 'white')
        SCREEN.blit(string_surf_1, (user_rect.x + 10, user_rect.y + 10))
        SCREEN.blit(string_surf_2, (input_rect.x + 10, input_rect.y + 10))
        SCREEN.blit(string_surf_3, (new_rect.x + 10, new_rect.y + 10))

        if back_button.draw(SCREEN):
            main()
        pygame.display.flip()


def sql_task():
    global user_name, user_string, input_string, new_string
    con = c.connect(host="localhost", user="root", password="292005", database="nox")
    cursor = con.cursor()
    cursor.execute(
        "insert into tasks (Name, Task1, Task2, Task3) values ('{}', '{}', '{}', '{}')".format(user_name, user_string,
                                                                                               input_string,
                                                                                               new_string))
    con.commit()


def todo():
    SCREEN.blit(todo_background, (0, 0))
    draw_text('Enter your task', font_title, WHITE, 300, 50)
    taskbox1()


def health():
    SCREEN.blit(health_background, (0, 0))
    if music1_button.draw(SCREEN):
        mixer.music.load('audios/Equity_music.mp3')
        mixer.music.play(-1)
    if music2_button.draw(SCREEN):
        mixer.music.load('audios/TheWanderer_music.mp3')
        mixer.music.play(-1)
    if music3_button.draw(SCREEN):
        mixer.music.load('audios/SailingAway_sound.mp3')
        mixer.music.play(-1)
    if pause_button.draw(SCREEN):
        mixer.music.pause()
    elif resume_button.draw(SCREEN):
        mixer.music.unpause()


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    SCREEN.blit(img, (x, y))


def main():
    run = True
    menu_state = "main"
    game_start = False
    mixer.music.load('audios/AQuietDay_music.mp3')
    mixer.music.play(-1)
    while run:
        if game_start:
            if menu_state == 'main':
                SCREEN.blit(menu_image, (0, 0))
                mixer.music.fadeout(3000)
                if game_button.draw(SCREEN):
                    menu_state = 'game'
                if todo_button.draw(SCREEN):
                    menu_state = 'todo'
                if mentalhealth_button.draw(SCREEN):
                    menu_state = 'health'
                if quit_button.draw(SCREEN):
                    run = False
            if menu_state == 'game':
                username_score()
                if back_button.draw(WINDOW):
                    menu_state = 'main'

            if menu_state == 'todo':
                username()

            if menu_state == 'health':
                health()
                draw_text('Come, Listen to Music & Relax your Mind', font_title, WHITE, 100, 40)
                if back_button.draw(SCREEN):
                    menu_state = 'main'
        #
        else:
            SCREEN.blit(start_background_image, (0, 0))
            draw_text('Welcome to NOX! Your Productivity Tracker!', font_title, BLACK, 50, 50)
            spirit_animation_start()
            SCREEN.blit(spirit_surf_start, (350, 170))
            draw_text('Press Space to start', font_title, BLACK, 250, 450)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_start = True
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


main()
