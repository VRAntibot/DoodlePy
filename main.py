import pygame
import random

pygame.init()
info = pygame.display.Info()
info_w = info.current_w / 2.5
info_h = info.current_h - 70
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = info_w, info_h
screen = pygame.display.set_mode(SCREEN_SIZE)
print(f'debug, x={info_w} y={info_h}')
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
x = 0
y = 0
flaga = True
gravity = 4
gravity_kef = 2  # gravity * gravity_t
gravity_t = 0
gravity_t_max = -1
speed = 5
changeFlag = False
all_sprite = pygame.sprite.Group()
obstacles = pygame.sprite.Group()  # создаем группу спрайтов
clock = pygame.time.Clock()

player = pygame.sprite.Sprite(all_sprite)  # создаем спрайт
player.image = pygame.image.load('images.jpg')  # добавляем спрайту картинку
player.image = pygame.transform.scale(player.image, (50, 50))
player.rect = player.image.get_rect()
player.rect.topleft = (200,450)
x = 200
y = 450
platform = pygame.sprite.Sprite(obstacles, all_sprite)  # создаем спрайт
platform.image = pygame.image.load('images.jpg')  # добавляем спрайту картинку
platform.image = pygame.transform.scale(platform.image, (100, 20))
platform.rect = platform.image.get_rect()
platform.rect.topleft = (200, 450)
def spawn_obstacle(y):
    obstacle = pygame.sprite.Sprite(all_sprite, obstacles)
    image_index = random.randint(1, 2)
    obstacle.image = pygame.image.load(f'platform{image_index}.png')
    obstacle.rect = obstacle.image.get_rect()
    print(random.randint(0, int(info_w)))
    obstacle.rect.x = random.randint(0, int(info_w))
    obstacle.rect.y = y
def create_initial_obstacles():
    fixed_y_positions = [100, 200, 300, 400, 500, 600]
    for y in fixed_y_positions:
        spawn_obstacle(y)

jumpflag = False
run = True
create_initial_obstacles()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    screen.fill(WHITE)
    if flaga:
        create_initial_obstacles()
        flaga = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        x += speed
    if keys[pygame.K_a]:
        x -= speed
    #gravity player
    if jumpflag:
        gravity_t = gravity_t_max
        jumpflag = False
    y += gravity * gravity_t
    if y< info_h/2:
        changeFlag = True
        y -= gravity * gravity_t
    gravity_t+=1/60
    #gravity platform
    for obstacle in obstacles:
        if changeFlag:
            obstacle.rect.y -= gravity * gravity_t
            if obstacle.rect.top > info_h:
                spawn_obstacle(0)
                obstacle.kill()
    changeFlag = False
    #draw
    player.rect.centerx = x  # управление координатами спрайта
    player.rect.centery = y   # управление координатами спрайта
    screen.blit(player.image, player.rect)  # отрисовываем спрайт на экране
    for obstacle in obstacles:
        screen.blit(obstacle.image, obstacle.rect)
    if pygame.sprite.collide_mask(player, platform) and gravity_t>0:
        jumpflag = True
    
    pygame.display.update()
    clock.tick(60) 
pygame.quit()
