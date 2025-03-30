import pygame
import os
import random
import time
pygame.font.init()

WIDTH,HEIGHT = 750,750
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Shooter")

#Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("attatch","pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("attatch","pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("attatch","pixel_ship_blue_small.png"))

#Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("attatch","pixel_ship_yellow.png"))

# Laser
RED_LASER = pygame.image.load(os.path.join("attatch","pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("attatch","pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("attatch","pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("attatch","pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("attatch","background-black.png")),(WIDTH,HEIGHT))
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self,vel):
        self.y += vel

    def off_screen(self, height):
        return not (height >= self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 30

    def __init__(self,x,y,health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self,window):
        #pygame.draw.rect(window,(255,0,0),(self.x,self.y,50,50)) #在坐标x,y下画一个50px*50px的红色矩形。
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                 self.lasers.remove(laser)
            elif laser.collision(objs):
                objs.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1




    def get_width(self):
        return self.ship_img.get_width()

    def get_heigth(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        #self.width = self.ship_img.get_width()
        #self.height = self.ship_img.get_height()

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                 self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self,window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self,window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y +  self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
                }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]#通过返回color的值，从COLOR_MAP中调出对应的两个元素
        self.mask = pygame.mask.from_surface(self.ship_img)#产生像素级遮罩，用于碰撞检测

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 20)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5
    player = Player(300,630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG,(0,0))
        #draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255)) #把文字转换成图像
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10,0)) #把图像显示到窗口上
        WIN.blit(level_label, (WIDTH - level_label.get_width() -10, 0))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)#ship矩形显示出来

        if lost:
            #print("lost is true")
            lost_label = lost_font.render("You Lost!!",1,(255,255,255))
            WIN.blit(lost_label, (WIDTH/2-lost_label.get_width()/2, 350))

        pygame.display.update()



    while run:
        #print(run)
        clock.tick(FPS)
        #print(lost)
        #print(lives)
        redraw_window()
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100),random.randrange(-1500,-100),
                              random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        #按下按键，控制矩形移动，并控制在窗框内部。
        keys = pygame.key.get_pressed()
        #print("keys down")
        if keys[pygame.K_a] and player.x - player_vel > 0:#left
            player.x -= player_vel
            #print(f"player.x = {player.x}")
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:#right
            player.x += player_vel
            #print(f"player.x = {player.x}")
        if keys[pygame.K_w] and player.y - player_vel > 0:#up
            player.y -= player_vel
            #print(f"player.x = {player.x}")
        if keys[pygame.K_s] and player.y + player_vel + player.get_heigth() + 20 < HEIGHT:#down
            player.y += player_vel
            #print(f"player.x = {player.x}")
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 240) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_heigth() > HEIGHT:
                lives -= 1
                #player.health -= 30
                enemies.remove(enemy)


        player.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 60)
    run = True
    while run:
        WIN.blit(BG,(0,0))
        title_label = title_font.render("Press the mouse to begin...",1,(255,255,255))
        WIN.blit(title_label,(WIDTH/2 - title_label.get_width()/2, 350))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
