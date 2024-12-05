from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс игровых объектов, от которого наследуются другие"""

    def __init__(self) -> None:
        """Инициализатор базового класса игровых объектов"""
        self.position: tuple = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color: tuple = ()

    def draw(self) -> None:
        """Заготовка метода для отрисовки объекта"""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним"""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self) -> None:
        """Устанавливает случайное положение для ябока в игром поле"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self) -> None:
        """Отрисовывает яблоко на игровой поверхности"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и ее поведение"""

    def __init__(self) -> None:
        super().__init__()
        self.length: int = 1
        self.positions: list = [self.position]
        self.direction: tuple = RIGHT
        self.next_direction = None
        self.body_color: tuple = SNAKE_COLOR
        self.last = None

    def update_direction(self) -> None:
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Обновляет позицию змейки"""
        x, y = self.get_head_position()
        new_x = (x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_x, new_y)

        if new_head_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_position)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def draw(self) -> None:
        """Отрисовывает змейку на экране"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple:
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self) -> None:
        """Cбрасывает змейку в начальное состояние после столкновения"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция для оброботки нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной игровой цикл"""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
