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

# 캐릭터
character = pygame.image.load("Images\\character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - character_height - stage_height
character_to_x = 0
character_speed = 0.6

# 무기 생성
weapon = pygame.image.load("Images\\weapon.png")
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapon_to_y = 0

# 무기는 여러발 발사 가능
weapons = []

# 공 이미지
ball_images = [
    pygame.image.load("Images\\balloon1.png"),
    pygame.image.load("Images\\balloon2.png"),
    pygame.image.load("Images\\balloon3.png"),
    pygame.image.load("Images\\balloon4.png")
]

# 공 스피드
ball_speed_y = [-18, -15, -12, -9]

# 공 정보
balls = []

# 최초 발생하는 큰 공
balls.append({
    "pos_x" : 50,
    "pos_y" : 50,
    "img_idx" : 0,
    "to_x": 3,
    "to_y": -10,
    "init_spd_y" : ball_speed_y[0]
})

# 폰트
die_font = pygame.font.Font(None, 90)
die_text = die_font.render("Game Over", True, (255, 0, 0))        



running = True
while running:

    screen.blit(background, (0, 0))

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


    # 캐릭터 경계값
    if character_x_pos < 0:
        character_x_pos = 0
    if character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = -ball_val["to_x"]

        # 공이 스테이지에 충돌 시
        if ball_pos_y > screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        
        # 공이 허공에 있을 시
        else:
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 충돌처리 (공 and 캐릭터)
    character_rect = character.get_rect()
    character_rect.top = character_y_pos
    character_rect.left = character_x_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_x_pos = ball_val["pos_x"]
        ball_y_pos = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.top = ball_y_pos
        ball_rect.left = ball_x_pos

    if character_rect.colliderect(ball_rect):
        running = False
        screen.blit(die_text, (50, 50))

    # 충돌처리 (공 and 무기)
    for weapon_idx, weapon_val in enumerate(weapons):
        weapon_x_pos = weapon_val[0]
        weapon_y_pos = weapon_val[1]
        weapon_rect = weapon.get_rect()
        weapon_rect.top = weapon_y_pos
        weapon_rect.left = weapon_x_pos
        if weapon_rect.colliderect(ball_rect):
            pass # 공이 쪼개짐


    # 그리기
    for i, j in weapons:
        screen.blit(weapon, (i, j))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    for idx, val in enumerate(balls):
        ball_image_idx = val["img_idx"]
        screen.blit(ball_images[ball_image_idx], (val["pos_x"], val["pos_y"]))
    pygame.display.update()

pygame.time.delay(1500)

pygame.quit()