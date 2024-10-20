import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Colors
WHITE = (255, 255, 255)

# Set up the clock for frame rate
clock = pygame.time.Clock()
FPS = 60

# Load the bird image and set its rectangle
bird_image = pygame.image.load("bird.png")
bird_rect = bird_image.get_rect(center=(100, HEIGHT // 2))

# Load background image
bg_image = pygame.image.load("background.png")

# Variables for bird movement
gravity = 0.5
bird_movement = 0

# Set up pipes
pipe_image = pygame.image.load("pipe.png")
pipe_list = []
pipe_height = [300, 400, 500]

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            screen.blit(pipe_image, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_image, False, True)
            screen.blit(flip_pipe, pipe)

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return [pipe for pipe in pipes if pipe.right > 0]

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= HEIGHT:
        return False
    return True

def rotate_bird(bird):
    return pygame.transform.rotozoom(bird, -bird_movement * 3, 1)

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_image.get_rect(midtop=(WIDTH + 100, random_pipe_pos))
    top_pipe = pipe_image.get_rect(midbottom=(WIDTH + 100, random_pipe_pos - 150))
    return bottom_pipe, top_pipe

def game_over():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 50, HEIGHT // 2 - 10))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 10
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    # Apply gravity
    bird_movement += gravity
    bird_rect.centery += bird_movement

    # Draw background
    screen.blit(bg_image, (0, 0))

    # Draw and move pipes
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    # Draw bird
    rotated_bird = rotate_bird(bird_image)
    screen.blit(rotated_bird, bird_rect)

    # Check for collisions
    if not check_collision(pipe_list):
        game_over()

    pygame.display.update()
    clock.tick(FPS)
