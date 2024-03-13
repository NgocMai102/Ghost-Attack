import pygame, sys
from pygame.locals import *
from object.data import *
from Chacracter import *
from Boss import *
from MenuUI import *

pygame.init()
pygame.mixer.init()


def run(runfile):
    with open(runfile, "r") as rnf:
        exec(rnf.read())


class GamePlay:
    def __init__(self):
        self.checkEvent()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        self.fpsClock = pygame.time.Clock()
        self.running = True
        self.Ghost = Player()
        self.sBoss = Boss(1300, 200, self.Ghost)
        self.text_surface = readyFont.render("READY?", False, (0, 0, 0))
        self.pre_time = 60
        self.help = True
        self.music = pygame.mixer.music.load("Sound\BG.wav")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)
        self.win = False
        self.lost = False

    def pause(self):
        pause = True
        while pause:
            self.screen.blit(pygame.image.load("Img\Pause.png"), (0, 0))
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, 1540, 800), 2)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and pygame.QUIT:
                    pause = False

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

        self.fpsClock.tick(FPS)

    def running_Game(self):
        self.screen.blit(background, (0, 0))
        if self.Ghost.HP > 0 and self.sBoss.HP > 0:
            if self.pre_time == 0:
                if self.Ghost.Cooldown > 0:
                    self.Ghost.Cooldown -= 1
                if self.sBoss.hit():
                    self.Ghost.getHit(10)
                self.Ghost.move()
                self.Ghost.draw(self.screen)

                for At in self.Ghost.Attacks:
                    if At.hit(self.sBoss, 230, 250):
                        if isinstance(At, Projectile):
                            self.sBoss.getHit(At.dame)
                        self.Ghost.Attacks.remove(At)
                    else:
                        for Atb in self.sBoss.Attacks:
                            if At.hit(Atb, 64, 64):
                                self.Ghost.createManaOrb(Atb.x, Atb.y)
                                self.sBoss.Attacks.remove(Atb)
                                self.Ghost.Attacks.remove(At)
                if self.sBoss.HP == 50 and self.help == True:
                    self.Ghost.createHpOrb(self.sBoss.x, self.sBoss.y)
                    self.help = False
                self.sBoss.Attack(self.Ghost)
                self.sBoss.draw(self.screen)
                for Atb in self.sBoss.Attacks:
                    if Atb.hit():
                        self.Ghost.getHit(Atb.dame)
                        self.sBoss.Attacks.remove(Atb)
            else:
                self.Ghost.draw(self.screen)
                self.sBoss.draw(self.screen)
                if self.pre_time > 30:
                    self.screen.blit(self.text_surface, (400, 250))
                else:
                    self.text_surface = readyFont.render("FIGHT!", False, (0, 0, 0))
                    self.screen.blit(self.text_surface, (400, 250))
                self.pre_time = self.pre_time - 1
        else:
            pygame.mixer.music.stop()
            if self.Ghost.HP <= 0:
                self.screen.blit(lose, (0, 0))
                self.lost = True
                self.win = False
            if self.sBoss.HP <= 0:
                self.screen.blit(win, (0, 0))
                self.win = True
                self.lost = False
            self.replay = pygame.font.Font(fontGame, 40)
            self.replay = self.replay.render("Press Enter to replay", False, (0, 0, 0))
            self.screen.blit(self.replay, (550, 650))
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 1)

    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.win or self.lost:
                    run("StartScene.py")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.pause()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
