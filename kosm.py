from typing import Any
from pygame import*
from random import randint

mixer.init()
font.init()

window = display.set_mode((700,500))
display.set_caption("Шутер")

img_back = "photo_2023-12-17_19-34-30.jpg"
img_hero = "photo_2023-12-17_19-34-59-removebg-preview.png"
img_enemy = "photo_2023-12-17_19-30-20-removebg-preview.png"
img_bullet = "photo_2023-12-17_19-30-18-removebg-preview.png"
img_astr = "photo_2023-12-17_19-30-290-removebg-preview.png"
img_boss = "pngwing.com.png"
img_hp="hp.png"
img_bosbul="bosbul.png"

font1 = font.SysFont('Arial',80)
font2=font.SysFont('Arial', 36)
win = font1.render('YOU WIN!', True, (255,255,255))
lose = font1.render('YOU LOSE!', True, (180,0,0))
score = 0
lost=0
max_lost=3
goal=5
hp=0
last_shoot_time = 0  
shoot_delay = 1000

class GameSprite(sprite.Sprite):
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        #кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet= Bullet(img_bullet, ship.rect.centerx, ship.rect.top, 15,20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost = lost + 1
       
class Astr(GameSprite):
    def update(self):
        self.rect.y += self.speed

class Bullet(GameSprite):
    def update(self):
        self.rect.y -=self.speed
        if self.rect.y < 0:
            self.kill()
        global score
        global hp
        if self.rect.colliderect(Boss):
            score = score +1 
            hp = hp - 70
            self.kill()

class B_Bullet(GameSprite): 
    def update(self):
        self.rect.y +=self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 100
            


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")

background = transform.scale(image.load(img_back),(win_width, win_height))
ship = Player(img_hero, 5, win_height-100,80,100,10)
Boss = GameSprite(img_boss, 30, -400,650,400,5)
Boss_hp=GameSprite(img_hp,hp,0,700,30,0)


monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width-80), -40,80,50, randint(1,5))
    monsters.add(monster)

asteroids = sprite.Group()
for h in range(1, 4):
    asteroid = Astr(img_astr, randint(80, win_width-80), -40,80,50, randint(1,5))
    asteroids.add(asteroid)   

bullets = sprite.Group()

Boss_Bullets = sprite.Group()
for p in range(1, 10):
    Boss_Bullet = B_Bullet(img_bosbul, randint(80, win_width-80), 100,20,50, randint(1,7))
    Boss_Bullets.add(Boss_Bullet)

finish= False
finish1=False
finish2=False
run = True
clock = time.Clock()
FPS=60

mixer.music.load("space.ogg")
mixer.music.set_volume(0.1) 
mixer.music.play(-1)
fire_sound = mixer.Sound('fire.ogg')

while run:
    
    for e in event.get():
        if e.type == QUIT:
            run= False
        elif e.type == KEYDOWN:
            if e.key==K_SPACE:
                fire_sound.play()
                current_time = time.get_ticks()  # получаем текущее время в миллисекундах
                if current_time - last_shoot_time >= shoot_delay:
                    fire_sound.play()
                    ship.fire()
                    last_shoot_time = current_time

    if not finish:
        window.blit(background, (0,0))

        text = font2.render("Рахунок: " + str(score), 1, (255,255,255))
        window.blit(text,(10,20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10, 50))

        ship.update()
        bullets.update()
        monsters.update()
        asteroids.update()

        ship.reset()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True,True)
        for c in collides:
            score = score +1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40,80,50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship,monsters,False) or lost >=max_lost:
            finish = True
            finish1=True
            finish2=True
            window.blit(lose,(200,200))

        if sprite.spritecollide(ship,asteroids,False) or lost >=max_lost:
            finish = True
            finish1=True
            finish2=True
            window.blit(lose,(200,200))
        
        if score>=goal:
            finish=True
        
        if lost==4:
            finish = True
            finish1=True
            finish2=True
            window.blit(lose,(200,200))

        display.update()

    if finish and not finish1:
        window.blit(background, (0,0))
        Boss.reset()

        if Boss.rect.y< -150:
            Boss.rect.y += 5

        if Boss.rect.y==-150:
            finish1=True
        
        ship.reset()

        display.update()

    if finish and finish1 and not finish2:
        window.blit(background, (0,0))

        text = font2.render("Рахунок: " + str(score), 1, (255,255,255))
        window.blit(text,(10,20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10, 50))
            
            
        Boss_hp.update()    
        Boss_Bullets.update()
        ship.update()
        bullets.update()
        Boss.reset()

        Boss_hp.rect.x = hp
        Boss_hp.reset()
        ship.reset()
        bullets.draw(window)
        Boss_Bullets.draw(window)

        if hp<=-700:
            finish2 = True
            window.blit(win,(200,200))

        if sprite.spritecollide(ship,Boss_Bullets,False) or lost >=max_lost:
            finish2=True
            window.blit(lose,(200,200))

        text = font2.render("Рахунок: " + str(score), 1, (255,255,255))
        window.blit(text,(10,20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10, 50))        

        display.update()

    time.delay(50)