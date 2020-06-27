import os

import pygame

pygame.init()

clock = pygame.time.Clock()

score = 0
sw = 800
sh= 500
win = pygame.display.set_mode((sw, sh))

walk_right = []
walk_left = []

dir = os.path.dirname(__file__)
filename = os.path.join(dir, 'media')
os.chdir(filename)

for i in range(1, 10):
    walk_right.append(pygame.image.load('R{}.png'.format(i)))

for k in range(1, 10):
    walk_left.append(pygame.image.load('L{}.png'.format(k)))
    print(k)

bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

bullet_sound = pygame.mixer.Sound("bullet.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

music = pygame.mixer.music.load("music.mp3")

os.chdir(dir)

# play music forever
pygame.mixer.music.play(-1)

class player(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
    
    def draw(self, win):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
        if not(self.standing):
            if self.left:
                win.blit(walk_left[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                win.blit(walk_right[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.right:
                win.blit(walk_right[0], (self.x, self.y))
            else:
                win.blit(walk_left[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)        

    def hit(self):
        print("jeff is hit")


class projectile(object):
    def __init__(self, x, y, r, color, facing,):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.facing = facing
        self.v = 8

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.r)

class enemy(object):

    os.chdir(filename)
    walk_right = []
    walk_left = []

    for o in range(1,12):
        walk_right.append(pygame.image.load('R{}E.png'.format(o)))
    
    for j in range(1,12):
        walk_left.append(pygame.image.load('L{}E.png'.format(j)))
        
    os.chdir(dir)

    def __init__(self, x, y, w, h, end):
        self.x = x
        self.y = y
        self.w = w 
        self.h = h
        self.end = end
        self.path = [self.x, self.end]
        self.walk_count = 0
        self.v = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57) 
        self.health = 10
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walk_count +1 >= 33:
                self.walk_count = 0
            
            if self.v > 0:
                win.blit(self.walk_right[self.walk_count //3], (self.x, self.y) )
                self.walk_count += 1
            else:
                win.blit(self.walk_left[self.walk_count //3], (self.x, self.y) )
                self.walk_count += 1
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)   
            pygame.draw.rect(win, (255, 0 ,0) , (self.hitbox[0], self.hitbox[1] - 20, 50, 10))  
            pygame.draw.rect(win, (0, 123, 0) , (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))    
        


    def move(self):
        if self.v > 0:
            if self.x  + self.v < self.path[1]:
                self.x += self.v 
            else:
                self.v = self.v * -1
                self.walk_count = 0
        else:
            if self.x - self.v > self.path[0]:
                self.x += self.v
            else:
                self.v = self.v * -1
                self.walk_count = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print("enemy is hit")


def redrawGameWin():
    win.blit(bg, (0,0))
    text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(text , (20, 20))
    jeff.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

# mainloop
font = pygame.font.SysFont('comicsans', 30, True)
bullets = []
goblin = enemy(100, 420, 64, 64, 700)
jeff = player(20,420, 64, 64)
shoot_loop = 0
run = True
while run:
    clock.tick(27)

    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 1:
        shoot_loop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    for bullet in bullets:
        if bullet.y - bullet.r < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.r > goblin.hitbox[1]:
            if bullet.x + bullet.r > goblin.hitbox[0] and bullet.x+ bullet.r < goblin.hitbox[0] + goblin.hitbox[2]:
                hit_sound.play()
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < sw and bullet.x > 0:
            bullet.x += bullet.v * facing
        else:
            bullets.pop(bullets.index(bullet))

    if jeff.y - jeff.h < goblin.hitbox[1] + goblin.hitbox[3] and jeff.y + jeff.h > goblin.hitbox[1]:
        if jeff.x + jeff.w > goblin.hitbox[0] and jeff.x + jeff.w < goblin.hitbox[0] + goblin.hitbox[2]:
            jeff.hit()

    if jeff.left:
        facing = -1
    else:
        facing = 1

    if keys[pygame.K_SPACE] and shoot_loop == 0:
       if len(bullets) < 5:
           bullet_sound.play()
           bullets.append(projectile(round(jeff.x + jeff.w // 2), round(jeff.y + jeff.h // 2), 5, (0,0,0), facing ))



    if keys[pygame.K_LEFT] and jeff.x > jeff.v:
        jeff.x -= jeff.v
        jeff.left = True
        jeff.right = False
        jeff.standing = False
    elif keys[pygame.K_RIGHT] and jeff.x < sw - jeff.w:
        jeff.x += jeff.v
        jeff.right = True
        jeff.left = False
        jeff.standing = False
    else:
        jeff.walk_count = 0
        jeff.standing = True

    if not(jeff.is_jump):
        if keys[pygame.K_UP] and jeff.is_jump is False:
            jeff.is_jump = True
            jeff.left = False
            jeff.right = False
    else:
        if jeff.jump_count >= -10:
            neg = 1
            if jeff.jump_count < 0:
                neg = -1
            jeff.y -= (jeff.jump_count ** 2) * 0.5 * neg
            jeff.jump_count -= 1
        else:
            jeff.is_jump = False
            jeff.jump_count = 10

    
    redrawGameWin()

pygame.quit
