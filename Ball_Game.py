from secrets import token_hex
import pygame

pygame.init()

# 스크린
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 타이틀
pygame.display.set_caption("Ball Game")

# FPS
clock = pygame.time.Clock()



# 배경
background = pygame.image.load("Images\\background.png")

# 스테이지
stage = pygame.image.load("Images\\stage.png")
stage_size = stage.get_rect().size
stage_width = stage_size[0]
stage_height = stage_size[1]

# 캐릭터 생성
character = pygame.image.load("Images\\character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - character_height - stage_height
character_to_x = 0
character_speed = 0.8

# 무기 생성
weapon = pygame.image.load("Images\\weapon.png")
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapon_to_y = 0

# 무기는 여러발 발사 가능
weapons = []

running = True
while running:
    
    dt = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x = -character_speed * dt
            if event.key == pygame.K_RIGHT:
                character_to_x = character_speed * dt

            if event.key == pygame.K_SPACE:
                weapon_to_y = -0.4 * dt
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)                
                weapon_y_pos = character_y_pos
                weapons.append((weapon_x_pos, weapon_y_pos))

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and character_to_x < 0) or (event.key == pygame.K_RIGHT and character_to_x > 0):
                character_to_x = 0

    character_x_pos += character_to_x
    weapons = [(i, j + weapon_to_y) for i, j in weapons]
    weapons = [(i, j) for i, j in weapons if j > 0]


    # 경계값
    if character_x_pos < 0:
        character_x_pos = 0
    if character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 그리기
    screen.blit(background, (0, 0))
    for i, j in weapons:
        screen.blit(weapon, (i, j))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    pygame.display.update()


pygame.quit()