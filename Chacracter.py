import pygame, sys
from pygame.locals import *
from object.data import *
from Projectile import *
import random


def inRock(x, y):
    if x >= 35 and x <= 277 and y >= 89 and y <= 200:
        return True
    return False


class Player(object):
    def __init__(self):
        self.HP = 100
        self.MP = 100
        self.width = player_width
        self.height = player_height
        self.initSpawn()
        # print(self.x, self.y)
        self.initMove()
        self.initSkill()
        self.initCollider()

    def initSpawn(self):
        self.x = 35
        self.y = 200
        while inRock(self.x, self.y):
            self.x = random.randrange(0, WIDTH - 64)
            self.y = random.randrange(140, HEIGHT - 100)
        self.clone_x = self.x
        self.clone_y = self.y + 39

    def initSkill(self):
        self.Attacks = []
        self.Recover = []
        self.Cooldown = 0
        self.isAt = False
        self.AtCount = 0

    def initCollider(self):
        self.hitBox = pygame.Rect(self.x + 2, self.y, player_width - 4, player_height)
        self.isHit = 0

    def initMove(self):
        self.walk = False
        self.direction = "left"
        self.walkXCount = 0
        self.walkYCount = 0
        self.idleCount = 0
        self.jumpCount = 8
        self.isJump = False
        self.dashCooldown = 0
        self.dashDirection = "left"

    def dash(self):
        if self.dashCooldown == 0:
            self.dashCooldown = player_dashCooldown
            self.dashDirection = self.direction

    def move(self):
        keys = pygame.key.get_pressed()
        self.walk = False
        if keys[pygame.K_a] and self.dashCooldown == 0:
            self.dash()
        elif self.dashCooldown <= player_dashCooldown - 8:
            if keys[pygame.K_d]:
                if self.Cooldown == 0 and self.MP > 0 and self.direction != "":
                    self.isAt = True
                    self.Attacks.append(
                        Projectile(
                            round(self.x + self.width // 2),
                            round(self.y + self.height // 2),
                            self.direction,
                        )
                    )
                    self.Cooldown = 10
                    pygame.mixer.Channel(0).play(Sound_At)
            if keys[pygame.K_LEFT] and self.x > 0:
                self.walk = True
                self.direction = "left"
                self.x -= player_speed
                self.clone_x -= player_speed
                if inRock(self.x, self.y):
                    self.x += player_speed
                    self.clone_x += player_speed
            if keys[pygame.K_RIGHT] and self.x < WIDTH - 64:
                self.walk = True
                self.direction = "right"
                self.x += player_speed
                self.clone_x += player_speed
                if inRock(self.x, self.y):
                    self.x -= player_speed
                    self.clone_x -= player_speed
            if keys[pygame.K_UP] and self.y > 140:
                self.walk = True
                self.direction = "up"
                self.y -= player_speed
                self.clone_y -= player_speed
                if inRock(self.x, self.y):
                    self.y += player_speed
                    self.clone_y += player_speed
            if keys[pygame.K_DOWN] and self.y < HEIGHT - 100:
                self.walk = True
                self.direction = "down"
                self.y += player_speed
                self.clone_y += player_speed
            if not (self.isJump):
                if keys[pygame.K_SPACE]:
                    self.isJump = True
            else:
                if self.jumpCount >= -8:
                    self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
                    self.jumpCount -= 1
                else:
                    self.jumpCount = 8
                    self.isJump = False
                if self.y > 700:
                    self.y = 700
                    self.clone_y = 700

    def draw(self, screen):
        # Health Bar
        drawBar(screen)
        pygame.draw.rect(screen, (50, 50, 50), (0, 3, self.HP * 2, 20))
        pygame.draw.rect(screen, (128, 128, 128), (0, 25, self.MP * 2, 20))

        if self.dashCooldown <= 20:
            screen.blit(clone, (self.clone_x, self.clone_y))
            if not (self.isAt):
                if self.idleCount + 1 >= 48:
                    self.idleCount = 0
                if self.walkYCount + 1 >= 20:
                    self.walkYCount = 0
                if self.walkXCount + 1 >= 20:
                    self.walkXCount = 0
                if not (self.walk):
                    screen.blit(player_idle[self.idleCount // 12], (self.x, self.y))
                    self.idleCount += 1
                else:
                    if self.direction == "down":
                        screen.blit(
                            player_walkDown[self.walkYCount // 10], (self.x, self.y)
                        )
                        self.walkYCount += 1
                    elif self.direction == "up":
                        screen.blit(
                            player_walkUp[self.walkYCount // 10], (self.x, self.y)
                        )
                        self.walkYCount += 1
                    elif self.direction == "right":
                        screen.blit(
                            player_walkRight[self.walkXCount // 5], (self.x, self.y)
                        )
                        self.walkXCount += 1
                    elif self.direction == "left":
                        screen.blit(
                            player_walkLeft[self.walkXCount // 5], (self.x, self.y)
                        )
                        self.walkXCount += 1
            else:
                if self.direction == "left":
                    screen.blit(player_AttackAnimation[0], (self.x, self.y))
                if self.direction == "right":
                    screen.blit(player_AttackAnimation[1], (self.x, self.y))
                if self.direction == "up":
                    screen.blit(player_AttackAnimation[2], (self.x, self.y))
                if self.direction == "down":
                    screen.blit(player_AttackAnimation[3], (self.x, self.y))
                self.AtCount += 1

                if self.AtCount == 4:
                    self.isAt = False
                    self.AtCount = 0
        else:
            if self.dashDirection == "left":
                self.x -= player_speed * 3
                self.clone_x = self.x
                screen.blit(clone, (self.clone_x, self.clone_y))
                screen.blit(player_walkLeft[2], (self.x, self.y))
            elif self.dashDirection == "right":
                self.x += player_speed * 3
                self.clone_x = self.x
                screen.blit(clone, (self.clone_x, self.clone_y))
                screen.blit(player_walkRight[2], (self.x, self.y))
            elif self.dashDirection == "up":
                self.y -= player_speed * 3
                self.clone_y = self.y
                screen.blit(clone, (self.clone_x, self.clone_y))
                screen.blit(player_walkUp[1], (self.x, self.y))
            elif self.dashDirection == "down":
                self.y += player_speed * 3
                self.clone_y = self.y
                screen.blit(clone, (self.clone_x, self.clone_y))
                screen.blit(player_walkDown[1], (self.x, self.y))

        if self.isHit > 0:
            if self.isHit % 20 == 0:
                screen.blit(player_getHit, (self.x, self.y))
            self.isHit -= 1

        self.hitBox = pygame.Rect(self.x + 5, self.y, player_width - 10, player_height)
        if ColliderBoxOn:
            pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)

        for Bolt in self.Attacks:
            if Bolt.x < 1500 and Bolt.x > 0 and Bolt.y > 150 and Bolt.y < 800:
                if Bolt.direction == "left":
                    Bolt.x -= Bolt.speed
                elif Bolt.direction == "right":
                    Bolt.x += Bolt.speed
                elif Bolt.direction == "up":
                    Bolt.y -= Bolt.speed
                elif Bolt.direction == "down":
                    Bolt.y += Bolt.speed
            else:
                self.Attacks.pop(self.Attacks.index(Bolt))
        for Bolt in self.Attacks:
            Bolt.draw(screen)

        # Orb
        for orb in self.Recover:
            orb.draw(screen)
            if orb.hit():
                if self.MP < 100 and orb.tag == "MP":
                    self.MP += 1
                if orb.tag == "HP" and self.HP < 100:
                    self.HP += 2
                self.Recover.remove(orb)

        ScreenLimit(self)
        self.clone_x = self.x
        self.clone_y = self.y + 39
        if self.dashCooldown > 0:
            self.dashCooldown -= 1
        # Sound_Move.play()

    def Attack(self):
        keys = pygame.key.get_pressed()

    def getHit(self, dame):
        if self.isHit == 0:
            self.HP -= dame
            self.isHit = 40
            pygame.mixer.Channel(1).play(Sound_Hurt)

    def createManaOrb(self, x, y):
        self.Recover.append(
            Mana_orb(
                x + random.randrange(-10, 10) - 10,
                y + 64 + random.randrange(-5, 5),
                self,
            )
        )
        self.Recover.append(
            Mana_orb(
                x + random.randrange(-10, 10) + 10,
                y + 64 + random.randrange(-5, 5),
                self,
            )
        )
        self.Recover.append(
            Mana_orb(
                x + random.randrange(-10, 10) + 5,
                y + 64 + random.randrange(-5, 5) + 5,
                self,
            )
        )

    def createManaOrb(self, x, y):
        self.Recover.append(
            Mana_orb(
                x + random.randrange(-10, 10) - 10,
                y + 64 + random.randrange(-5, 5),
                self,
            )
        )
        self.Recover.append(
            Mana_orb(
                x + random.randrange(-10, 10) + 10,
                y + 64 + random.randrange(-5, 5),
                self,
            )
        )
        self.Recover.append(
            Mana_orb(
                x + random.randrange(-10, 10) + 5,
                y + 64 + random.randrange(-5, 5) + 5,
                self,
            )
        )

    def createHpOrb(self, x, y):
        self.Recover.append(HP_orb(x + 125, y + 250, self))
