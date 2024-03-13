import pygame, sys
from pygame.locals import *
from object.data import *
from Chacracter import *
from Boss import *
from Gameplay import *

pygame.init()
pygame.mixer.init()
g = GamePlay()

while g.running:
    g.checkEvent()
    g.running_Game()
    pygame.display.update()
    g.fpsClock.tick(FPS)
