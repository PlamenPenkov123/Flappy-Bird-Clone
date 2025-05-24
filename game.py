import pygame
import random

# Intitalize the game
pygame.init()

# Set the window attributes
screen_height, screen_width = 500, 500
screen = pygame.display.set_mode((screen_height, screen_width))
pygame.display.set_caption("Flappy Gato")

# Set the background
background = pygame.image.load('images/sky.jpg')
background = pygame.transform.scale(background, (screen_height, screen_width))

# Set the grass
grass = pygame.image.load("images/grass.png")
grass_height = 75
grass = pygame.transform.scale(grass, (screen_width, grass_height))

# Set the character
character = pygame.image.load("images/cat.png")
character = pygame.transform.scale(character, (75, 75))
character_rect = character.get_rect()
character_rect.center = (screen_width // 2, screen_height // 2)

# Seting the pipes
pipe_width = 70
pipe_gap = 175
pipe_speed = 3

pipe_x = screen_width
def random_pipe_height():
    return random.randint(50, screen_height - grass_height - pipe_gap - 50)

pipe_top_heigth = random_pipe_height()

velocity = 0
gravity = 0.5
jump_strength = -7.5

font = pygame.font.SysFont(None, 60)
game_over = False

clock = pygame.time.Clock();

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                character_rect.center = (screen_width // 2, screen_height // 2)
                velocity = 0
                pipe_x = screen_width
                pipe_top_height = random_pipe_height()
                game_over = False
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                velocity = jump_strength
    
    if not game_over:
        # Apply gravity to the velocity
        velocity += gravity
        # Update position of the player
        character_rect.y += velocity

        # Stops the game when the player touches the grass
        if character_rect.bottom > screen_height - grass_height:
           character_rect.bottom = screen_height - grass_height
           game_over = True
        if character_rect.top <= 0:
            character_rect.top = 0
            game_over = True

        # Move the pipe left
        pipe_x -= pipe_speed

        # Reset pipe when it leaves the screen
        if pipe_x + pipe_width < 0:
            pipe_x = screen_width
            pipe_top_heigth = random_pipe_height()
        
        # Collision with the pipe
        pipe_top_rect = pygame.Rect(pipe_x, 0, pipe_width, pipe_top_heigth)
        pipe_bottom_rect = pygame.Rect(pipe_x, pipe_top_heigth + pipe_gap, pipe_width, screen_height - grass_height - (pipe_top_heigth + pipe_gap))

        if character_rect.colliderect(pipe_top_rect) or character_rect.colliderect(pipe_bottom_rect):
            game_over = True


        # Drawing
        screen.blit(background, (0, 0))
        screen.blit(grass, (0, screen_height - grass_height))
        screen.blit(character, character_rect)
        
        pygame.draw.rect(screen, (0, 255, 0), pipe_top_rect)
        pygame.draw.rect(screen, (0, 255, 0), pipe_bottom_rect)
    if game_over:
        game_over_text = font.render("Game over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(game_over_text, text_rect)
    else:
        screen.blit(character, character_rect)

    pygame.display.flip()

pygame.quit()