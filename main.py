import os
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fireboy and Watergirl")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Отображение игры на экране
    pygame.display.update()

fireboy_image = pygame.image.load(os.path.join("assets", "Fireboy.png")).convert_alpha()
watergirl_image = pygame.image.load(os.path.join("assets", "Watergirl.png")).convert_alpha()
wall_image = pygame.image.load(os.path.join("assets", "wall.png")).convert()
water_image = pygame.image.load(os.path.join("assets", "water.png")).convert_alpha()
hazard_image = pygame.image.load(os.path.join("assets", "hazard.png")).convert_alpha()
door_closed_image = pygame.image.load(os.path.join("assets", "door_closed.png")).convert_alpha()
door_open_image = pygame.image.load(os.path.join("assets", "door_open.png")).convert_alpha()

class Fireboy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = fireboy_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def move(self, direction):
        if direction == "up":
            self.rect.y -= 5
        elif direction == "down":
            self.rect.y += 5
        elif direction == "left":
            self.rect.x -= 5
        elif direction == "right":
            self.rect.x += 5


class Watergirl(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = watergirl_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, direction):
        if direction == "up":
            self.rect.y -= 5
        elif direction == "down":
            self.rect.y += 5
        elif direction == "left":
            self.rect.x -= 5
        elif direction == "right":
            self.rect.x += 5

    # Класс для стен


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = wall_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # Класс для воды


class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = water_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # Класс для опасной жидкости


class Hazard(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = hazard_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class DoorClosed(pygame.sprite.Sprite):
    def init(self, x, y):
        super().init()
        self.image = door_closed_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class DoorOpen(pygame.sprite.Sprite):
    def init(self, x, y):
        super().init()
        self.image = door_open_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


fireboy = Fireboy(50, 50)
watergirl = Watergirl(700, 500)
wall = Wall(200, 200)
water = Water(400, 300)
hazard = Hazard(600, 100)
door_closed = DoorClosed(300, 400)
door_open = DoorOpen(400, 400)

all_sprites = pygame.sprite.Group()
all_sprites.add(fireboy, watergirl, wall, water, hazard, door_closed, door_open)

walls = pygame.sprite.Group()
walls.add(wall)

waters = pygame.sprite.Group()
waters.add(water)

hazards = pygame.sprite.Group()
hazards.add(hazard)

doors_closed = pygame.sprite.Group()
doors_closed.add(door_closed)

doors_open = pygame.sprite.Group()
doors_open.add(door_open)

# Обновление движения персонажей
keys = pygame.key.get_pressed()
if keys[pygame.K_w]:
    fireboy.move("up")
if keys[pygame.K_s]:
    fireboy.move("down")
if keys[pygame.K_a]:
    fireboy.move("left")
if keys[pygame.K_d]:
    fireboy.move("right")

if keys[pygame.K_UP]:
    watergirl.move("up")
if keys[pygame.K_DOWN]:
    watergirl.move("down")
if keys[pygame.K_LEFT]:
    watergirl.move("left")
if keys[pygame.K_RIGHT]:
    watergirl.move("right")

# Отображение игры на экране
screen.fill((255, 255, 255))
all_sprites.draw(screen)
pygame.display.update()

# Завершение игры
pygame.quit()