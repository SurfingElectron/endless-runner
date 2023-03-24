# IMPORTS
import pygame 
from sys import exit


# HELPER FUNCTIONS
def display_score():
    score = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = font.render(f'{score}', False, (111,196,169))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return score

def game_start_splash():
    screen.fill((204, 229, 255))

    title_surf = font.render('PIXEL RUNNER', False, (111,196,169))
    title_rect = title_surf.get_rect(center = (400, 50))

    instruct_surf = font.render('Press SPACE to start', False, (111,196,169))
    instruct_rect = instruct_surf.get_rect(center = (400, 350))

    screen.blit(player_stand_surf, player_stand_rect)
    screen.blit(title_surf, title_rect)

    high_score_surf = font.render(f'High Score: {score}', False, (111,196,169))
    high_score_rect = high_score_surf.get_rect(center = (400, 350))
 
    if score == 0:
        screen.blit(instruct_surf, instruct_rect)
    else:
        screen.blit(high_score_surf, high_score_rect)


# LET'S GOOOOOO
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Pixel Runner')
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/Pixeltype.ttf', 50)

# Create variables
# Speed variables for game difficulty?
game_active = False
start_time = 0
player_gravity = 0
score = 0



# Create surfaces & rectangles
sky_surf = pygame.image.load('assets/sky.png').convert()
ground_surf = pygame.image.load('assets/ground.png').convert()

snail_surf = pygame.image.load('assets/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (750, 300))

player_walk_surf = pygame.image.load('assets/player/player_walk1.png').convert_alpha()
player_rect = player_walk_surf.get_rect(midbottom = (80, 300))

player_stand_surf = pygame.transform.rotozoom((pygame.image.load('assets/player/player_stand.png')), 0, 2)
player_stand_rect = player_stand_surf.get_rect(center = (400, 200))

while True:

    # Check for user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:    
            if event.type == pygame.KEYDOWN and player_rect.bottom >= 300:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                snail_rect.left = 800
                start_time = pygame.time.get_ticks()
                game_active = True


    # Active Gameplay
    if game_active:
        # Background and score
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,300))
        score = display_score()

        # Snail
        snail_rect.x -= 5
        if snail_rect.right <= 0: snail_rect.left = 800
        screen.blit(snail_surf, snail_rect)

        # Player
        player_gravity +=1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_walk_surf, player_rect)

        # Collisions
        if snail_rect.colliderect(player_rect):
            game_active = False
    
    else:
        game_start_splash()
        


    # Update the display surface, and set the maximum frame rate (i.e. how often to run the main 'While True' loop)
    pygame.display.update()
    clock.tick(60)