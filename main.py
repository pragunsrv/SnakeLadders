import random

class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[i + j * self.size for i in range(self.size)] for j in range(self.size)]
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100, 71: 91}
        self.create_board()

    def create_board(self):
        self.display_board()

    def display_board(self):
        print("Board:")
        for row in self.board:
            print(" ".join(f"{x:2}" for x in row))

    def get_position(self, pos):
        row = (pos - 1) // self.size
        col = (pos - 1) % self.size
        return (row, col)

    def get_value(self, row, col):
        return self.board[row][col]

    def set_value(self, row, col, value):
        self.board[row][col] = value

    def print_snakes_and_ladders(self):
        print("Snakes:")
        for start, end in self.snakes.items():
            print(f"From {start} to {end}")
        print("Ladders:")
        for start, end in self.ladders.items():
            print(f"From {start} to {end}")

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.total_moves = 0

    def roll_die(self):
        return random.randint(1, 6)

    def move(self, roll, snakes, ladders):
        new_position = self.position + roll
        if new_position > 100:
            new_position = 100 - (new_position - 100)
        if new_position in snakes:
            new_position = snakes[new_position]
        elif new_position in ladders:
            new_position = ladders[new_position]
        self.position = new_position
        self.total_moves += 1

    def __str__(self):
        return f"{self.name} is at position {self.position}"

class Game:
    def __init__(self):
        self.board = Board(size=10)
        self.players = [Player(f'Player {i + 1}') for i in range(2)]
        self.current_player_index = 0
        self.max_moves = 1000

    def roll_and_move(self):
        player = self.players[self.current_player_index]
        roll = player.roll_die()
        player.move(roll, self.board.snakes, self.board.ladders)
        print(f"{player.name} rolled a {roll} and moved to {player.position}")
        if player.position == 100:
            print(f"{player.name} wins!")
            return True
        return False

    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        print(f"Switching to {self.players[self.current_player_index].name}")

    def play(self):
        self.board.print_snakes_and_ladders()
        moves = 0
        while moves < self.max_moves:
            if self.roll_and_move():
                break
            self.switch_player()
            moves += 1
        else:
            print("Maximum moves reached.")

if __name__ == "__main__":
    game = Game()
    game.play()
