import taipy as tp
import random

class SnakeGame:

    def __init__(self, w=40, h=20):
        self.w = w
        self.h = h
        # Init game state
        self.direction = 'RIGHT'
        self.head = {'x': w // 2, 'y': h // 2}
        self.snake = [
            {'x': self.head['x'], 'y': self.head['y']},
            {'x': self.head['x'] - 1, 'y': self.head['y']},
            {'x': self.head['x'] - 2, 'y': self.head['y']}
        ]
        self.food = None
        self._place_food()

    def _place_food(self):
        self.food = {'x': random.randint(0, self.w - 1), 'y': random.randint(0, self.h - 1)}
        if self.food in self.snake:
            self._place_food()

    def play_step(self, direction):
        # Move snake
        new_head = {'x': self.head['x'], 'y': self.head['y']}
        if direction == 'UP':
            new_head['y'] -= 1
        elif direction == 'DOWN':
            new_head['y'] += 1
        elif direction == 'LEFT':
            new_head['x'] -= 1
        elif direction == 'RIGHT':
            new_head['x'] += 1

        self.snake.insert(0, new_head)
        self.head = new_head

        # Check if game over
        game_over = False
        if (
            self.head['x'] >= self.w or self.head['x'] < 0 or
            self.head['y'] >= self.h or self.head['y'] < 0 or
            self.head in self.snake[1:]
        ):
            game_over = True

        # Check if food is eaten
        if self.head == self.food:
            self._place_food()
        else:
            self.snake.pop()

        return game_over

    def get_board(self):
        board = [[' ' for _ in range(self.w)] for _ in range(self.h)]
        for seg in self.snake:
            board[seg['y']][seg['x']] = '*'
        board[self.food['y']][self.food['x']] = '#'
        return [''.join(row) for row in board]


# Initialize Snake game
game = SnakeGame()

# Define callback function for button clicks
def move_snake(direction):
    game_over = game.play_step(direction)
    if game_over:
        print("Game Over!")
    else:
        board = game.get_board()
        for row in board:
            print(row)

# Run the game loop
while True:
    move = input("Enter direction (W/A/S/D): ").upper()
    if move in ['W', 'A', 'S', 'D']:
        move_snake({'W': 'UP', 'A': 'LEFT', 'S': 'DOWN', 'D': 'RIGHT'}[move])
    else:
        print("Invalid input! Use W/A/S/D.")
