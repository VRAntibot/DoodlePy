import pygame

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
gravity = 4
gravity_kef = 2  # gravity * gravity_t
gravity_t = 0
gravity_t_max = -1
speed = 5

all_sprite = pygame.sprite.Group()
obstacles = pygame.sprite.Group()  # создаем группу спрайтов
clock = pygame.time.Clock()

player = pygame.sprite.Sprite(all_sprite)  # создаем спрайт
player.image = pygame.image.load('images.jpg')  # добавляем спрайту картинку
player.image = pygame.transform.scale(player.image, (50, 50))
player.rect = player.image.get_rect()
player.rect.topleft = (40, 40)

platform = pygame.sprite.Sprite(obstacles)  # создаем спрайт
platform.image = pygame.image.load('images.jpg')  # добавляем спрайту картинку
platform.image = pygame.transform.scale(platform.image, (100, 20))
platform.rect = platform.image.get_rect()
platform.rect.topleft = (200, 500)

jumpflag = False
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        x += speed
    if keys[pygame.K_a]:
        x -= speed
    #gravity
    if jumpflag:
        gravity_t = gravity_t_max
        jumpflag = False
    y += gravity * gravity_t
    gravity_t+=1/60
    #draw
    player.rect.centerx = x  # управление координатами спрайта
    player.rect.centery = y   # управление координатами спрайта
    screen.blit(player.image, player.rect)  # отрисовываем спрайт на экране
    screen.blit(platform.image, platform.rect)  # отрисовываем спрайт на экране
    if pygame.sprite.collide_mask(player, platform):
        jumpflag = True
    
    pygame.display.update()
    clock.tick(60) 
pygame.quit()
