import random

class SnakesAndLadders:
    def __init__(self):
        self.board_size = 10
        self.board = [[i + j * self.board_size for i in range(self.board_size)] for j in range(self.board_size)]
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100, 71: 91}
        self.players = [{'position': 0, 'name': f'Player {i + 1}'} for i in range(2)]
        self.current_player_index = 0
        self.total_rolls = 0
        self.max_rolls = 1000

    def roll_die(self):
        return random.randint(1, 6)

    def move_player(self):
        player = self.players[self.current_player_index]
        roll = self.roll_die()
        self.total_rolls += 1
        if self.total_rolls > self.max_rolls:
            print("Maximum rolls reached.")
            return
        position = player['position'] + roll
        if position > 100:
            position = 100 - (position - 100)
        if position in self.snakes:
            position = self.snakes[position]
        elif position in self.ladders:
            position = self.ladders[position]
        player['position'] = position
        print(f"{player['name']} rolled a {roll} and moved to {position}")

    def check_winner(self):
        return self.players[self.current_player_index]['position'] == 100

    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        print(f"Switching to {self.players[self.current_player_index]['name']}")

    def display_board(self):
        print("Board:")
        for row in self.board:
            print(" ".join(f"{x:2}" for x in row))

    def play(self):
        self.display_board()
        while True:
            self.move_player()
            if self.check_winner():
                print(f"{self.players[self.current_player_index]['name']} wins!")
                break
            self.switch_player()

if __name__ == "__main__":
    game = SnakesAndLadders()
    game.play()
