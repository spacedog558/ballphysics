import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 500
FPS = 60

# Set up the display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Multi-Sphere Physics Simulation")

# Clock for controlling the frame rate
timer = pygame.time.Clock()

# Sphere class
class Sphere:
    def __init__(self, x, y, vx=0, vy=0):
        self.x = x
        self.y = y
        self.radius = random.randint(15, 30)
        self.velocity_x = vx
        self.velocity_y = vy
        self.mass = self.radius ** 2  # Mass proportional to area
        self.dragging = False
        self.last_pos = (x, y)

    def update(self, dt):
        if not self.dragging:
            self.velocity_y += gravity * dt
            self.x += self.velocity_x * dt
            self.y += self.velocity_y * dt

            # Bounce off bottom
            if self.y + self.radius >= HEIGHT:
                self.y = HEIGHT - self.radius
                self.velocity_y = -self.velocity_y * bounce_reduction

            # Bounce off top
            if self.y - self.radius <= 0:
                self.y = self.radius
                self.velocity_y = -self.velocity_y * bounce_reduction

            # Bounce off sides
            if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
                self.x = max(self.radius, min(WIDTH - self.radius, self.x))
                self.velocity_x = -self.velocity_x * bounce_reduction

    def draw(self):
        speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        max_speed = 500  # Adjust this value to change color sensitivity
        color_value = min(speed / max_speed, 1)
        color = (int(255 * color_value), int(255 * (1 - color_value)), 0)
        pygame.draw.circle(win, color, (int(self.x), int(self.y)), self.radius)

def check_collision(s1, s2):
    dx = s1.x - s2.x
    dy = s1.y - s2.y
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance < s1.radius + s2.radius:
        # Collision detected, calculate new velocities
        angle = math.atan2(dy, dx)
        sin = math.sin(angle)
        cos = math.cos(angle)

        # Rotate sphere velocities
        s1_velocity_x = s1.velocity_x * cos + s1.velocity_y * sin
        s1_velocity_y = s1.velocity_y * cos - s1.velocity_x * sin
        s2_velocity_x = s2.velocity_x * cos + s2.velocity_y * sin
        s2_velocity_y = s2.velocity_y * cos - s2.velocity_x * sin

        # Collision reaction
        total_mass = s1.mass + s2.mass
        new_s1_velocity_x = ((s1.mass - s2.mass) * s1_velocity_x + 2 * s2.mass * s2_velocity_x) / total_mass
        new_s2_velocity_x = ((s2.mass - s1.mass) * s2_velocity_x + 2 * s1.mass * s1_velocity_x) / total_mass

        # Rotate velocities back
        s1.velocity_x = new_s1_velocity_x * cos - s1_velocity_y * sin
        s1.velocity_y = s1_velocity_y * cos + new_s1_velocity_x * sin
        s2.velocity_x = new_s2_velocity_x * cos - s2_velocity_y * sin
        s2.velocity_y = s2_velocity_y * cos + new_s2_velocity_x * sin

        # Move spheres apart to prevent sticking
        overlap = 0.5 * (s1.radius + s2.radius - distance + 1)
        s1.x += overlap * cos
        s1.y += overlap * sin
        s2.x -= overlap * cos
        s2.y -= overlap * sin

# Game properties
gravity = 9.81 * 100  # Increased gravity (9.81 m/s^2 * 100 pixels/meter)
bounce_reduction = 0.8

# List to store all spheres
spheres = [Sphere(WIDTH // 2, HEIGHT // 2)]

# Main loop
run = True
last_time = pygame.time.get_ticks()
while run:
    # Calculate delta time
    current_time = pygame.time.get_ticks()
    dt = (current_time - last_time) / 1000.0  # Convert to seconds
    last_time = current_time

    timer.tick(FPS)
    win.fill((0, 0, 0))  # Clear screen with black
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if click is inside any sphere
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for sphere in spheres:
                if math.sqrt((mouse_x - sphere.x)**2 + (mouse_y - sphere.y)**2) <= sphere.radius:
                    sphere.dragging = True
                    sphere.last_pos = (mouse_x, mouse_y)
                    break
            else:
                # If no sphere was clicked, spawn a new one
                spheres.append(Sphere(mouse_x, mouse_y))
        elif event.type == pygame.MOUSEBUTTONUP:
            for sphere in spheres:
                if sphere.dragging:
                    sphere.dragging = False
                    # Calculate velocity based on mouse movement
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    sphere.velocity_x = (mouse_x - sphere.last_pos[0]) / dt
                    sphere.velocity_y = (mouse_y - sphere.last_pos[1]) / dt
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                # Spawn a new sphere at the mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                spheres.append(Sphere(mouse_x, mouse_y))

    # Update and draw all spheres
    for i, sphere in enumerate(spheres):
        if sphere.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            sphere.x, sphere.y = mouse_x, mouse_y
            sphere.last_pos = (mouse_x, mouse_y)
        else:
            sphere.update(dt)
        
        # Check collisions with other spheres
        for other_sphere in spheres[i+1:]:
            check_collision(sphere, other_sphere)
        
        sphere.draw()
    
    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()