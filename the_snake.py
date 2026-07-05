# Больше вроде нигде написать возможности нет, по этому напишу здесь.
# Большое спасибо за review. Пришлось попыхтеть,
# но много интересного для себя подчеркнул,
# как и при первом проекте с холодильником.

from random import randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER_X, SCREEN_CENTER_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SNAKE_HEAD_COLOR = (0, 0, 255)

SPEED = 20

game_speed = SPEED

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Create game class."""

    def __init__(self, position=(0, 0), body_color=(100, 100, 100)):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position, color):
        """Draw one cell of the object on screen."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect, 1)


class Snake(GameObject):
    """Create snake class."""

    def __init__(self):
        super().__init__((SCREEN_CENTER_X, SCREEN_CENTER_Y), SNAKE_COLOR)
        self.reset()

    def move(self):
        """Move object."""
        old_position_x, old_position_y = self.get_head_position()
        direction_x, direction_y = self.direction

        new_position_x = (
            old_position_x + direction_x * GRID_SIZE
        ) % SCREEN_WIDTH
        new_position_y = (
            old_position_y + direction_y * GRID_SIZE
        ) % SCREEN_HEIGHT

        self.positions.insert(0, (new_position_x, new_position_y))

        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.draw_cell(
                self.last, BOARD_BACKGROUND_COLOR
            )  # Reset tail color
            del self.positions[-1]

    def update_direction(self, next_direction):
        """Update direction after user input."""
        self.direction = next_direction

    def draw_head(self):
        """Draw the head of the snake"""
        head_color = (randint(50, 255), randint(50, 255), randint(50, 255))
        self.draw_cell(self.positions[0], head_color)

    def get_head_position(self):
        """Get head position."""
        return self.positions[0]

    def check_self_collision(self):
        """Check collision with self."""
        head_position = self.get_head_position()
        for position in self.positions[1:]:
            if position == head_position:
                reset_screen()
                self.reset()

    def reset(self):
        """Restart Game."""
        super().__init__((SCREEN_CENTER_X, SCREEN_CENTER_Y), SNAKE_COLOR)
        self.positions = [self.position]
        self.head_color = SNAKE_HEAD_COLOR
        self.length = 1
        self.direction = RIGHT
        self.last = None


class Apple(GameObject):
    """Create apple class."""

    def __init__(self):
        super().__init__(self.randomize_position(positions=()), APPLE_COLOR)

    # Я при первой сдаче хотел прислать с циклом,
    # но я в него передавал snake.positions что в принципе не правильно.
    # Убрал потому что тесты на платформе не принимали.
    def randomize_position(self, positions):
        """Create random object position."""
        while True:
            random_column_x = randint(0, SCREEN_WIDTH // GRID_SIZE - 1)
            random_row_y = randint(0, SCREEN_HEIGHT // GRID_SIZE - 1)

            random_position_x = random_column_x * GRID_SIZE
            random_position_y = random_row_y * GRID_SIZE

            apple_new_position = (random_position_x, random_position_y)

            if apple_new_position not in positions:
                return apple_new_position

    def draw(self):
        """Draw the apple."""
        self.draw_cell(self.position, self.body_color)


def reset_screen():
    """Reset screen."""
    screen.fill(BOARD_BACKGROUND_COLOR)  # Deletes old snake


def handle_keys(game_object):
    """User input keys."""
    global game_speed

    directions = {
        (pygame.K_UP, UP): UP,
        (pygame.K_UP, DOWN): DOWN,
        (pygame.K_UP, LEFT): UP,
        (pygame.K_UP, RIGHT): UP,
        (pygame.K_DOWN, UP): UP,
        (pygame.K_DOWN, DOWN): DOWN,
        (pygame.K_DOWN, LEFT): DOWN,
        (pygame.K_DOWN, RIGHT): DOWN,
        (pygame.K_LEFT, UP): LEFT,
        (pygame.K_LEFT, DOWN): LEFT,
        (pygame.K_LEFT, LEFT): LEFT,
        (pygame.K_LEFT, RIGHT): RIGHT,
        (pygame.K_RIGHT, UP): RIGHT,
        (pygame.K_RIGHT, DOWN): RIGHT,
        (pygame.K_RIGHT, LEFT): LEFT,
        (pygame.K_RIGHT, RIGHT): RIGHT
    }

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit

            key = (event.key, game_object.direction)

            if key in directions:
                game_object.update_direction(directions[key])

            elif event.unicode == '+':
                game_speed += 2
            elif event.unicode == '-' and game_speed > 2:
                game_speed += -2


def main():
    """Run the main game loop."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:

        handle_keys(snake)

        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)

        snake.check_self_collision()

        snake.draw_head()
        apple.draw()

        clock.tick(game_speed)

        pygame.display.update()


if __name__ == '__main__':
    main()
