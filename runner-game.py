# IMPORTS
import pygame 
from sys import exit
from random import randint


# HELPER FUNCTIONS
def calculate_score():
    score = int((pygame.time.get_ticks() - start_time) / 1000)
    return score

def display_score(score_type, x, y):
    score_surf = font.render(f'{score_type} {score}', False, (111,196,169))
    score_rect = score_surf.get_rect(center = (x, y))
    screen.blit(score_surf, score_rect)

def game_start_splash():
    screen.fill((204, 229, 255))

    title_surf = font.render('PIXEL RUNNER', False, (111,196,169))
    title_rect = title_surf.get_rect(center = (400, 50))

    instruct_surf = font.render('Press SPACE to start', False, (111,196,169))
    instruct_rect = instruct_surf.get_rect(center = (400, 350))

    screen.blit(player_stand, player_stand_rect)
    screen.blit(title_surf, title_rect)

    # Show instructions if it's the first time, else show the last score
    if score == 0:
        screen.blit(instruct_surf, instruct_rect)
    else:
        display_score('High Score:', 400, 350)


def change_obstacle_index(index):
    if index == 0:
        index = 1
    else:
        index = 0
    return index

def obstacle_movement(obstacles):
    if obstacles:
        for obstacle in obstacles:
            obstacle.x -= 5

            # Check bottom position of rect to see if it's a snail or a fly
            if obstacle.bottom == 300:
                screen.blit(snail_surf, obstacle)
            else:
                screen.blit(fly_surf, obstacle)

        # Deletes out of bounds obstacles (i.e. only copies visible ones)
        obstacles = [obstacle for obstacle in obstacles if obstacle.x > -100]
        return obstacles
    
    else: return []

def is_collision(player, obstacles):
    if obstacles:
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                return True
    return False

def player_animation():
    global player_surf, player_walk_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_walk_index += 0.1
        if player_walk_index >= len(player_walk):
            player_walk_index = 0
        player_surf = player_walk[int(player_walk_index)]
    
    screen.blit(player_surf, player_rect)

# LET'S GOOOOOO
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Pixel Runner')
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/Pixeltype.ttf', 50)

# Variables
game_active = True
start_time = 0
score = 0
player_gravity = 0

# Background surfaces
sky_surf = pygame.image.load('assets/sky.png').convert()
ground_surf = pygame.image.load('assets/ground.png').convert()

# Player surfaces / rects / variables & lists for animation
player_stand = pygame.transform.rotozoom((pygame.image.load('assets/player/player_stand.png')), 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

player_jump = pygame.image.load('assets/player/player_jump.png').convert_alpha()

player_walk_1 = pygame.image.load('assets/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('assets/player/player_walk_2.png').convert_alpha()
player_walk_index = 0
player_walk = [player_walk_1, player_walk_2]
player_surf = player_walk[player_walk_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))

# Obstacle surfaces / variables & lists for animation
snail_frame_1 = pygame.image.load('assets/snail/snail_1.png').convert_alpha()
snail_frame_2 = pygame.image.load('assets/snail/snail_2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('assets/fly/fly_1.png').convert_alpha()
fly_frame_2 = pygame.image.load('assets/fly/fly_2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

# Obstacle timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
obstacle_rect_list = []

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

# Game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            # Check user inputs    
            if event.type == pygame.KEYDOWN and player_rect.bottom >= 300:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20

            # Check timers        
            if event.type == obstacle_timer:
                if randint(0,2): # generates 0 or 1 - evaluates to True/False
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900, 1100), 210)))
            if event.type == snail_animation_timer:
                snail_frame_index = change_obstacle_index(snail_frame_index)
                snail_surf = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                fly_frame_index = change_obstacle_index(fly_frame_index)
                fly_surf = fly_frames[fly_frame_index]
            
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Reset variables for a clean start!
                start_time = pygame.time.get_ticks()
                obstacle_rect_list = []
                player_rect.midbottom = (80,300)
                player_gravity = 0
                game_active = True

    # Active Gameplay
    if game_active:
        # Background and score
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,300))
        score = calculate_score()
        display_score('', 400, 50)

        # Generate snails and flies
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Player
        player_gravity +=1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()

        # Collisions
        game_active = not is_collision(player_rect, obstacle_rect_list)
    
    else:
        game_start_splash()


    # Update the display surface, and set the maximum frame rate (i.e. how often to run the main 'While True' loop)
    pygame.display.update()
    clock.tick(60)