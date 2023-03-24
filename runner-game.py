# IMPORTS
import pygame 
from sys import exit


# HELPER FUNCTIONS


# LET'S GOOOOOO
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Endless Runner')
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/Pixeltype.ttf', 50)

# Create surfaces
sky_surface = pygame.image.load('assets/sky.png')
ground_surface = pygame.image.load('assets/ground.png')
text_surface = font.render('TEST', False, (255, 255, 255))

while True:

    # Check for user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))
    screen.blit(text_surface, (400, 50))

    # Update the display surface, and set the maximum frame rate (i.e. how often to run the main 'While True' loop)
    pygame.display.update()
    clock.tick(60)