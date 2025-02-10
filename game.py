import pygame
import sys
import random

# -------------------- Настройка основных параметров --------------------
BLOCK_SIZE = 20                   # Размер одного блока в пикселях
GRID_WIDTH = 30                   # Количество блоков по горизонтали
GRID_HEIGHT = 20                  # Количество блоков по вертикали
WIDTH = GRID_WIDTH * BLOCK_SIZE   # Ширина окна игры
HEIGHT = GRID_HEIGHT * BLOCK_SIZE # Высота окна игры

# Определение цветов (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# -------------------- Класс змейки --------------------
class Snake:
    def __init__(self):
        # Инициализируем змейку, начинающуюся в центре экрана, длиной 3 сегмента
        init_x = GRID_WIDTH // 2
        init_y = GRID_HEIGHT // 2
        self.segments = [
            (init_x, init_y),
            (init_x - 1, init_y),
            (init_x - 2, init_y)
        ]
        self.direction = (1, 0)  # Начальное направление – вправо
        self.grow_flag = False   # Флаг, сигнализирующий о необходимости увеличения длины

    def move(self):
        # Вычисляем новое положение головы
        head_x, head_y = self.segments[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        # Добавляем новую голову в начало списка сегментов
        self.segments.insert(0, new_head)
        # Если змейке не нужно расти, удаляем последний сегмент
        if self.grow_flag:
            self.grow_flag = False
        else:
            self.segments.pop()

    def change_direction(self, new_direction):
        # Запрещаем разворот на 180° (то есть смену направления на противоположное)
        opposite_direction = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_direction:
            self.direction = new_direction

    def grow(self):
        # Устанавливаем флаг для увеличения длины при следующем перемещении
        self.grow_flag = True

    def draw(self, surface):
        # Рисуем каждый сегмент змейки на поверхности
        for i, segment in enumerate(self.segments):
            x, y = segment
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            # Голова змейки выделяется другим цветом
            if i == 0:
                pygame.draw.rect(surface, BLUE, rect)
            else:
                pygame.draw.rect(surface, GREEN, rect)
            # Добавляем обводку для эстетики
            pygame.draw.rect(surface, DARK_GREEN, rect, 1)

# -------------------- Класс еды --------------------
class Food:
    def __init__(self, snake_segments):
        self.position = self.random_position(snake_segments)

    def random_position(self, snake_segments):
        # Выбираем случайную позицию, которая не занята сегментами змейки
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_segments:
                return pos

    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(surface, RED, rect)

# -------------------- Класс игры --------------------
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Игра Змейка")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.reset_game()

    def reset_game(self):
        # Инициализация новых объектов игры
        self.snake = Snake()
        self.food = Food(self.snake.segments)
        self.score = 0
        self.game_over = False

    def handle_events(self):
        # Обработка событий (нажатий клавиш, закрытие окна)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Управление направлением змейки стрелками
                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))
                # После окончания игры можно нажать R для рестарта
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()

    def update(self):
        # Обновление состояния игры, если игра не окончена
        if not self.game_over:
            self.snake.move()
            head_x, head_y = self.snake.segments[0]

            # Проверка столкновения со стенами
            if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
                self.game_over = True

            # Проверка столкновения с собственным телом
            if self.snake.segments[0] in self.snake.segments[1:]:
                self.game_over = True

            # Проверка на съедение еды
            if self.snake.segments[0] == self.food.position:
                self.snake.grow()
                self.score += 1
                self.food = Food(self.snake.segments)

    def render(self):
        # Отрисовка всех элементов игры
        self.screen.fill(BLACK)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        # Отображаем текущий счет
        score_surface = self.font.render(f"Счет: {self.score}", True, WHITE)
        self.screen.blit(score_surface, (10, 10))

        # Если игра окончена, выводим сообщение
        if self.game_over:
            game_over_surface = self.font.render("Игра окончена! Нажмите R для новой игры", True, WHITE)
            rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(game_over_surface, rect)

        pygame.display.flip()

    def run(self):
        # Главный цикл игры
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(10)  # Ограничение до 10 кадров в секунду

# -------------------- Запуск игры --------------------
def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
