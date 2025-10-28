import pygame

pygame.init()


WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paddle Ball Demo")

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
RED = pygame.Color('red')
GREEN = pygame.Color('green')
YELLOW = pygame.Color('yellow')

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

BALL_RADIUS = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 120, 20
FPS = 60

def draw_text(surface, text, pos, color=WHITE, font_choice=font):
    img = font_choice.render(text, True, color)
    surface.blit(img, pos)

def change_color():
    color = pygame.Color(0)
    color.hsva = (pygame.time.get_ticks() % 360, 100, 100, 100)
    return color

def reset_ball():
    return WIDTH // 2, HEIGHT // 2, 0, 5, RED



ball_x, ball_y, ball_speed_x, ball_speed_y, ball_color = reset_ball()
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
paddle_y = HEIGHT - 50
paddle_speed = 8
score = 0
lives = 3
game_over = False
paused = False
in_title = True  
hit_counter = 0  
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_title and event.type == pygame.KEYDOWN:
            in_title = False
            score = 0
            lives = 3
            ball_x, ball_y, ball_speed_x, ball_speed_y, ball_color = reset_ball()
            game_over = False

        if game_over and event.type == pygame.KEYDOWN:
            in_title = True 

        if not in_title and not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

    keys = pygame.key.get_pressed()
    if not in_title and not game_over and not paused:
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x + PADDLE_WIDTH < WIDTH:
            paddle_x += paddle_speed

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if ball_x - BALL_RADIUS <= 0 or ball_x + BALL_RADIUS >= WIDTH:
            ball_speed_x *= -1
            ball_color = change_color()
        if ball_y - BALL_RADIUS <= 0:
            ball_speed_y *= -1
            ball_color = change_color()

        if (paddle_y < ball_y + BALL_RADIUS < paddle_y + PADDLE_HEIGHT and
            paddle_x < ball_x < paddle_x + PADDLE_WIDTH and ball_speed_y > 0):
            hit_pos = ((ball_x - paddle_x) / PADDLE_WIDTH) * 2 - 1
            ball_speed_x = hit_pos * 7
            ball_speed_y *= -1
            score += 1
            hit_counter += 1
            ball_color = change_color()

            if hit_counter % 5 == 0:
                ball_speed_x *= 1.1
                ball_speed_y *= 1.1

        if ball_y - BALL_RADIUS > HEIGHT:
            lives -= 1
            if lives > 0:
                ball_x, ball_y, ball_speed_x, ball_speed_y, ball_color = reset_ball()
            else:
                game_over = True

    window.fill(BLACK)

    if in_title:
        draw_text(window, "Paddle Ball Demo", (WIDTH // 2 - 190, HEIGHT // 2 - 80), YELLOW)
        draw_text(window, "Press any key to start", (WIDTH // 2 - 180, HEIGHT // 2), WHITE, small_font)

    elif game_over:
        draw_text(window, "GAME OVER", (WIDTH // 2 - 150, HEIGHT // 2 - 60), YELLOW)
        draw_text(window, f"Final Score: {score}", (WIDTH // 2 - 150, HEIGHT // 2))
        draw_text(window, "Press any key to return to title", (WIDTH // 2 - 230, HEIGHT // 2 + 60), WHITE, small_font)

    elif paused:
        draw_text(window, "PAUSED", (WIDTH // 2 - 80, HEIGHT // 2 - 30), YELLOW)
        draw_text(window, "Press P to resume", (WIDTH // 2 - 130, HEIGHT // 2 + 20), WHITE, small_font)

    else:
        pygame.draw.circle(window, ball_color, (int(ball_x), int(ball_y)), BALL_RADIUS)
        pygame.draw.rect(window, GREEN, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        draw_text(window, f"Score: {score}", (20, 20))
        draw_text(window, f"Lives: {lives}", (WIDTH - 180, 20))
        draw_text(window, "Press P to pause", (WIDTH // 2 - 100, 20), WHITE, small_font)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()



