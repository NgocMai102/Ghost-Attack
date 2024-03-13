import pygame, sys

pygame.font.init()
pygame.mixer.init()

# constants
HEIGHT = 800
WIDTH = 1540
FPS = 30

# background
background = pygame.image.load("Img\Background.png")
backgroundMenu = pygame.image.load("ImgMenu\Background.png")

# UI
lose = pygame.image.load("Img\Lose.png")
lose = pygame.transform.scale(lose, (WIDTH, HEIGHT))

icon = pygame.image.load("Img\Icon.png")
win = pygame.image.load("Img\Win.png")
win = pygame.transform.scale(win, (WIDTH, HEIGHT))

MenuTutorial = pygame.image.load("imgMenu\Tutorial.png")

# font
readyFont = pygame.font.SysFont("Comic Sans MS", 200)
fontGame = "BRITANIC.TTF"
# sound----------------------------------------------
Sound_At = pygame.mixer.Sound("Sound\main_attack.wav")
Sound_At.set_volume(0.2)

Sound_Move = pygame.mixer.Sound("Sound\main_move_glass.wav")
Sound_Move.set_volume(0.3)

Sound_Hurt = pygame.mixer.Sound("Sound\main_hurt.wav")
Sound_Hurt.set_volume(0.2)
# ---------------------------------------------------

# clone
clone = pygame.image.load("Img\Clone.png")

# player
player_speed = 8
player_width = 64
player_height = 92
player_dashCooldown = 28

player_bulletColor = (50, 50, 50)
player_bulletRadius = 15
player_bulletSpeed = 30
player_bulletDamage = 3

player_idle = [
    pygame.image.load("Img\Player\Idle\Idle_1.png"),
    pygame.image.load("Img\Player\Idle\Idle_2.png"),
    pygame.image.load("Img\Player\Idle\Idle_1.png"),
    pygame.image.load("Img\Player\Idle\Idle_4.png"),
]

player_walkDown = [
    pygame.image.load("Img\Player\WalkDown\WalkDown_1.png"),
    pygame.image.load("Img\Player\WalkDown\WalkDown_2.png"),
]

player_walkUp = [
    pygame.image.load("Img\Player\WalkUp\WalkUp_1.png"),
    pygame.image.load("Img\Player\WalkUp\WalkUp_2.png"),
]

player_walkLeft = [
    pygame.image.load("Img\Player\WalkLeft\WalkLeft_1.png"),
    pygame.image.load("Img\Player\WalkLeft\WalkLeft_2.png"),
    pygame.image.load("Img\Player\WalkLeft\WalkLeft_3.png"),
    pygame.image.load("Img\Player\WalkLeft\WalkLeft_1.png"),
]

player_walkRight = [
    pygame.image.load("Img\Player\WalkRight\WalkRight_1.png"),
    pygame.image.load("Img\Player\WalkRight\WalkRight_2.png"),
    pygame.image.load("Img\Player\WalkRight\WalkRight_3.png"),
    pygame.image.load("Img\Player\WalkRight\WalkRight_1.png"),
]

player_AttackAnimation = [
    pygame.image.load("Img\Player\AttackLeft.png"),
    pygame.image.load("Img\Player\AttackRight.png"),
    pygame.image.load("Img\Player\AttackUp.png"),
    pygame.image.load("Img\Player\AttackDown.png"),
]

player_getHit = pygame.image.load("Img\Player\Player_getHit.png")

# Enemy
skull_width = 64
skull_height = 64
skull_speed = 3
skull_dame = 5

floating_skull_radius = 160

ske_hand_speed = 8
ske_hand_rotate = 0
ske_hand_dame = 3

ShieldImg = pygame.image.load("Img\Shield.png")
SkeImg = pygame.image.load("Img\Ske.png")
SkeImg = pygame.transform.scale(SkeImg, (64, 102))
SkuImg = pygame.image.load("Img\Skull.png")
SkehandImg = pygame.image.load("Img\Ske_hand.png")

SkuSound = pygame.mixer.Sound("Sound\laugh.wav")
SkuSound.set_volume(1)

# Boss
boss_width = 250
boss_height = 250
boss_HP = 100
boss_facing = -1

Boss_img = pygame.image.load("Img\Boss\Boss.png")
Boss_img = pygame.transform.scale(Boss_img, (250, 250))

Boss_getHit = pygame.image.load("Img\Boss\Boss_getHit.png")
Boss_getHit = pygame.transform.scale(Boss_getHit, (250, 250))

Boss_shadow = pygame.image.load("Img\Boss\Boss_shadow.png")
Boss_shadow = pygame.transform.scale(Boss_shadow, (230, 250 / 6))

Boss_side = pygame.image.load("Img\Boss\Boss_side.png")
Boss_side = pygame.transform.scale(Boss_side, (250, 250))

Boss_s1Ac = pygame.image.load("Img\Boss\Boss_s1Ac.png")
Boss_s1Ac = pygame.transform.scale(Boss_s1Ac, (250, 250))

SkillSound1 = pygame.mixer.Sound("Sound\Boss_Skill1.wav")
SkillSound1.set_volume(0.5)
Boss_sound_hurt = pygame.mixer.Sound("Sound\Boss_hurt.wav")
Boss_sound_hurt.set_volume(0.6)
