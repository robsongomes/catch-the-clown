import pygame, random

pygame.init()

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 200
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Catch the clown")

# set fps and clock
FPS = 60
clock = pygame.time.Clock()

# set game values
PLAYER_STARTING_LIVES = 5
CLOWN_STARTING_VELOCITY = 3
CLOWN_ACCELERATION = .5

score = 0
player_lives = PLAYER_STARTING_LIVES

clown_velocity = CLOWN_STARTING_VELOCITY
clown_dx = random.choice([-1, 1])
clown_dy = random.choice([-1, 1])

# set colors
BLUE = (1, 175, 209)
YELLOW = (248, 231, 28)
BLACK = (0, 0, 0)

# set fonts
font = pygame.font.Font("Franxurter.ttf", 32)

# set text
title_text = font.render("Catch the Clown", True, BLUE)
title_rect = title_text.get_rect()
title_rect.topleft = (50, 10)

score_text = font.render("SCORE: " + str(score), True, YELLOW)
score_rect = score_text.get_rect()
score_rect.topright = (WINDOW_WIDTH - 50, 10)


lives_text = font.render("LIVES: " + str(player_lives), True, YELLOW)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 50, 50)

# set sound and music
pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1)

click_sound = pygame.mixer.Sound("click_sound.wav")

# set images
clown = pygame.image.load("clown.png")
clown_rect = clown.get_rect()
clown_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_coord = pygame.mouse.get_pos()    
            if clown_rect.collidepoint(mouse_coord):
                click_sound.play()
                score += 1
                clown_velocity += CLOWN_ACCELERATION

                p_dx = clown_dx
                p_dy = clown_dy
                while (p_dx == clown_dx and p_dy == clown_dy):
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])
            else:
                player_lives -= 1
    
    clown_rect.x += clown_velocity * clown_dx
    clown_rect.y += clown_velocity * clown_dy
    
    if clown_rect.left <= 0 or clown_rect.right >= WINDOW_WIDTH:
        clown_dx *= -1
        print("saiu da tela", clown_rect, clown_dx, clown_velocity)
    if clown_rect.bottom >= WINDOW_HEIGHT or clown_rect.top <= 0:
        clown_dy *= -1
        print("saiu da tela", clown_rect, clown_dy, clown_velocity)

    if player_lives == 0:
        game_over = True

        pygame.mixer.music.stop()
        game_over_text = font.render("GAME OVER", True, YELLOW, BLUE)
        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        
        game_continue_text = font.render("CLICK ANYWHERE TO PLAY AGAIN", True, YELLOW, BLUE)
        game_continue_text_rect = game_continue_text.get_rect()
        game_continue_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50)
        
        display_surface.blit(game_over_text, game_over_text_rect)
        display_surface.blit(game_continue_text, game_continue_text_rect)

        pygame.display.update()

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_over = False
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    clown_velocity = CLOWN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)
                if event.type == pygame.QUIT:
                    game_over = False
                    running = False

            pygame.display.update()
    

    display_surface.fill(YELLOW, (0, 0, WINDOW_WIDTH//2, WINDOW_HEIGHT))
    display_surface.fill(BLUE, (WINDOW_WIDTH//2, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.draw.line(display_surface, BLACK, (WINDOW_WIDTH//2, 0), (WINDOW_WIDTH//2,WINDOW_HEIGHT), 6)

    score_text = font.render("SCORE: " + str(score), True, YELLOW)
    lives_text = font.render("LIVES: " + str(player_lives), True, YELLOW)

    display_surface.blit(title_text, title_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(lives_text, lives_rect)
    display_surface.blit(clown, clown_rect)

    pygame.display.update()
    clock.tick(FPS)