# IMPORTS
import pygame 
from sys import exit


# HELPER FUNCTIONS
def display_score():
    score = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = font.render(f'{score}', False, (100, 149, 237))
    score_rect = score_surf.get_rect(midtop = (400, 50))
    screen.blit(score_surf, score_rect)


# LET'S GOOOOOO
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Endless Runner')
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/Pixeltype.ttf', 50)

# Create variables
# Speed variables for game difficulty?
game_active = True
start_time = 0
player_gravity = 0



# Create surfaces & rectangles
sky_surf = pygame.image.load('assets/sky.png').convert()
ground_surf = pygame.image.load('assets/ground.png').convert()



snail_surf = pygame.image.load('assets/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (750, 300))

player_surf = pygame.image.load('assets/player/player_walk1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))

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

        display_score()
        #screen.blit(score_surf, score_rect)

        # Snail
        snail_rect.x -= 4
        if snail_rect.right <= 0: snail_rect.left = 800
        screen.blit(snail_surf, snail_rect)

        # Player
        player_gravity +=1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        # Collisions
        if snail_rect.colliderect(player_rect):
            game_active = False
    
    else:
        screen.fill('Blue')


    # Update the display surface, and set the maximum frame rate (i.e. how often to run the main 'While True' loop)
    pygame.display.update()
    clock.tick(60)