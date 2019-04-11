# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH =  900
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
TITLE = "What's New Pussycat?"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 20, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (244, 215, 66)
GREEN = (86, 181, 85)


# Fonts
FONT_SM = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 24)
FONT_MD = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 32)
FONT_LG = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 55)
FONT_XL = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 65)


# Images
ship_img = pygame.image.load('assets/images/jukebox.png').convert_alpha()
laser_img = pygame.image.load('assets/images/goodlaser.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/goodcat.png').convert_alpha()
background_img = pygame.image.load('assets/images/background.png').convert()
enemy2_img = pygame.image.load('assets/images/inutj.png').convert_alpha()
enemy3_img = pygame.image.load('assets/images/wnptj.png').convert_alpha()
title_img = pygame.image.load('assets/images/title.png').convert()
lose_img = pygame.image.load('assets/images/lose.png').convert()
win_img = pygame.image.load('assets/images/win.png').convert()
powerup1_img = pygame.image.load('assets/images/powerup1.png').convert_alpha()
hit1_img = pygame.image.load('assets/images/jukeboxdamage1.png').convert_alpha()
hit2_img = pygame.image.load('assets/images/jukeboxgameover.png').convert_alpha()


# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
CAT = pygame.mixer.Sound('assets/sounds/cat.ogg')
NOTE = pygame.mixer.Sound('assets/sounds/note.ogg')
WIN_SND = pygame.mixer.Sound('assets/sounds/win.ogg')
LOSE_SND = pygame.mixer.Sound('assets/sounds/lose.ogg')
TITLE = pygame.mixer.Sound('assets/sounds/title.ogg')


# Stages
START = 0
PLAYING = 1
WIN = 2
LOSE = 3


