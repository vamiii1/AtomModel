import pygame
import time
import math
running = True
x1 = 0
locations = []
def atomanimation():
    global running, locations, x1
    proton = pygame.draw.circle(screen, "red", (200, 200), 10)
    electron = pygame.draw.circle(screen, "blue", (200, 200), 5)
    while running:    
        for i in range(360):
            x = 100 * math.cos(math.radians(i))
            y = 100 * math.sin(math.radians(i))
            electron.center = (x + 200, y + 200)
            screen.fill("black")
            proton = pygame.draw.circle(screen, "red", (200, 200), 10)
            electron = pygame.draw.circle(screen, "blue", (x + 200, y + 200), 5)
            locations.append((200, y))
            locations = list(set(locations))
            
            pygame.draw.circle(screen, "white", (500, y+200), 5)
            pygame.draw.line(screen, "white", (500, 200), (500, y+200))
            pygame.display.flip()
            x1+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            time.sleep(0.005)
        locations = []

screen = pygame.display.set_mode((600, 600))
atomanimation()
pygame.init()