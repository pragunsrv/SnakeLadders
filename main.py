import random
import time

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
        self.is_immune = False
        self.special_abilities = []
        self.special_ability_cooldowns = {}
        self.status_effects = []

    def roll_die(self):
        return random.randint(1, 6)

    def move(self, roll, snakes, ladders):
        if self.is_immune:
            self.is_immune = False
            return
        new_position = self.position + roll
        if new_position > 100:
            new_position = 100 - (new_position - 100)
        if new_position in snakes:
            new_position = snakes[new_position]
        elif new_position in ladders:
            new_position = ladders[new_position]
        self.position = new_position
        self.total_moves += 1

    def activate_immunity(self):
        self.is_immune = True

    def add_special_ability(self, ability, cooldown):
        self.special_abilities.append(ability)
        self.special_ability_cooldowns[ability.name] = cooldown

    def use_special_ability(self, index):
        if 0 <= index < len(self.special_abilities):
            ability = self.special_abilities[index]
            if self.special_ability_cooldowns[ability.name] > 0:
                print(f"{ability.name} is on cooldown for {self.special_ability_cooldowns[ability.name]} more turns.")
                return
            ability.use(self)
            self.special_ability_cooldowns[ability.name] = ability.cooldown
        else:
            print("Invalid ability index.")

    def decrement_cooldowns(self):
        for ability in self.special_ability_cooldowns:
            if self.special_ability_cooldowns[ability] > 0:
                self.special_ability_cooldowns[ability] -= 1

    def add_status_effect(self, effect, duration):
        self.status_effects.append((effect, duration))

    def apply_status_effects(self):
        for effect, duration in self.status_effects:
            if duration > 0:
                effect(self)
                duration -= 1
        self.status_effects = [(effect, duration) for effect, duration in self.status_effects if duration > 0]

    def __str__(self):
        return f"{self.name} is at position {self.position}"

class Ability:
    def __init__(self, name, effect, cooldown):
        self.name = name
        self.effect = effect
        self.cooldown = cooldown

    def use(self, player):
        self.effect(player)
        print(f"{player.name} used {self.name} ability.")

class Game:
    def __init__(self):
        self.board = Board(size=10)
        self.players = [Player(f'Player {i + 1}') for i in range(2)]
        self.current_player_index = 0
        self.max_moves = 1000
        self.immune_turns = 0
        self.round = 1
        self.special_abilities_used = {}
        self.history = []

    def roll_and_move(self):
        player = self.players[self.current_player_index]
        roll = player.roll_die()
        player.move(roll, self.board.snakes, self.board.ladders)
        self.history.append((player.name, player.position, roll))
        print(f"{player.name} rolled a {roll} and moved to {player.position}")
        player.apply_status_effects()
        if player.position == 100:
            print(f"{player.name} wins!")
            return True
        player.decrement_cooldowns()
        if self.immune_turns > 0:
            self.immune_turns -= 1
        return False

    def activate_immune_mode(self):
        for player in self.players:
            player.activate_immunity()
        self.immune_turns = 3
        print("Immune mode activated for all players!")

    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        print(f"Switching to {self.players[self.current_player_index].name}")

    def assign_special_abilities(self):
        ability1 = Ability("Extra Roll", lambda p: p.move(p.roll_die(), self.board.snakes, self.board.ladders), 2)
        ability2 = Ability("Skip Turn", lambda p: print(f"{p.name} skipped their turn."), 1)
        self.players[0].add_special_ability(ability1, 2)
        self.players[1].add_special_ability(ability2, 1)

    def special_abilities_phase(self):
        for i, player in enumerate(self.players):
            if player.special_abilities:
                print(f"{player.name}'s Special Abilities:")
                for j, ability in enumerate(player.special_abilities):
                    print(f"{j}: {ability.name} (Cooldown: {player.special_ability_cooldowns[ability.name]})")
                choice = int(input(f"{player.name}, choose an ability to use (number): "))
                player.use_special_ability(choice)
                if player.name not in self.special_abilities_used:
                    self.special_abilities_used[player.name] = set()
                self.special_abilities_used[player.name].add(choice)

    def handle_status_effects(self):
        for player in self.players:
            if player.status_effects:
                print(f"{player.name} is affected by:")
                for effect, duration in player.status_effects:
                    print(f"- {effect.__name__} (Duration: {duration})")

    def save_history(self):
        with open('game_history.txt', 'w') as file:
            for entry in self.history:
                file.write(f"{entry[0]} moved to {entry[1]} after rolling {entry[2]}\n")

    def load_history(self):
        try:
            with open('game_history.txt', 'r') as file:
                for line in file:
                    print(line.strip())
        except FileNotFoundError:
            print("No game history found.")

    def display_rules(self):
        print("Game Rules:")
        print("1. Roll the die to move.")
        print("2. Snakes will move you down.")
        print("3. Ladders will move you up.")
        print("4. Use special abilities wisely.")
        print("5. First to reach position 100 wins.")

    def setup_game(self):
        self.display_rules()
        self.load_history()
        self.assign_special_abilities()

    def play(self):
        self.setup_game()
        self.board.print_snakes_and_ladders()
        moves = 0
        while moves < self.max_moves:
            print(f"Round {self.round}")
            self.special_abilities_phase()
            if self.roll_and_move():
                self.save_history()
                break
            if moves % 10 == 0:
                self.activate_immune_mode()
            self.handle_status_effects()
            self.switch_player()
            moves += 1
            self.round += 1
            time.sleep(1)
        else:
            print("Maximum moves reached.")
            self.save_history()

if __name__ == "__main__":
    game = Game()
    game.play()
