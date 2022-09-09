import pygame
import random
import time
import sys

# from Tools.demo.spreadsheet import center

pygame.init()
clock = pygame.time.Clock()


def game_floor():
    screen.blit(floor, (floor_x_pos, 900))
    screen.blit(floor, (floor_x_pos + 576, 900))


def check_collision(pipes):
    # collision with pipes
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            die_sound.play()
            return False

    # check hit the bottom floor and upside the main window
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        die_sound.play()
        return False
    return True


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


# variables
gravity = 0.25
bird_movement = 0

screen_width = 576
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))

background = pygame.image.load("assets/images/background-day.png").convert()
background = pygame.transform.scale2x(background)

bird = pygame.image.load("assets/images/redbird-midflap.png").convert_alpha()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100, 512))

floor = pygame.image.load("assets/images/base.png").convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

message = pygame.image.load("assets/images/message.png").convert_alpha()  # makes it transparent
message = pygame.transform.scale2x(message)
game_over_rect = message.get_rect(center=(288, 512))

# building pipes
pipe_surface = pygame.image.load("assets/images/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [400, 600, 800]

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

flap_sound = pygame.mixer.Sound("assets/audio/wing.wav")
die_sound = pygame.mixer.Sound("assets/audio/die.wav")
game_active = True
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                bird_movement = 0
                bird_rect.center = (100, 512)
                pipe_list.clear()
                game_active = True

        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

    screen.blit(background, (0, 0))
    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird, bird_rect)

        # Draw Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # check for collision
        game_active = check_collision(pipe_list)
    else:
        screen.blit(message, game_over_rect)
    # create and move floor
    floor_x_pos -= 1
    game_floor()
    if floor_x_pos < -576:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(80)

pygame.quit()
quit()