# Game classes    
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 3
        self.health = 3


    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def shoot(self):
        print("Pew!")

        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

        NOTE.play()

    def change_image(self):
        if self.health == 3:
            self.image = ship_img
            
        if self.health == 2:
            self.image = hit1_img

        if self.health == 1:
            self.image = hit2_img
            
    def update(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        hit_list = pygame.sprite.spritecollide(self, powerups, True,
                                               pygame.sprite.collide_mask)

        for hit in hit_list:
            print("Yee yee")
            hit.apply(self)

        hit_list = pygame.sprite.spritecollide(self, bombs, True,
                                               pygame.sprite.collide_mask)

        for hit in hit_list:
            print("Oof!")
            self.health -=1

        self.change_image()
            
        if self.health == 0:
            self.kill()

    
class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        print("Bwwamp!")

        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            EXPLOSION.play()
            player.score += 1
            print("Boom!")
            self.kill()
            

class HealthPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def apply(self, ship):
        ship.health = 3
        

    def update(self):
        self.rect.y += self.speed

        if self.rect.bottom > HEIGHT:
            self.kill()


class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.speed = 5
        CAT.play()

    def update(self):
        self.rect.y += self.speed

        if self.rect.bottom > HEIGHT:
            self.kill()
    

class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 3
        self.drop = 20
        self.moving_right = True
        self.drop_speed = 1
        self.bomb_rate = 20

    def move(self):
        hits_edge = False

        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True

            else:
                m.rect.x -= self.speed

                if m.rect.left <=0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            self.move_down()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop


    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def update(self):
        self.move()
        self.choose_bomber()


# Game helper functions
def show_title_screen():
    TITLE.play()
    screen.blit(title_img, [0,0])
    title_text = FONT_XL.render("What's New Pussycat?", 1, GREEN)
    screen.blit(title_text, [50, 0])
    title2_text = FONT_MD.render("Inspired by John Mulaney's Salt and Pepper Diner.", 1, GREEN)
    screen.blit(title2_text, [0, 600])
    title3_text = FONT_XL.render("Press SPACE to play", 1, GREEN)
    screen.blit(title3_text, [60, 500])
    
    

def show_lose_screen():
    LOSE_SND.play()
    screen.blit(lose_img, [0, 0])
    lose_text = FONT_XL.render(" ! ! ! H a  H a  L o s e r ! ! ! ", 1, RED)
    screen.blit(lose_text, [0, 75])
    lose2_text = FONT_XL.render("Press SPACE to restart", 1, RED)
    screen.blit(lose2_text, [10, 600])

def show_win_screen():
    WIN_SND.play()
    screen.blit(win_img, [0, 0])
    win_text = FONT_LG.render("Congratulations! You Win!", 1, YELLOW)
    screen.blit(win_text, [50, 75])
    win2_text = FONT_LG.render("Press SPACE to play again", 1, YELLOW)
    screen.blit(win2_text, [50, 600])
    

def display_statistics():
    score_text = FONT_MD.render(str(player.score), 1, WHITE)
    screen.blit(score_text, [850, 20])
    if player.score == 21:
        show_win_screen()

 
def check_end():
    global stage

    if len(mobs) == 0:
        stage = WIN
    elif len(player) == 0:
        stage = LOSE

def setup():
    global stage, done, player, ship, lasers, mobs, fleet, bombs, powerups
    
    ''' Make game objects '''
    ship = Ship(384, 536, ship_img)

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    mob1 = Mob(100, 200, enemy3_img)
    mob2 = Mob(300, 200, enemy3_img)
    mob3 = Mob(500, 200, enemy3_img)
    mob4 = Mob(700, 200, enemy3_img)
    mob5 = Mob(200, 200, enemy3_img)
    mob6 = Mob(400, 200, enemy3_img)
    mob7 = Mob(600, 200, enemy3_img)
    mob8 = Mob(150, 100, enemy3_img)
    mob9 = Mob(100, 0, enemy3_img)
    mob10 = Mob(200, 0, enemy3_img)
    mob11 = Mob(300, 0, enemy3_img)
    mob12 = Mob(250, 100, enemy3_img)
    mob13 = Mob(350, 100, enemy3_img)
    mob14 = Mob(450, 100, enemy3_img)
    mob15 = Mob(550, 100, enemy3_img)
    mob16 = Mob(650, 100, enemy3_img)
    mob17 = Mob(300, 0, enemy3_img)
    mob18 = Mob(500, 0, enemy3_img)
    mob19 = Mob(600, 0, enemy3_img)
    mob20 = Mob(700, 0, enemy3_img)
    mob21 = Mob(400, 0, enemy2_img)
    
    
    

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10, mob11, mob12, mob13, mob14, mob15, mob16, mob17, mob18, mob19, mob20, mob21)

    powerup1 = HealthPowerUp(200, -2000, powerup1_img)
    powerups = pygame.sprite.Group()
    powerups.add(powerup1)

    fleet = Fleet(mobs)

    ''' set stage '''
    stage = START
   

    
# Game loop
setup()
done = False

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif event.key == pygame.K_SPACE:
                if event.key == pygame.K_SPACE:
                    ship.shoot()

            if stage == PLAYING:
                pass

            if stage == WIN or stage == LOSE:
                print(stage)
                if event.key == pygame.K_SPACE:
                    setup()

    pressed = pygame.key.get_pressed()
    

        
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
       if pressed[pygame.K_LEFT]:
           ship.move_left()
       elif pressed[pygame.K_RIGHT]:
           ship.move_right()

       if pressed[pygame.K_UP]:
            ship.move_up()
       elif pressed[pygame.K_DOWN]:
           ship.move_down()

       player.update()
       lasers.update()
       bombs.update()
       fleet.update()
       mobs.update()
       powerups.update()

       check_end()
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.blit(background_img, [0,0])
    lasers.draw(screen)
    bombs.draw(screen)
    player.draw(screen)
    mobs.draw(screen)
    powerups.draw(screen)
    display_statistics()
    

   
    if stage == START:
        show_title_screen()
    elif stage == WIN:
        show_win_screen()
    elif stage == LOSE:
        show_lose_screen()

        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()
    

    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
