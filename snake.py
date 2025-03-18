import pygame
import sys
import random

# -------------------- Настройка основных параметров --------------------
BLOCK_SIZE = 20                   # Размер одного блока в пикселях
GRID_WIDTH = 30                   # Количество блоков по горизонтали
GRID_HEIGHT = 20                  # Количество блоков по вертикали
GAME_AREA_Y_OFFSET = 30           # Смещение игрового поля для области счета
WIDTH = GRID_WIDTH * BLOCK_SIZE   # Ширина окна игры
HEIGHT = GRID_HEIGHT * BLOCK_SIZE + GAME_AREA_Y_OFFSET  # Высота окна с учетом области счета

# Определение цветов (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
SNAKE_BODY_COLOR = (0, 200, 0)    # Яркий зеленый для тела змейки
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)      # Светло-серый для сетки
DARK_GRAY = (50, 50, 50)          # Темно-серый для области счета

# -------------------- Класс змейки --------------------
class Snake:
    def __init__(self):
        init_x = GRID_WIDTH // 2
        init_y = GRID_HEIGHT // 2
        self.segments = [
            (init_x, init_y),
            (init_x - 1, init_y),
            (init_x - 2, init_y)
        ]
        self.direction = (1, 0)  # Начальное направление – вправо
        self.grow_flag = False

    def move(self):
        head_x, head_y = self.segments[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.segments.insert(0, new_head)
        if self.grow_flag:
            self.grow_flag = False
        else:
            self.segments.pop()

    def change_direction(self, new_direction):
        opposite_direction = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_direction:
            self.direction = new_direction

    def grow(self):
        self.grow_flag = True

    def draw(self, surface, offset_y):
        for i, segment in enumerate(self.segments):
            x, y = segment
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE + offset_y, BLOCK_SIZE, BLOCK_SIZE)
            if i == 0:  # Голова
                pygame.draw.rect(surface, BLUE, rect)
                # Добавляем глаза в зависимости от направления
                eye_size = 4
                if self.direction == (1, 0):  # Вправо
                    eye1 = (x * BLOCK_SIZE + BLOCK_SIZE - 6, y * BLOCK_SIZE + offset_y + 6)
                    eye2 = (x * BLOCK_SIZE + BLOCK_SIZE - 6, y * BLOCK_SIZE + offset_y + 14)
                elif self.direction == (-1, 0):  # Влево
                    eye1 = (x * BLOCK_SIZE + 6, y * BLOCK_SIZE + offset_y + 6)
                    eye2 = (x * BLOCK_SIZE + 6, y * BLOCK_SIZE + offset_y + 14)
                elif self.direction == (0, -1):  # Вверх
                    eye1 = (x * BLOCK_SIZE + 6, y * BLOCK_SIZE + offset_y + 6)
                    eye2 = (x * BLOCK_SIZE + 14, y * BLOCK_SIZE + offset_y + 6)
                elif self.direction == (0, 1):  # Вниз
                    eye1 = (x * BLOCK_SIZE + 6, y * BLOCK_SIZE + offset_y + BLOCK_SIZE - 6)
                    eye2 = (x * BLOCK_SIZE + 14, y * BLOCK_SIZE + offset_y + BLOCK_SIZE - 6)
                pygame.draw.circle(surface, WHITE, eye1, eye_size)
                pygame.draw.circle(surface, WHITE, eye2, eye_size)
            else:  # Тело
                pygame.draw.rect(surface, SNAKE_BODY_COLOR, rect)
            pygame.draw.rect(surface, DARK_GREEN, rect, 1)

# -------------------- Класс еды --------------------
class Food:
    def __init__(self, snake_segments):
        self.position = self.random_position(snake_segments)

    def random_position(self, snake_segments):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_segments:
                return pos

    def draw(self, surface, offset_y):
        x, y = self.position
        center = (x * BLOCK_SIZE + BLOCK_SIZE // 2, y * BLOCK_SIZE + offset_y + BLOCK_SIZE // 2)
        pygame.draw.circle(surface, RED, center, BLOCK_SIZE // 2)

# -------------------- Класс игры --------------------
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.reset_game()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food(self.snake.segments)
        self.score = 0
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()

    def update(self):
        if not self.game_over:
            self.snake.move()
            head_x, head_y = self.snake.segments[0]
            if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
                self.game_over = True
            if self.snake.segments[0] in self.snake.segments[1:]:
                self.game_over = True
            if self.snake.segments[0] == self.food.position:
                self.snake.grow()
                self.score += 1
                self.food = Food(self.snake.segments)

    def draw_grid(self, offset_y):
        for x in range(0, WIDTH, BLOCK_SIZE):
            pygame.draw.line(self.screen, LIGHT_GRAY, (x, offset_y), (x, offset_y + GRID_HEIGHT * BLOCK_SIZE))
        for y in range(offset_y, offset_y + GRID_HEIGHT * BLOCK_SIZE, BLOCK_SIZE):
            pygame.draw.line(self.screen, LIGHT_GRAY, (0, y), (WIDTH, y))

    def render(self):
        self.screen.fill(BLACK)
        # Отрисовка области счета
        score_rect = pygame.Rect(0, 0, WIDTH, GAME_AREA_Y_OFFSET)
        pygame.draw.rect(self.screen, DARK_GRAY, score_rect)
        title_surface = self.font.render("Snake Game", True, WHITE)
        self.screen.blit(title_surface, (10, 5))
        score_surface = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_surface.get_rect(right=WIDTH - 10, top=5)
        self.screen.blit(score_surface, score_rect)

        # Отрисовка игрового поля
        self.draw_grid(GAME_AREA_Y_OFFSET)
        self.snake.draw(self.screen, GAME_AREA_Y_OFFSET)
        self.food.draw(self.screen, GAME_AREA_Y_OFFSET)
        game_area_rect = pygame.Rect(0, GAME_AREA_Y_OFFSET, WIDTH, GRID_HEIGHT * BLOCK_SIZE)
        pygame.draw.rect(self.screen, WHITE, game_area_rect, 1)

        # Экран "Game Over"
        if self.game_over:
            overlay = pygame.Surface((WIDTH, GRID_HEIGHT * BLOCK_SIZE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, GAME_AREA_Y_OFFSET))
            game_over_text = f"Game Over! Score: {self.score} Press R to restart"
            game_over_surface = self.font.render(game_over_text, True, WHITE)
            rect = game_over_surface.get_rect(center=(WIDTH // 2, GAME_AREA_Y_OFFSET + (GRID_HEIGHT * BLOCK_SIZE) // 2))
            self.screen.blit(game_over_surface, rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(10)

# -------------------- Запуск игры --------------------
def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
