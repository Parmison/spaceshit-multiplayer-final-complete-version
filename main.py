import pygame
import time
pygame.init()

space = pygame.image.load("lesson 6/image/space bg.png")

yellow_ship = pygame.image.load("lesson 6/image/spaceship yellow.png")
yellow_ship= pygame.transform.scale(yellow_ship,(100,100))

orange_ship = pygame.image.load("lesson 6/image/spaceship orange.png")
orange_ship = pygame.transform.scale(orange_ship,(100,100))

font = pygame.font.SysFont("Times New Roman",36)

screen = pygame.display.set_mode((1250,690))

border = pygame.Rect(625,0,5,690)

#pygame.sprite.Sprite

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super().__init__()
        self.color = color
        self.rect = pygame.Rect(x,y,5,10)
    def update(self):
        if self.color == "yellow":
            self.rect.x += 5 
            if self.rect.x>1250:
                self.kill()
        elif self.color == "orange":
            self.rect.x -= 5 
            if self.rect.x<0:
                self.kill()


class Spaceship(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super().__init__()
        self.color = color
        if color == "yellow":
            self.image = pygame.transform.rotate(yellow_ship,90)
        elif color == "orange":
            self.image = pygame.transform.rotate(orange_ship,270)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.health = 100
    def handel_movement(self,keys):
        if self.color == "orange":
            if keys[pygame.K_UP] and self.rect.y>50:
                self.rect.y -= 1
            if keys[pygame.K_DOWN] and self.rect.y<550:
                self.rect.y += 1
            if keys[pygame.K_LEFT] and self.rect.x>650:
                self.rect.x -= 1
            if keys[pygame.K_RIGHT] and self.rect.x<1000:
                self.rect.x += 1

        if self.color == "yellow":
            if keys[pygame.K_w] and self.rect.y>50:
                self.rect.y -= 1
            if keys[pygame.K_s] and self.rect.y<550:
                self.rect.y += 1
            if keys[pygame.K_a] and self.rect.x>50:
                self.rect.x -= 1
            if keys[pygame.K_d] and self.rect.x<450:
                self.rect.x += 1

orange = Spaceship(950,330,"orange")
yellow = Spaceship(350,330,"yellow")

def draw_window(yellow,orange,yellow_bullets,orange_bullets):
    screen.blit(space,(0,0))
    pygame.draw.rect(screen,"white",border)
    screen.blit(orange.image,orange.rect.center)
    screen.blit(yellow.image,yellow.rect.center)
    text1 = font.render(f"health left yellow:{yellow.health}",True,"white")
    text2 = font.render(f"health left orange:{orange.health}",True,"white")
    screen.blit(text1,(100,50))
    screen.blit(text2,(900,50))
    for bullet in yellow_bullets:
        pygame.draw.rect(screen,"yellow",bullet.rect)
    for bullet in orange_bullets:
        pygame.draw.rect(screen,"orange",bullet.rect)
    pygame.display.update()
clock = pygame.time.Clock()

yellow_bullets = pygame.sprite.Group()
orange_bullets = pygame.sprite.Group()

def handel_collision(orange,yellow,orange_bullets,yellow_bullets):
    for bullet in yellow_bullets:
        if orange.rect.colliderect(bullet.rect):
            orange.health -= 1
            bullet.kill()
            print("oranges dead")
    for bullet in orange_bullets:
        if yellow.rect.colliderect(bullet.rect):
            yellow.health -= 1
            bullet.kill()
            print("yellows dead")

def winner(player):
    Player = font.render(f"{player} has won the battle",True,"white")
    screen.blit(Player,(625,345))
    pygame.display.update()
    pygame.time.delay(5000)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                bullet1 = Bullet(yellow.rect.x+100,yellow.rect.y + yellow.rect.height/2+50,"yellow")
                yellow_bullets.add(bullet1)
            if event.key == pygame.K_p:
                bullet2 = Bullet(orange.rect.x,orange.rect.y + orange.rect.height/2+50,"orange")
                orange_bullets.add(bullet2)
    if orange.health <= 0:
        winner("yellow")
        break
    if yellow.health <= 0:
        winner("orange")
        break

    keys = pygame.key.get_pressed()
    orange.handel_movement(keys)
    yellow.handel_movement(keys)
    yellow_bullets.update()
    orange_bullets.update()
    draw_window(yellow,orange,yellow_bullets,orange_bullets)
    handel_collision(orange,yellow,orange_bullets,yellow_bullets)
