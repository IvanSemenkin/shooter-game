from pygame import *
from random import randint
from time import sleep
win_width = 1366
win_height = 768
points = 0
hp = 3
lost = 0
points = 0
nissed = 0
FPS = 60
made = 0
score2 = 0
make = False
finish = False
rgb = (255,129,0)

window = display.set_mode((0, 0), FULLSCREEN)
display.set_caption('Догонялки')
background = transform.scale(image.load("galaxy.jpg"), (1366, 768))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, x, y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (x, y))
        self.speed = player_speed
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
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 25, 45, 7)
        bullet1 = Bullet('bullet.png', self.rect.centerx, self.rect.top - 55, 25, 45, 7)
        bullets.add(bullet)
        bullets.add(bullet1)

bullets = sprite.Group()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost     
        if self.rect.y > win_width:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost = lost + 1


class Boss(GameSprite):
    hp = 3
    def update(self):
        if self.rect.x > 1260:
            self.direction = 'left' 
        elif self.rect.x < 100:
            self.direction = 'right'

        if self.direction == 'left':
            self.rect.x -= self.speed
        if self.direction == 'right':
            self.rect.x += self.speed 

        

    def fire(self):
        bullet_boss = Bullet('bullet.png', self.rect.centerx, self.rect.bottom, 15, 20, -15)
        bullets_boss.add(bullet_boss)

bullets_boss = sprite.Group()


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed    
        if self.rect.y < 0 or self.rect.y > 700:
            self.kill()
    

img_enamy = 'ufo.png'
monsters = sprite.Group()
for i in range(1, 3):
    monster = Enemy(img_enamy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

font.init()
font = font.SysFont('Arial', 35)

rocet = Player('rocket.png', 680, 600, 100, 100, 15)

clock = time.Clock()

# mixer.init()
# mixer.music.load('Shooting Stars.mp3')
# mixer.music.play()

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocet.fire()
            elif e.key == K_ESCAPE:
                game = False
                

    if not finish:
        window.blit(background, (0, 0))
        score = font.render('Счёт ' + str(points), True, rgb)
        window.blit(score, (10, 20))
        los = font.render('Пропущено ' + str(lost), True, rgb)
        window.blit(los, (10, 50))
        # hp_boss = font.render('Жизни босса ' + str(enemy_boss.hp), True, (rgb))
        # window.blit(hp_boss, (10, 80))
        sprites_list = sprite.groupcollide(monsters, bullets, True, False)



        for i in sprites_list:
            points = points + 1
            score2 = score2 + 1
            if score2 >= 5:
                make = True
                if make == True:
                    enemy_boss = Boss('pngwing.png', 1267, 100, 100, 100, 7)
                    enemy_boss.hp = 3
                    make = False
                    made = 1
                    score2 = 0
            monster = Enemy(img_enamy, randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
            monsters.add(monster)
    
        rocet.reset()
        rocet.update()
        monsters.update()
        
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()
        if made == 1:
            enemy_boss.update()
            enemy_boss.reset()
            

            bullets_boss.draw(window)
            bullets_boss.update()
            if len(bullets_boss) < 3:
                enemy_boss.fire()

            bullets_boss.draw(window)
            if sprite.spritecollide(rocet, bullets_boss, False):
                finish = True
                aaa = font.render('Вы проиграли!' , True, rgb)
                window.blit(aaa, (win_width/2, win_height/2))
            if sprite.spritecollide(enemy_boss, bullets, True):
                enemy_boss.hp -= 1
                if enemy_boss.hp <= 0:
                    enemy_boss.kill()
                    made = 0
                print(enemy_boss.hp)
    else:
        rocet = Player('rocket.png', 680, 600, 100, 100, 15)
        monsters = sprite.Group()
        for i in range(1, 3):
            monster = Enemy(img_enamy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            monsters.add(monster)
        lost = 0
        points = 0
        time.delay(3000)
        finish = False
        made = 0
        print('Начинаем заново!')
            

    clock.tick(FPS)
    display.update()
