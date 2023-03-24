# IMPORTS
import pygame 
from sys import exit


# HELPER FUNCTIONS


# LET'S GOOOOOO
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Endless Runner')
clock = pygame.time.Clock()

while True:

    # Check for user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Update the display surface, and set the maximum frame rate (i.e. how often to run the main While True loop)
    pygame.display.update()
    clock.tick(60)