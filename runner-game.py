# IMPORTS
import pygame 
from sys import exit
from random import randint, choice

# SPRITES
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Player animation surfaces / index / lists
        player_walk_1 = pygame.image.load('assets/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('assets/player/player_walk_2.png').convert_alpha()
        self.frame_index = 0
        self.frames = [player_walk_1, player_walk_2]
        self.player_jump = pygame.image.load('assets/player/player_jump.png').convert_alpha()
    
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.frame_index += 0.1
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.input()
        self.apply_gravity()
        self.animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_frame_1 = pygame.image.load('assets/fly/fly_1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('assets/fly/fly_2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load('assets/snail/snail_1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('assets/snail/snail_2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def destroy_out_of_bounds(self):
        if self.rect.x <= -50:
            self.kill()
    
    def update(self):
        self.animation()
        self.rect.x -= 5
        self.destroy_out_of_bounds()


# HELPER FUNCTIONS
def calculate_score():
    score = int((pygame.time.get_ticks() - start_time) / 1000)
    return score

def display_score(score_type, x, y):
    score_surf = font.render(f'{score_type} {score}', False, (111,196,169))
    score_rect = score_surf.get_rect(center = (x, y))
    screen.blit(score_surf, score_rect)

def start_game():
    global start_time, game_active
    # Reset variables for a clean beginning
    start_time = pygame.time.get_ticks()
    player.sprite.rect.midbottom = (80,300)
    obstacle_group.empty()
    player.gravity = 0
    game_active = True

def is_collision():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        return True
    else: return False

def game_start_splash():
    screen.fill((204, 229, 255))

    player_stand = pygame.transform.rotozoom((pygame.image.load('assets/player/player_stand.png')), 0, 2)
    player_stand_rect = player_stand.get_rect(center = (400, 200))

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



# LET'S GOOOOOO
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Pixel Runner')
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/Pixeltype.ttf', 50)

# Variables
game_active = False
start_time = 0
score = 0

# Sprite Groups
player = pygame.sprite.GroupSingle()
player.add(Player()) 

obstacle_group = pygame.sprite.Group()

# Background surfaces
sky_surf = pygame.image.load('assets/sky.png').convert()
ground_surf = pygame.image.load('assets/ground.png').convert()

# Obstacle timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
obstacle_rect_list = []

# Game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            # Create obstacles       
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['snail', 'snail', 'snail', 'fly'])))  
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_game()

    # Active Gameplay
    if game_active:
        # Background and score
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,300))
        score = calculate_score()
        display_score('', 400, 50)

        # Generate snails and flies
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Player
        player.draw(screen)
        player.update()

        # Collisions
        game_active = not is_collision()
    
    else:
        game_start_splash()

    # Update the display surface, and set the maximum frame rate (i.e. how often to run the main 'While True' loop)
    pygame.display.update()
    clock.tick(60)