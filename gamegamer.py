import pygame
import random
import sys

pygame.init()

# Настройка экрана
WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ALLIGATORILLA KILLER")

clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
ORANGE = (255, 140, 0)
PURPLE = (150, 50, 200)
YELLOW = (255, 220, 50)
GRAY = (150, 150, 150)

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 60)

GROUND_Y = 330

# Игрок
player = pygame.Rect(100, GROUND_Y - 40, 40, 40)
player_y_speed = 0
gravity = 0.8
jump_power = -15
on_ground = True

# Объекты
bullets = []
enemies = []

# Всякие переменные и тд

score = 0
game_speed = 6
enemy_timer = 0
next_enemy_time = 80
bullet_speed = 10
game_over = False

shoot_cooldown = 0


def draw_player():
    pygame.draw.circle(screen, ORANGE, player.center, 20)


def draw_bullets():
    for bullet in bullets:
        pygame.draw.circle(screen, YELLOW, bullet.center, 6)


def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, PURPLE, enemy)


def restart_game():
    global player_y_speed, on_ground
    global bullets, enemies
    global score, game_speed, enemy_timer
    global game_over, shoot_cooldown
    global next_enemy_time

    player.y = GROUND_Y - 40
    player_y_speed = 0
    on_ground = True

    bullets = []
    enemies = []

    score = 0
    game_speed = 6
    enemy_timer = 0
    next_enemy_time = 80

    shoot_cooldown = 0
    game_over = False


while True:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if not game_over:

                # Прыжок
                if event.key == pygame.K_SPACE and on_ground:
                    player_y_speed = jump_power
                    on_ground = False

                # Выстрел
                if event.key in (pygame.K_a, pygame.K_f):
                    if shoot_cooldown == 0:

                        bullet = pygame.Rect(
                            player.right,
                            player.centery - 5,
                            15,
                            10
                        )

                        bullets.append(bullet)
                        shoot_cooldown = 20

            else:

                if event.key == pygame.K_r:
                    restart_game()

    screen.fill(WHITE)

    if not game_over:

        score += 1

        # Постепенное увеличение сложности
        difficulty = score // 1000

        game_speed = min(6 + difficulty, 13)

        if shoot_cooldown > 0:
            shoot_cooldown -= 1

        # Прыжок
        player_y_speed += gravity
        player.y += player_y_speed

        if player.bottom >= GROUND_Y:
            player.bottom = GROUND_Y
            player_y_speed = 0
            on_ground = True

        # враги
        enemy_timer += 1

        if enemy_timer >= next_enemy_time:

            # Больше врагов
            amount = 1

            if difficulty >= 1:
                amount = random.choices(
                    [1, 2, 3],
                    weights=[50, 35, 15]
                )[0]

            for i in range(amount):

                enemy = pygame.Rect(
                    WIDTH + i * 65,
                    GROUND_Y - 35,
                    35,
                    35
                )

                enemies.append(enemy)

            enemy_timer = 0

            # Чем дальше игра, тем больше врагов
            min_time = max(25, 70 - difficulty * 7)
            max_time = max(45, 110 - difficulty * 9)

            next_enemy_time = random.randint(
                min_time,
                max_time
            )

        # Движение врагов
        for enemy in enemies:
            enemy.x -= game_speed

        # Движение снарядов
        for bullet in bullets:
            bullet.x += bullet_speed

        bullets = [
            bullet for bullet in bullets
            if bullet.left < WIDTH
        ]

        # Убийство врага
        for bullet in bullets[:]:

            for enemy in enemies[:]:

                if bullet.colliderect(enemy):

                    bullets.remove(bullet)
                    enemies.remove(enemy)

                    score += 100
                    break


        for enemy in enemies:

            if player.colliderect(enemy):
                game_over = True

        enemies = [
            enemy for enemy in enemies
            if enemy.right > 0
        ]

        # Земля
        pygame.draw.line(
            screen,
            BLACK,
            (0, GROUND_Y),
            (WIDTH, GROUND_Y),
            3
        )

        # Объекты
        draw_player()
        draw_bullets()
        draw_enemies()

        # Счёт
        score_text = font.render(
            f"Score: {score // 10}",
            True,
            BLACK
        )

        screen.blit(score_text, (20, 20))

        level_text = font.render(
            f"Level: {difficulty + 1}",
            True,
            GRAY
        )

        screen.blit(level_text, (20, 55))

    else:

        game_over_text = big_font.render(
            "GAME OVER",
            True,
            PURPLE
        )

        restart_text = font.render(
            "Press R to restart",
            True,
            BLACK
        )

        screen.blit(
            game_over_text,
            (WIDTH // 2 - 140, HEIGHT // 2 - 40)
        )

        screen.blit(
            restart_text,
            (WIDTH // 2 - 110, HEIGHT // 2 + 20)
        )

    pygame.display.update()


    # Игра на подобии гугл дино, я решила добавить возможность выстрела чтобы уничтожить врага, 
    # также потом я поняла что игра довольно скучная так что добавила увеличение сложности, со временем врагов становится больше