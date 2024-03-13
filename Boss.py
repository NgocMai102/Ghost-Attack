import random
import pygame, sys
from pygame.locals import *
from object.data import *
from Projectile import *
from Enemy import *

pygame.init()
pygame.mixer.init()


class Boss(object):
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.shadow_x = x
        self.shadow_y = y + 250
        self.target = target
        self.HP = boss_HP
        self.isHit = 0
        self.initProperty()
        self.initAttack()

    def initProperty(self):
        self.floatCount = 0
        self.width = boss_width
        self.height = boss_height
        self.facing = boss_facing
        self.hitBox = pygame.Rect(self.x + 10, self.y, self.width - 20, self.height)

    def initAttack(self):
        self.Attacks = []
        self.Cooldown = 0
        self.Acskill = False

        # Skill 1
        self.s1_ac = 0
        self.s1_cd = 0
        self.s1_sp = 0
        # Skill 2
        self.s2_cd = 0
        # Skill 3
        self.s3_cd = 0

    def draw(self, screen):
        if self.Cooldown > 0:
            self.Cooldown -= 1
        if self.s1_cd > 0:
            self.s1_cd -= 1
        if self.s2_cd > 0:
            self.s2_cd -= 1
        if self.s3_cd > 0:
            self.s3_cd -= 1
        if not (self.Acskill):
            if self.floatCount >= -1:
                self.y -= (self.floatCount * abs(self.floatCount)) * 0.5
                self.floatCount -= 0.1
            else:
                self.floatCount = 1

            if self.isHit > 0:
                screen.blit(Boss_getHit, (self.x, self.y))
                self.isHit -= 1
            else:
                screen.blit(Boss_img, (self.x, self.y))
        else:
            if self.s1_ac > 0:
                if self.s1_ac > 30:
                    if self.y + 250 != self.target.y + 92:
                        if self.y + 250 > self.target.y + 92:
                            self.y -= self.s1_sp
                        else:
                            self.y += self.s1_sp
                    screen.blit(Boss_img, (self.x, self.y))
                elif self.s1_ac > 25:
                    screen.blit(Boss_s1Ac, (self.x, self.y))
                else:
                    # Skill1Sound.play()
                    self.x += 30 * self.facing
                    if self.facing == -1:
                        screen.blit(Boss_side, (self.x, self.y))
                    else:
                        screen.blit(
                            pygame.transform.flip(Boss_side, True, False),
                            (self.x, self.y),
                        )
                self.s1_ac -= 1
            else:
                self.Acskill = False
        self.shadow_x = self.x
        self.shadow_y = self.y + 250

        for At in self.Attacks:
            At.draw(screen)

        ScreenLimit(self)
        screen.blit(Boss_shadow, (self.shadow_x, self.shadow_y))

        pygame.draw.rect(screen, (10, 10, 10), (1480, 200, 50, 100 * 5 + 4))
        pygame.draw.rect(
            screen,
            (200, 200, 200),
            (1480 + 2, 200 + 2 + (100 - self.HP) * 5, 50 - 4, self.HP * 5),
        )

        self.hitBox = pygame.Rect(self.x + 10, self.y, 230, 250)
        if ColliderBoxOn:
            pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)

    def getHit(self, dame):
        pygame.mixer.Channel(2).play(Boss_sound_hurt)
        self.HP -= dame
        self.isHit = 2

    def hit(self):
        if self.hitBox.colliderect(self.target.hitBox):
            return True
        return False

    def Attack(self, Player):
        if self.s1_cd == 0:
            self.skill1()
            self.s1_cd = 120

        if self.s2_cd == 0 and self.HP < 30:
            self.skill3()
            self.s2_cd = 50

        if self.Cooldown == 0:
            self.Attacks.append(skull(self.x, self.y, Player))
            self.Cooldown = 100

        if self.s3_cd == 0 and self.HP < 60:
            self.skill2()
            self.s3_cd = 150

    def skill1(self):
        if self.x - self.target.x > 0:
            self.facing = -1
        else:
            self.facing = 1
        pygame.mixer.Channel(1).play(SkillSound1)
        self.s1_sp = abs(self.target.y + 92 - self.y - 250) / 10
        self.s1_ac = 40
        self.Acskill = True
        self.s1_cd = 10

    def skill3(self):
        x = random.randrange(-100, 100)
        if self.facing == 1:
            self.Attacks.append(Ske_hand(0, 200 + x, 1, self.target))
            self.Attacks.append(Ske_hand(100, 450 + x, 1, self.target))
            self.Attacks.append(Ske_hand(0, 700 + x, 1, self.target))
        else:
            self.Attacks.append(Ske_hand(1500, 200 + x, -1, self.target))
            self.Attacks.append(Ske_hand(1400, 450 + x, -1, self.target))
            self.Attacks.append(Ske_hand(1300, 700 + x, -1, self.target))

    def skill2(self):
        self.Attacks.clear()
        self.Attacks.append(floating_skull(self, self.target, 0))
        self.Attacks.append(floating_skull(self, self.target, 1))
        self.Attacks.append(floating_skull(self, self.target, 2))
        self.Attacks.append(floating_skull(self, self.target, 3))
