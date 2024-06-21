import math
import random
import pygame

windows_width, windows_height = 500, 500
display = pygame.display.set_mode((windows_width, windows_height))
x, y = 50, 50
oldX, oldY = 50, 50
maxLen = 20
t = 0
running = True
trail = []
spawnObjects = []
prevKey = None
pressed = [0, 0, 0, 0]


class Head:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.x = x
        self.y = y

    def draw(self, win, color):
        pygame.draw.circle(win, color, (self.x, self.y), 10)


class TrailObj:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 5)
        self.x = x
        self.y = y

    def draw(self, win, color):
        pygame.draw.circle(win, color, (self.x, self.y), 5)


def dist(x, y, oldX, oldY):
    dx = oldX - x
    dy = oldY - y
    return math.sqrt((dx*dx) + (dy*dy))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    t += 1
    if dist(x, y, oldX, oldY) >= 2:
        oldX, oldY = x, y
        trail.insert(0, TrailObj(x, y))
        if len(trail) > maxLen:
            trail.pop(-1)
    if t // 10 >= 1000:
        t = 0
        spawnObjects.append(TrailObj(random.randint(5, windows_width - 5), random.randint(5, windows_height - 5)))
    if len(spawnObjects) >= 5:
        spawnObjects.pop(0)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] and prevKey != 'a':
        x += 0.1
        prevKey = 'd'
    if keys[pygame.K_a] and prevKey != 'd':
        x += -0.1
        prevKey = 'a'
    if keys[pygame.K_s] and prevKey != 'w':
        y += 0.1
        prevKey = 's'
    if keys[pygame.K_w] and prevKey != 's':
        y += -0.1
        prevKey = 'w'
    if x < 0 or x > windows_width or y < 0 or y > windows_height:
        running = False
    display.fill((0, 0, 0))
    head = Head(x, y)
    for i in range(len(trail)):
        if i > 10:
            if head.rect.colliderect(trail[i].rect):
                running = False
        trail[i].draw(display, (127, 255, 0))
    for i in spawnObjects:
        i.draw(display, (255, 0, 0))
        if dist(x, y, i.x, i.y) <= 15:
            spawnObjects.remove(i)
            maxLen += 10
    head.draw(display, (127, 255, 0))
    pygame.display.flip()
