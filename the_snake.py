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

BORDER_COLOR = (93, 216, 228)

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

    def __init__(self):
        self.position = None
        self.body_color = None

    def draw(self):
        """Draw object on screen."""
        pass


class Snake(GameObject):
    """Create snake class."""

    def __init__(self):
        super().__init__()
        self.positions = [(SCREEN_CENTER_X, SCREEN_CENTER_Y)]
        self.body_color = SNAKE_COLOR
        self.head_color = SNAKE_HEAD_COLOR
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

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

        self.last = self.positions[-1]

    def adjust_tail(self):
        """Adjust tail size."""
        if len(self.positions) > self.length:
            del self.positions[-1]
        else:
            self.last = None

    def update_direction(self):
        """Update direction after user input."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Draw objects and border on screen."""
        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.head_color, head_rect)
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, head_rect, 1)

        if self.last:  # Use this instead of screen.fill()
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Get head position."""
        return self.positions[0]

    def check_collisions(self, apple):
        """Check all collisions."""
        self.check_self_collision()
        self.check_apple_collision(apple)

    def check_self_collision(self):
        """Check collision with self."""
        head_position = self.get_head_position()
        for position in self.positions[1:]:
            if position == head_position:
                self.reset()

    def check_apple_collision(self, apple):
        """Check collision with apple."""
        head_position = self.get_head_position()
        apple_position = apple.position

        if head_position == apple_position:
            self.length += 1
            apple.position = apple.randomize_position()

    def reset(self):
        """Restart Game."""
        screen.fill(BOARD_BACKGROUND_COLOR)  # Deletes old snake
        self.__init__()


class Apple(GameObject):
    """Create apple class."""

    def __init__(self):
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Draw apple and border on screen."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, self.body_color, rect, 1)

    def randomize_position(self):
        """Create random object position."""
        random_column_x = randint(0, SCREEN_WIDTH // GRID_SIZE - 1)
        random_row_y = randint(0, SCREEN_HEIGHT // GRID_SIZE - 1)

        random_position_x = random_column_x * GRID_SIZE
        random_position_y = random_row_y * GRID_SIZE

        return random_position_x, random_position_y


def handle_keys(game_object):
    """User input keys."""
    global game_speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
                game_object.update_direction()
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
                game_object.update_direction()
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
                game_object.update_direction()
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
                game_object.update_direction()

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

        # Тут опишите основную логику игры.

        handle_keys(snake)
        snake.move()
        snake.check_collisions(apple)
        snake.adjust_tail()
        apple.draw()
        snake.draw()

        clock.tick(game_speed)

        pygame.display.update()


if __name__ == '__main__':
    main()
