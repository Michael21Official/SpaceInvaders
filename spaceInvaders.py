import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

background = pygame.transform.scale(pygame.image.load('kosmos.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
player_img = pygame.transform.scale(pygame.image.load('spaceship.png'), (70, 70))
bullet_img = pygame.transform.scale(pygame.image.load('shoot1.png'), (20, 20))
explosion_imgs = [pygame.transform.scale(pygame.image.load(f'explosion{i}.png'), (50, 50)) for i in range(1, 7)]
shield_img = pygame.transform.scale(pygame.image.load('shield.png'), (60, 30))
ufo_img = pygame.transform.scale(pygame.image.load('wrogDuzy.png'), (100, 60))

enemy_imgs = [
    pygame.transform.scale(pygame.image.load('wrog0.png'), (50, 50)),
    pygame.transform.scale(pygame.image.load('wrog1.png'), (50, 50)),
    pygame.transform.scale(pygame.image.load('wrog2.png'), (50, 50)),
    pygame.transform.scale(pygame.image.load('wrog3.png'), (50, 50))
]

shoot_sound = pygame.mixer.Sound('shoot.mp3')
explosion_sound = pygame.mixer.Sound('explosion.mp3')

def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_enemy(enemy):
    screen.blit(enemy_imgs[enemy["type"]], (enemy["x"], enemy["y"]))

def draw_shields():
    for shield in shields:
        if shield["health"] > 0:
            screen.blit(shield_img, (shield["x"], shield["y"]))

def fire_bullet(x, y):
    global bullets
    bullet = {"x": x, "y": y, "state": "fire"}
    bullets.append(bullet)
    pygame.mixer.Sound.play(shoot_sound)

def is_collision(x1, y1, x2, y2, distance):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) < distance

def draw_ufo():
    if ufo["active"]:
        screen.blit(ufo_img, (ufo["x"], ufo["y"]))
        font = pygame.font.Font(None, 48)
        health_text = font.render(f"Health: {ufo['health']}", True, (255, 255, 255))
        screen.blit(health_text, (ufo["x"], ufo["y"] - 30))

def get_settings_from_menu():
    settings = {
        'level': 1,
        'num_rows': 4,
        'num_cols': 8,
        'enemy_speed': 1
    }
    print("Settings from menu:", settings)
    return settings

def start_game(settings):
    global player_x, player_y, player_x_change, score, lives, enemy_speed, enemy_direction, enemies, ufo, shields, bullets, ufo_bullets, level
    level = settings['level']
    enemy_speed = settings['enemy_speed']
    enemy_direction = 1

    player_x = SCREEN_WIDTH // 2 - 50
    player_y = SCREEN_HEIGHT - 100
    player_x_change = 0
    score = 0
    lives = 3

    rows = settings['num_rows']
    cols = settings['num_cols']
    enemy_margin_x = SCREEN_WIDTH // (cols + 1)
    enemy_margin_y = SCREEN_HEIGHT // (rows + 2)
    enemy_width = int(enemy_margin_x * 0.8)
    enemy_height = int(enemy_margin_y * 0.8)

    enemies = []
    for row in range(rows):
        for col in range(cols):
            enemies.append({
                "x": col * enemy_margin_x + enemy_margin_x // 2,
                "y": row * enemy_margin_y + 50,
                "speed": enemy_speed,
                "type": random.randint(0, len(enemy_imgs) - 1),
                "health": 1
            })

    ufo = {
        "x": random.randint(0, SCREEN_WIDTH - 100),
        "y": 10,
        "speed": 4,
        "active": False,
        "timer": 0,
        "health": 10
    }

    shields = [
        {"x": 150, "y": SCREEN_HEIGHT - 200, "health": 3},
        {"x": 400, "y": SCREEN_HEIGHT - 200, "health": 3},
        {"x": 650, "y": SCREEN_HEIGHT - 200, "health": 3}
    ]

    bullets = []
    ufo_bullets = []
    game_loop()

def ufo_fire_bullet():
    if ufo["active"]:
        bullet = {"x": ufo["x"] + 50, "y": ufo["y"] + 60, "speed": 5, "state": "fire"}
        ufo_bullets.append(bullet)

def enemy_fire_bullet(enemy):
    if random.randint(1, 100) < 5:
        bullet = {"x": enemy["x"] + 20, "y": enemy["y"] + 30, "speed": 5, "state": "fire"}
        bullets.append(bullet)

def game_loop():
    global player_x, player_y, player_x_change, score, lives, enemy_speed, enemy_direction, enemies, ufo, level, bullets, ufo_bullets

    running = True
    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -8
                if event.key == pygame.K_RIGHT:
                    player_x_change = 8
                if event.key == pygame.K_SPACE:
                    fire_bullet(player_x, player_y)
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player_x_change = 0

        player_x += player_x_change
        player_x = max(0, min(player_x, SCREEN_WIDTH - 70))

        for bullet in bullets[:]:
            if bullet["state"] == "fire":
                screen.blit(bullet_img, (bullet["x"] + 25, bullet["y"] - 20))
                bullet["y"] -= 15
                if bullet["y"] < 0:
                    bullets.remove(bullet)

        for bullet in ufo_bullets[:]:
            if bullet["state"] == "fire":
                screen.blit(bullet_img, (bullet["x"], bullet["y"]))
                bullet["y"] += bullet["speed"]
                if bullet["y"] > SCREEN_HEIGHT:
                    ufo_bullets.remove(bullet)

        move_down = False
        for enemy in enemies:
            enemy["x"] += enemy_direction * enemy["speed"]
            if enemy["x"] <= 0:
                enemy["x"] = 0
                move_down = True
            elif enemy["x"] >= SCREEN_WIDTH - 50:
                enemy["x"] = SCREEN_WIDTH - 50
                move_down = True

            if enemy["y"] < SCREEN_HEIGHT // 2:
                enemy_fire_bullet(enemy)

        if move_down:
            for enemy in enemies:
                enemy["y"] += 50
            enemy_direction *= -1

        for enemy in enemies[:]:
            for bullet in bullets[:]:
                if is_collision(enemy["x"], enemy["y"], bullet["x"], bullet["y"], 30):
                    pygame.mixer.Sound.play(explosion_sound)
                    bullets.remove(bullet)
                    score += 10
                    enemies.remove(enemy)

        if ufo["active"]:
            for bullet in bullets[:]:
                if is_collision(ufo["x"], ufo["y"], bullet["x"], bullet["y"], 30):
                    pygame.mixer.Sound.play(explosion_sound)
                    bullets.remove(bullet)
                    ufo["health"] -= 1

                    screen.blit(random.choice(explosion_imgs), (ufo["x"], ufo["y"]))

                    if ufo["health"] <= 0:
                        ufo["active"] = False
                        score += 1000

                        for i in range(6):
                            screen.blit(explosion_imgs[i], (ufo["x"], ufo["y"]))
                            pygame.display.update()
                            pygame.time.delay(100)

                        ufo["x"] = random.randint(0, SCREEN_WIDTH - 100)
                        ufo["y"] = 10
                        ufo["timer"] = 0
                        ufo["health"] = random.randint(5, 8)

        if not enemies and not ufo["active"]:
            ufo["active"] = True

        if ufo["active"]:
            if ufo["timer"] < 300:
                ufo["y"] += 1
            else:
                ufo["x"] += ufo["speed"]
                if ufo["x"] <= 0 or ufo["x"] >= SCREEN_WIDTH - 100:
                    ufo["speed"] *= -1

            ufo["timer"] += 1
            if ufo["y"] > SCREEN_HEIGHT // 2:
                ufo["y"] = SCREEN_HEIGHT // 2

            if random.randint(1, 100) < 2:
                ufo_fire_bullet()

        for enemy in enemies:
            draw_enemy(enemy)

        draw_player(player_x, player_y)
        draw_shields()
        draw_ufo()

        for bullet in ufo_bullets[:]:
            if is_collision(player_x, player_y, bullet["x"], bullet["y"], 30):
                pygame.mixer.Sound.play(explosion_sound)
                ufo_bullets.remove(bullet)
                lives -= 1

                if lives <= 0:
                    font = pygame.font.Font(None, 64)
                    game_over_text = font.render("GAME OVER", True, (255, 255, 255))
                    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
                    pygame.display.update()
                    pygame.time.delay(2000)
                    running = False

        pygame.display.update()

    pygame.quit()

settings = get_settings_from_menu()
start_game(settings)
