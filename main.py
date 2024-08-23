import random

class SnakesAndLadders:
    def __init__(self):
        self.board = list(range(101))
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100, 71: 91}
        self.player_positions = [0, 0]
        self.current_player = 0

    def roll_die(self):
        return random.randint(1, 6)

    def move_player(self):
        roll = self.roll_die()
        position = self.player_positions[self.current_player]
        position += roll
        if position > 100:
            position = 100 - (position - 100)
        if position in self.snakes:
            position = self.snakes[position]
        elif position in self.ladders:
            position = self.ladders[position]
        self.player_positions[self.current_player] = position

    def check_winner(self):
        return self.player_positions[self.current_player] == 100

    def switch_player(self):
        self.current_player = (self.current_player + 1) % 2

    def play(self):
        while True:
            self.move_player()
            print(f"Player {self.current_player + 1} is at position {self.player_positions[self.current_player]}")
            if self.check_winner():
                print(f"Player {self.current_player + 1} wins!")
                break
            self.switch_player()

if __name__ == "__main__":
    game = SnakesAndLadders()
    game.play()
