import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'graphics')
snd_dir = path.join(path.dirname(__file__), 'sounds')
#HS_dir = path.join(path.dirname(__file__), 'highscore')
#HS_FILE = "highscore space shoot.txt"


width = 500
length = 800
fps = 55
POWERUP_TIME = 5000
#highscore = 0

green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 255, 255)
yellow = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, length))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, green, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)
    
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (100, 78))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, yellow, self.rect.center, self.radius)
        self.rect.centerx = width/2
        self.rect.bottom = length - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 300
        self.last_shot = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        

    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

            
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        
        self.rect.x +=self.speedx
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
        

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now 
            if self.power == 1:
                bullet = Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
                
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left,self.rect.centery)
                bullet2 = Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
                
            
    
class mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(meteor_img, (50, 50))
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius1 = int(self.rect.width/3)
        #pygame.draw.circle(self.image_orig, red, self.rect.center, self.radius1)
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 9)
        self.speedx = random.randrange(-4, 4)
       
        self.rot = 0
        self.rot_speed = random.randrange(-7, 7)
        self.last_update = pygame.time.get_ticks()
        
        
    def rotate(self):
        now = pygame.time.get_ticks()
        if now- self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > length + 10 or self.rect.left < -25 or self.rect.right > width + 25:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
        
           
            



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 40))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['gun', 'shield'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

    #def load_data():
       # dir = path.dirname(__file__)
       # with open(path.join(dir, HS_FILE), 'w') as f:
         #   try:
          #      highscore = int(f.read())
           # except:
            #    highscore = 0

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
            
background = pygame.image.load(path.join(img_dir, "stars.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "space_ship.png")).convert()
meteor_img = pygame.image.load(path.join(img_dir, "meteor.png")).convert()

intro_music = pygame.mixer.music.load(path.join(snd_dir, 'intro space'))
pygame.mixer.music.set_volume(1.3)



explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(8):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
powerup_images = {}
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()

font_name2 = pygame.font.match_font("arial")
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'laser_sound.wav'))
expl_sounds = []
for snd in ['Explosion_1', 'Explosion_2']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
powerup_sound = pygame.mixer.Sound(path.join(snd_dir, 'powerup_sound'))

pygame.mixer.music.play(loops=-1)

def game_intro():
        
    draw_text(screen, "Space Shooter!", 72, width/2, length / 4)
    draw_text(screen, "Space bar to shoot Arrow keys to move!", 22, width/2, length / 2)
    draw_text(screen, "Press any key to begin", 18, width/2, length * 3/4)
   # draw_text(screen, "High Score: " + str(highscore), 22, width/2, length / 3)
    
    pygame.display.flip()
    # self.load_data()
    waiting = True
    
    while waiting:
        
       
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


    

            



game_over = True

running = True
while running:
    if game_over:
        game_intro()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        player = Player()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        

        all_sprites.add(player)
        for i in range(10):
            newmob()   
        score = 0
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
     

    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 3
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

   

    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'gun':
            player.powerup()
            powerup_sound.play()
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            powerup_sound.play()
            if player.shield >= 100:
                player.shield = 100
            

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= random.randrange(5, 25)
        expl = Explosion(hit.rect.center, 'lg')
        random.choice(expl_sounds).play()
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            clock.tick(2)
            game_over = True
    



    screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, width / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
   
    pygame.display.flip()

pygame.quit()
    
