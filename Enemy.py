import pygame, sys
import math
from pygame.locals import *
from Projectile import *


class skull(object):
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.initProperty()
        pygame.mixer.Channel(4).play(SkuSound)

    def initProperty(self):
        self.width = skull_width
        self.height = skull_height
        self.dame = skull_dame
        self.speed = skull_speed
        self.hitBox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        if self.x < self.target.x:
            self.x += min(self.speed, abs(self.x - self.target.x))
        else:
            self.x -= min(self.speed, abs(self.x - self.target.x))
        if self.y < self.target.y - 7:
            self.y += min(self.speed, abs(self.y - self.target.y + 10))
        else:
            self.y -= min(self.speed, abs(self.y - self.target.y + 10))
        screen.blit(SkuImg, (self.x, self.y))
        self.hitBox = pygame.Rect(self.x, self.y, self.width, self.height)
        if ColliderBoxOn:
            pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)

    def hit(self):
        if self.hitBox.colliderect(self.target.hitBox):
            return True
        return False


class floating_skull(object):
    def __init__(self, target, player, number):
        self.alpha = 0
        self.target = target
        self.player = player
        self.number = number
        self.initProperty(self.target)
        pygame.mixer.Channel(4).play(SkuSound)

    def initProperty(self, target):
        self.x = target.x
        self.y = target.y
        self.width = skull_width
        self.height = skull_height
        self.dame = skull_dame
        self.radius = floating_skull_radius
        self.hitBox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        self.alpha += 0.1
        if self.alpha >= 360:
            self.alpha = 0

        self.x = (
            self.target.x + 90 - self.radius * math.cos(self.alpha + self.number * 80)
        )
        self.y = (
            self.target.y + 95 - self.radius * math.sin(self.alpha + self.number * 80)
        )

        screen.blit(SkuImg, (self.x, self.y))

        ScreenLimit(self)

        self.hitBox = pygame.Rect(self.x, self.y, self.width, self.height)
        if ColliderBoxOn:
            pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)

    def hit(self):
        if self.hitBox.colliderect(self.player.hitBox):
            return True
        return False


class Ske_hand(object):
    def __init__(self, x, y, facing, target):
        self.x = x
        self.y = y
        self.target = target
        self.facing = facing
        self.hitBox = pygame.Rect(self.x, self.y, 34, 120)
        self.initProperty()

    def initProperty(self):
        self.speed = ske_hand_speed
        self.rotate = ske_hand_rotate
        self.dame = ske_hand_dame

    def draw(self, screen):
        self.x += 8 * self.facing
        self.rotate += 90
        if self.rotate >= 360:
            self.rotate = 0
        if self.rotate == 0:
            screen.blit(SkehandImg, (self.x, self.y - 60))
            self.hitBox = pygame.Rect(self.x, self.y - 60, 34, 120)
        if self.rotate == 90:
            screen.blit(
                (pygame.transform.rotate(SkehandImg, -90)), (self.x - 60, self.y - 17)
            )
            self.hitBox = pygame.Rect(self.x - 60, self.y - 17, 120, 34)
        if self.rotate == 180:
            screen.blit(
                pygame.transform.flip(SkehandImg, True, True), (self.x, self.y - 60)
            )
            self.hitBox = pygame.Rect(self.x, self.y - 60, 34, 120)
        if self.rotate == 270:
            screen.blit(
                (pygame.transform.rotate(SkehandImg, 90)), (self.x - 30, self.y - 7)
            )
            self.hitBox = pygame.Rect(self.x - 30, self.y - 7, 120, 34)

        if ColliderBoxOn:
            pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)

    def hit(self):
        if self.hitBox.colliderect(self.target.hitBox):
            return True
        return False
