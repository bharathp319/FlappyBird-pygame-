import os
import pygame
import time
import random
pygame.init()
black = (0, 0, 0)
bg = pygame.image.load("bg.jpg")
#bg = pygame.transform.scale(bg, (640, 300))
win = pygame.display.set_mode((960, 450))


fontname = pygame.font.match_font('time_new_roman')
font = pygame.font.Font(fontname, 40)
textsurface = font.render('Score:', True, (255, 255, 255))

score = 0

img_name = os.listdir("grumpy bird sprite sheets")
images = []
for imn in img_name:
    img = pygame.image.load(os.path.join("grumpy bird sprite sheets", imn))
    img = pygame.transform.scale(img, (60, 60))
    images.append(img)

background_last_update = pygame.time.get_ticks()
x1 = 0
x2 = 960
limit = x2
steps = 3
pause = False
def draw_background():
    global bg, background_last_update, win, x1, x2, limit, steps, score
    now = pygame.time.get_ticks()
    if now - background_last_update > 100:
        x1 -= steps
        x2 -= steps
        if x1 <=  -limit:
            x1 = limit
        if x2 <=  -limit:
            x2 = limit
    win.blit(bg, (x1, 0))
    win.blit(bg, (x2, 0))
    textsurface = font.render('Score: '+str(int(score)), True, (255, 255, 255))
    win.blit(textsurface,(50, 50))

def update_draw_window():
    global win, black, sprite_group
    win.fill(black)
    draw_background()
    sprite_group.update()
    sprite_group.draw(win)
    pygame.display.flip()


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.current_image = 0
        self.image = images[self.current_image]
        self.images = images
        self.radius = 22
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_update = pygame.time.get_ticks()

        self.isJumping = False
        self.initialJumpCount = 16
        self.jumpCount = self.initialJumpCount
        self.up = 1
        self.jumpIncrementTime = None
        
        
    def update(self):
        global  score
        now = pygame.time.get_ticks()
        if now - self.last_update  > 250:
            self.current_image += 1
            if len(self.images) <= (self.current_image):
                self.current_image = len(self.images) % (self.current_image)
            self.image = self.images[self.current_image]
            self.last_update = pygame.time.get_ticks()
            
        if self.isJumping and (now - self.jumpIncrementTime > 15):
            self.jumpIncrementTime = now
            if self.jumpCount < 0:
                self.isJumping = False
                self.up = 1
                self.jumpCount = self.initialJumpCount
            self.rect.y += self.up * self.jumpCount
            self.jumpCount -= 1
        if not self.isJumping:
            self.rect.y += int(self.up * (self.jumpCount ** 0.5))
            if self.jumpCount < self.initialJumpCount:
                self.jumpCount += 1
        if (self.rect.top <= 0) or self.rect.bottom >= 450:
            self.rect.x = 300
            self.rect.y = 100
            sprite_group.remove(pipe_group)
            pipe_group.empty()
            score = 0
            time.sleep(1)
            
    def jump(self):
        if not self.isJumping:
            self.jumpCount = self.initialJumpCount
            self.isJumping = True
            self.up = -1
            self.jumpIncrementTime  = pygame.time.get_ticks()
        if self.isJumping:
            self.up = -1
            self.jumpCount = self.initialJumpCount
        

class Pipe(pygame.sprite.Sprite):
    def __init__(self, h, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, h))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 960
        self.rect.y = y

        self.passed = False
    def update(self):
        global score
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()
        if (self.rect.right < bird.rect.x) and (not self.passed) :
            score += 0.5
            self.passed = True
            
        
sprite_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
bird = Bird(300, 100, images)
sprite_group.add(bird)

update_draw_window()
time.sleep(5)

run = True
last_pipe = pygame.time.get_ticks()

def create_pipe():
    global sprite_group, pipe_group
    height1 = random.choice(range(50, 200))
    # height2 = 450  - height1
    #height1 = 150
    y2 = height1 + 175
    pipe1 = Pipe(height1, 0)
    pipe2 = Pipe(300, y2)
    sprite_group.add(pipe1)
    sprite_group.add(pipe2)
    pipe_group.add(pipe1)
    pipe_group.add(pipe2)

while run:
    now = pygame.time.get_ticks()
    if (now - last_pipe > 1500) & (not pause):
        create_pipe()
        last_pipe = now
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE) & (not pause):
                bird.jump()
            elif (event.key == pygame.K_p) & (not pause):
                pause = True
            elif (event.key == pygame.K_p) & (pause):
                pause = False
                last_pipe = pygame.time.get_ticks()
    hits = pygame.sprite.spritecollide(bird, pipe_group, False)
    if hits:
        bird.kill()
        bird = Bird(300, 100, images)
        sprite_group.remove(pipe_group)
        pipe_group.empty()
        sprite_group.add(bird)
        score = 0
        time.sleep(1)
    if not pause:
        update_draw_window()
pygame.quit()
