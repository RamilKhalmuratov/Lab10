import psycopg2
import pygame
import json
import random

# Подключение к БД
def connect_db():
    return psycopg2.connect(
        dbname="phonebook_db",
        user="postgres",
        password="22041983re",  # Ваш пароль
        host="localhost"
    )

# Проверка/создание пользователя
def get_user(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO users (username) VALUES (%s) RETURNING user_id", (username,))
        user_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO user_scores (user_id, level, score) VALUES (%s, 1, 0)", (user_id,))
        conn.commit()
        print(f"✅ Новый пользователь '{username}' создан!")
    else:
        user_id = user[0]
        cursor.execute("SELECT level, score FROM user_scores WHERE user_id = %s", (user_id,))
        level, score = cursor.fetchone()
        print(f"🕹️ Добро пожаловать, {username}! Текущий уровень: {level}, счёт: {score}")
    conn.close()
    return user_id

# Сохранение игры
def save_game(user_id, level, score, state):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user_scores SET level = %s, score = %s, saved_state = %s WHERE user_id = %s",
        (level, score, json.dumps(state), user_id)
    )
    conn.commit()
    conn.close()
    print("💾 Игра сохранена!")

# Основная игра
def play_game(username):
    user_id = get_user(username)
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    
    # Параметры игры
    snake_pos = [[100, 100], [90, 100], [80, 100]]
    direction = "RIGHT"
    food_pos = [random.randrange(1, 80) * 10, random.randrange(1, 60) * 10]
    score = 0
    level = 1
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_game(user_id, level, score, {"snake_pos": snake_pos})
                    running = False
                # Управление змейкой
                elif event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
        
        # Движение змейки
        if direction == "UP":
            snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] - 10])
        elif direction == "DOWN":
            snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] + 10])
        elif direction == "LEFT":
            snake_pos.insert(0, [snake_pos[0][0] - 10, snake_pos[0][1]])
        elif direction == "RIGHT":
            snake_pos.insert(0, [snake_pos[0][0] + 10, snake_pos[0][1]])
        
        # Проверка на съедение еды
        if snake_pos[0] == food_pos:
            score += 10
            food_pos = [random.randrange(1, 80) * 10, random.randrange(1, 60) * 10]
        else:
            snake_pos.pop()
        
        # Отрисовка
        screen.fill((0, 0, 0))
        for pos in snake_pos:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food_pos[0], food_pos[1], 10, 10))
        
        # Отображение счёта
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Счёт: {score} | Уровень: {level}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(15)  # Скорость игры
    
    pygame.quit()

# Старт игры
if __name__ == "__main__":
    username = input("Введите ваш username: ")
    play_game(username)