import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 500
FPS = 60

# Set up the display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sphere physics engine")

# Clock for controlling the frame rate
timer = pygame.time.Clock()

# Sphere properties
spherex = 400
sphere_radius = 25
initial_velocity = 0
gravity = 0.5
bounce_reduction = 0.8  # Increased from 0.7 to 0.8 for more pronounced effect

# Variables for bounce calculation
velocity = initial_velocity
spherey = HEIGHT / 2  # Start in the middle of the screen

# Main loop
run = True
while run:
    timer.tick(FPS)
    win.fill((0, 0, 0))  # Clear screen with black
    
    # Draw the sphere
    pygame.draw.circle(win, (128, 128, 128), (spherex, int(spherey)), sphere_radius)
    
    # Update sphere position
    spherey += velocity
    velocity += gravity
    
    # Check for collision with bottom boundary
    if spherey + sphere_radius >= HEIGHT:
        spherey = HEIGHT - sphere_radius  # Correct position
        velocity = -velocity * bounce_reduction  # Reverse and reduce velocity
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()