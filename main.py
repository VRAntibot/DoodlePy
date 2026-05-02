import pygame
import random
import time

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
b = ""
high_jump = False
score=0
flaga = True
springflag = True
gravity = 6
gravity_kef = 2  # gravity * gravity_t
gravity_t = 0
gravity_t_max = -1
speed = 5
fps = 0
frames = 0
change_plat = False
last_event_time = time.time()
change_time = time.time()
changeFlag = False
all_sprite = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
platforms = pygame.sprite.Group()
move = pygame.sprite.Group()
springs = pygame.sprite.Group()# создаем группу спрайтов
destructible = pygame.sprite.Group()# создаем группу спрайтов
clock = pygame.time.Clock()

player = pygame.sprite.Sprite(all_sprite)  # создаем спрайт
player.image = pygame.image.load('player.png')  # добавляем спрайту картинку
player.image = pygame.transform.scale(player.image, (50, 50))

background_image = pygame.image.load('back.png')

player.rect = player.image.get_rect()
player.rect.topleft = (200,450)
x = 200
y = 450
def spawn_obstacle(y):
    a = random.randint(1,15)
    if a == 1:
        spring = pygame.sprite.Sprite(all_sprite, springs, obstacles)
        image_index = random.randint(1, 2)
        spring.image = pygame.image.load(f'spring{image_index}.png')
        spring.image = pygame.transform.scale(spring.image, (100, 70))
        spring.rect = spring.image.get_rect()
        # position
        print(random.randint(0, int(info_w)))
        spring.rect.x = random.randint(0, int(info_w))
        spring.rect.y = y
    elif a == 2:
        d_platform = pygame.sprite.Sprite(all_sprite, destructible, obstacles)
        image_index = random.randint(1, 2)
        d_platform.image = pygame.image.load(f'platform_d.png')
        d_platform.image = pygame.transform.scale(d_platform.image, (100, 70))
        d_platform.rect = d_platform.image.get_rect()
        # position
        print(random.randint(0, int(info_w)))
        d_platform.rect.x = random.randint(0, int(info_w))
        d_platform.rect.y = y
    elif a == 3 or a == 4:
        m_platform = pygame.sprite.Sprite(all_sprite, move, platforms, obstacles)
        image_index = random.randint(1, 2)
        m_platform.image = pygame.image.load(f'platform_m.png')
        m_platform.image = pygame.transform.scale(m_platform.image, (100, 70))
        m_platform.rect = m_platform.image.get_rect()
        # position
        print(random.randint(0, int(info_w)))
        m_platform.rect.x = random.randint(0, int(info_w))
        m_platform.rect.y = y
    else:
        platform = pygame.sprite.Sprite(all_sprite, obstacles,platforms)
        image_index = random.randint(1, 2)
        platform.image = pygame.image.load(f'platform{image_index}.png')
        platform.image = pygame.transform.scale(platform.image, (100, 70))
        platform.rect = platform.image.get_rect()
        #position
        print(random.randint(0, int(info_w)))
        platform.rect.x = random.randint(0, int(info_w))
        platform.rect.y = y
def create_initial_obstacles():
    fixed_y_positions = list(range(75, 901, 75))
    for y in fixed_y_positions:
        spawn_obstacle(y)

jumpflag = False
run = True
#create_initial_obstacles()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.blit(background_image, (0, 0))
    
    #fps counter
    frames+=1
    current_time = time.time()
    if current_time - last_event_time >= 1:
        last_event_time = current_time
        fps = frames
        frames = 0
    if flaga:
        create_initial_obstacles()
        flaga = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        x += speed
    if keys[pygame.K_a]:
        x -= speed
    if keys[pygame.K_SPACE]:
        high_jump = True
        b = "High jump"
    else:
        high_jump = False
        b = ""

    #gravity player
    if player.rect.left > SCREEN_WIDTH:
        player.rect.right = 0
        x = player.rect.right 
    if player.rect.right < 0:
        player.rect.left = SCREEN_WIDTH
        x = player.rect.left 
    if y > 800:
        b = "Game over :("


    if springflag:
        gravity_t = gravity_t_max*2
        springflag = False
    elif jumpflag:
        gravity_t = gravity_t_max
        jumpflag = False
    y += gravity * gravity_t
    if y< info_h/2:
        changeFlag = True
        y -= gravity * gravity_t
        score+=1
    gravity_t+=1/60
    #gravity platform
    for obstacle in obstacles:
        if changeFlag:
            obstacle.rect.y -= gravity * gravity_t
            if obstacle.rect.top > info_h:
                spawn_obstacle(0)
                obstacle.kill()
    changeFlag = False
    
    if current_time - change_time >= 5:
        change_time = current_time
        if change_plat:
            change_plat = False
        else:
            change_plat = True
    for plat in move:
        if change_plat:
            plat.rect.y -= 1
        else:
            plat.rect.y += 1 
    #draw
        #text
    font_object = pygame.font.SysFont('Arial', 28)
    text = font_object.render(f'Score:{score} {b}', False, 'white')
    screen.blit(text, (10, 10))
    #fps
    font_object = pygame.font.SysFont('Arial', 28)
    text = font_object.render(f'Fps:{fps}', False, 'white')
    screen.blit(text, (info_w-100, 10))
        #player
    player.rect.centerx = x  # управление координатами спрайта
    player.rect.centery = y   # управление координатами спрайта
    screen.blit(player.image, player.rect)  # отрисовываем спрайт на экране
    for obstacle in obstacles:
        screen.blit(obstacle.image, obstacle.rect)
    if pygame.sprite.spritecollide(player, platforms, False, pygame.sprite.collide_mask) and gravity_t>0:
        if high_jump and score > 500:
            springflag = True
            score -= 500
        else:
            jumpflag = True
    if pygame.sprite.spritecollide(player, springs, False, pygame.sprite.collide_mask) and gravity_t>0:
        springflag = True
    hits = pygame.sprite.spritecollide(player, destructible, False, pygame.sprite.collide_mask)
    if hits and gravity_t>0:
        jumpflag = True
        for hit in hits:
            hit.kill()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
