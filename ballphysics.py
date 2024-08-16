import pygame
pygame.init()

WIDTH = 800
HEIGHT = 500
win = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Moving sphere")

timer = pygame.time.Clock()
fps = 60
run = True

spherex = 200
spherey = 200
sphereVel = 5

def sphere_draw():
    pygame.draw.rect(win, 'grey', [spherex, spherey,50,50], 0, 50)

while run:
    timer.tick(fps)
    win.fill('black')
    
    sphere_draw()
    if spherey >= 450:
        spherey -= sphereVel
    elif spherey < 0:
        spherey += sphereVel
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()