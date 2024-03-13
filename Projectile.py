import pygame, sys
from pygame.locals import *
from object.data import *

ColliderBoxOn = False


def drawBar(screen):
    pygame.draw.rect(screen, (0, 0, 0), (0, 2, 100 * 2 + 2, 22))
    pygame.draw.rect(screen, (255, 255, 255), (0, 3, 100 * 2, 20))
    pygame.draw.rect(screen, (0, 0, 0), (0, 24, 100 * 2 + 2, 22))
    pygame.draw.rect(screen, (255, 255, 255), (0, 25, 100 * 2, 20))


def ScreenLimit(target):
    if target.x + target.width > WIDTH:
        target.x = WIDTH - target.width
    if target.x < 0:
        target.x = 0
    if target.y + target.height > HEIGHT:
        target.y = HEIGHT - target.height
    if target.y < 140:
        target.y = 140


class Projectile(object):
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.initProperty()
        self.hitBox = (x, y, self.radius)

    def initProperty(self):
        self.color = player_bulletColor
        self.radius = player_bulletRadius
        self.speed = player_bulletSpeed
        self.dame = player_bulletDamage

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (100, 100, 100), (self.x, self.y), self.radius - 2)
        pygame.draw.circle(screen, (250, 250, 250), (self.x, self.y), self.radius - 3)
        if ColliderBoxOn:
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius, 2)

    def hit(self, enemy, width, height):
        if (
            self.x >= enemy.x
            and self.y >= enemy.y
            and self.x <= enemy.x + width
            and self.y <= enemy.y + height
        ):
            return True
        return False


class Mana_orb(object):
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.tag = "MP"
        self.hitBox = pygame.Rect(self.x, self.y, 2, 2)

    def draw(self, screen):
        if ColliderBoxOn:
            pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)
        pygame.draw.circle(screen, (200, 200, 200), (self.x, self.y), 5)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 5, 1)

    def hit(self):
        if self.hitBox.colliderect(self.target.hitBox):
            return True
        return False


class HP_orb(object):
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.Cooldown = 2
        self.target = target
        self.hitBox = pygame.Rect(self.x, self.y, 2, 2)
        self.tag = "HP"

    def draw(self, screen):
        if ColliderBoxOn:
            pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 4)
        pygame.draw.circle(screen, (50, 50, 50), (self.x, self.y), 10)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 10, 2)

    def hit(self):
        if self.hitBox.colliderect(self.target.hitBox):
            return True
        return False


class shield(object):
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.Cooldown = 5
        self.hitBox = (x, y, 16, 92)

    def draw(self, screen):
        if self.direction == "right":
            self.hitBox = (self.x + 64, self.y, 16, 92)
            pygame.draw.ellipse(screen, (150, 150, 150), (self.x + 64, self.y, 16, 92))
        elif self.direction == "left":
            self.hitBox = (self.x - 16, self.y, 16, 92)
            pygame.draw.ellipse(screen, (150, 150, 150), (self.x - 16, self.y, 16, 92))
        elif self.direction == "up":
            self.hitBox = (self.x - 14, self.y - 16, 92, 16)
            pygame.draw.ellipse(
                screen, (150, 150, 150), (self.x - 14, self.y - 16, 92, 16)
            )
        elif self.direction == "down":
            self.hitBox = (self.x - 14, self.y + 94, 92, 16)
            pygame.draw.ellipse(
                screen, (150, 150, 150), (self.x - 14, self.y + 94, 92, 16)
            )
        pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)
