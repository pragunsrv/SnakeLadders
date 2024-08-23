import random
import time

class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[i + j * self.size for i in range(self.size)] for j in range(self.size)]
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
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
        self.inventory = []
        self.equipped_items = {}
        self.score = 0
        self.level = 1
        self.experience = 0
        self.xp_to_next_level = 100
        self.bonus_points = 0
        self.inventory_limit = 5
        self.extra_turns = 0
        self.teleportation_uses = 0
        self.healing_potions = 0
        self.double_dice_uses = 0

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
        self.gain_experience(10)
        if self.extra_turns > 0:
            self.extra_turns -= 1
            return True
        return False

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

    def add_item(self, item):
        if len(self.inventory) < self.inventory_limit:
            self.inventory.append(item)
        else:
            print(f"Inventory full! Cannot add {item.name}.")

    def equip_item(self, item_name):
        if item_name in self.inventory:
            self.equipped_items[item_name] = self.inventory.remove(item_name)
        else:
            print(f"Item {item_name} not found in inventory.")

    def use_item(self, item_name):
        if item_name in self.equipped_items:
            item = self.equipped_items[item_name]
            item.use(self)
        else:
            print(f"Item {item_name} is not equipped.")

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.xp_to_next_level:
            self.experience -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level *= 1.5
            print(f"{self.name} leveled up to {self.level}!")

    def add_bonus_points(self, points):
        self.bonus_points += points

    def __str__(self):
        return f"{self.name} is at position {self.position}, Level: {self.level}, Experience: {self.experience}, Bonus Points: {self.bonus_points}, Extra Turns: {self.extra_turns}, Teleportation Uses: {self.teleportation_uses}, Healing Potions: {self.healing_potions}, Double Dice Uses: {self.double_dice_uses}"

class Ability:
    def __init__(self, name, effect, cooldown):
        self.name = name
        self.effect = effect
        self.cooldown = cooldown

    def use(self, player):
        self.effect(player)
        print(f"{player.name} used {self.name} ability.")

class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def use(self, player):
        self.effect(player)
        print(f"{player.name} used item {self.name}.")

class Game:
    def __init__(self):
        self.board = Board(size=10)
        self.players = [Player(f'Player {i + 1}') for i in range(4)]
        self.current_player_index = 0
        self.max_moves = 1000
        self.immune_turns = 0
        self.round = 1
        self.special_abilities_used = {}
        self.history = []
        self.items = [
            Item("Healing Potion", lambda p: p.healing_potions += 1),
            Item("Double Dice", lambda p: p.double_dice_uses += 1),
            Item("Shield", lambda p: p.activate_immunity()),
            Item("Speed Boots", lambda p: p.move(p.roll_die(), self.board.snakes, self.board.ladders)),
            Item("Teleportation Device", lambda p: p.teleportation_uses += 1),
            Item("Extra Life", lambda p: p.add_bonus_points(50)),
            Item("Magic Wand", lambda p: p.gain_experience(25)),
            Item("Invisibility Cloak", lambda p: p.activate_immunity()),
            Item("Energy Drink", lambda p: p.move(p.roll_die() * 2, self.board.snakes, self.board.ladders)),
            Item("Mystery Box", lambda p: p.gain_experience(random.randint(10, 50))),
            Item("Coin Purse", lambda p: p.add_bonus_points(random.randint(10, 30))),
            Item("Teleportation Stone", lambda p: p.teleportation_uses += 1),
            Item("Regeneration Potion", lambda p: p.add_status_effect(lambda p: print(f"{p.name} regenerating"), 2)),
            Item("Luck Charm", lambda p: p.roll_die() * 2),
            Item("Victory Medal", lambda p: p.add_bonus_points(100)),
            Item("Power-Up", lambda p: p.move(p.roll_die() * 2, self.board.snakes, self.board.ladders)),
            Item("Time Stopper", lambda p: p.extra_turns += 1),
            Item("Mana Potion", lambda p: p.special_abilities.append(Ability("Extra Turn", lambda p: p.move(p.roll_die(), self.board.snakes, self.board.ladders), 3))),
            Item("Luck Potion", lambda p: p.gain_experience(random.randint(20, 50))),
            Item("Teleportation Amulet", lambda p: p.position = random.choice([20, 40, 60, 80, 100])),
            Item("Phoenix Feather", lambda p: p.healing_potions += 2),
            Item("Dragon Scale", lambda p: p.add_status_effect(lambda p: print(f"{p.name} has increased defense"), 5)),
            Item("Speed Boost", lambda p: p.move(p.roll_die() * 3, self.board.snakes, self.board.ladders)),
            Item("Health Potion", lambda p: p.healing_potions += 1),
            Item("Mystic Orb", lambda p: p.add_status_effect(lambda p: print(f"{p.name} gains bonus points"), 3)),
            Item("Time Machine", lambda p: p.position = 1),
            Item("Power Stone", lambda p: p.add_special_ability(Ability("Shield", lambda p: p.activate_immunity(), 2), 2))
        ]

    def roll_and_move(self):
        player = self.players[self.current_player_index]
        roll = player.roll_die()
        if player.move(roll, self.board.snakes, self.board.ladders):
            print(f"{player.name} rolled a {roll} and moved to {player.position}.")
            if player.position == 100:
                print(f"{player.name} wins!")
                self.history.append((player.name, player.position, roll))
                return True
            self.history.append((player.name, player.position, roll))
        return False

    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def activate_immune_mode(self):
        player = self.players[self.current_player_index]
        player.activate_immunity()
        print(f"{player.name} activated immunity mode.")

    def handle_status_effects(self):
        for player in self.players:
            player.apply_status_effects()
            player.decrement_cooldowns()

    def special_abilities_phase(self):
        for i, player in enumerate(self.players):
            if player.special_abilities:
                print(f"{player.name}'s Special Abilities:")
                for j, ability in enumerate(player.special_abilities):
                    print(f"{j}. {ability.name} (Cooldown: {player.special_ability_cooldowns[ability.name]})")
                choice = int(input(f"Select ability for {player.name}: "))
                player.use_special_ability(choice)
                self.special_abilities_used[player.name] = player.special_abilities[choice]

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
        print("6. Special items may alter game dynamics.")
        print("7. Manage inventory and use items strategically.")
        print("8. Track status effects and cooldowns.")
        print("9. Use special items for various effects.")
        print("10. Activate special abilities at the right time.")
        print("11. Use inventory items to gain advantages.")
        print("12. Collect bonus points and experience.")
        print("13. Extra turns and teleportation can change the game.")
        print("14. Healing potions can restore your health.")
        print("15. Special abilities can be used strategically.")
        print("16. Items may provide additional benefits.")

    def setup_game(self):
        self.display_rules()
        self.load_history()
        self.assign_special_abilities()
        for player in self.players:
            for item in self.items:
                player.add_item(item)
                if item.name in ["Healing Potion", "Double Dice"]:
                    player.equip_item(item.name)
            player.add_special_ability(Ability("Extra Turn", lambda p: p.move(p.roll_die(), self.board.snakes, self.board.ladders), 3), 3)
            player.add_special_ability(Ability("Swap Position", lambda p: self.swap_positions(), 4), 4)
            player.gain_experience(50)
            player.add_bonus_points(10)
            player.inventory_limit = 20
            player.add_item(self.items[5])
            player.add_item(self.items[6])
            player.add_item(self.items[7])
            player.add_item(self.items[8])
            player.add_item(self.items[9])
            player.add_item(self.items[10])
            player.add_item(self.items[11])
            player.add_item(self.items[12])
            player.add_item(self.items[13])
            player.add_item(self.items[14])
            player.add_item(self.items[15])
            player.add_item(self.items[16])
            player.add_item(self.items[17])
            player.add_item(self.items[18])
            player.add_item(self.items[19])
            player.add_item(self.items[20])
            player.add_item(self.items[21])
            player.add_item(self.items[22])
            player.add_item(self.items[23])
            player.add_item(self.items[24])
            player.add_item(self.items[25])
            player.add_item(self.items[26])
            player.add_item(self.items[27])
            player.add_item(self.items[28])
            player.add_item(self.items[29])
            player.add_item(self.items[30])
            player.add_item(self.items[31])
            player.add_item(self.items[32])
            player.add_item(self.items[33])
            player.add_item(self.items[34])
            player.add_item(self.items[35])
            player.add_item(self.items[36])
            player.add_item(self.items[37])
            player.add_item(self.items[38])
            player.add_item(self.items[39])
            player.add_item(self.items[40])
            player.add_item(self.items[41])
            player.add_item(self.items[42])
            player.add_item(self.items[43])
            player.add_item(self.items[44])
            player.add_item(self.items[45])
            player.add_item(self.items[46])
            player.add_item(self.items[47])
            player.add_item(self.items[48])
            player.add_item(self.items[49])
            player.add_item(self.items[50])
            player.add_item(self.items[51])
            player.add_item(self.items[52])
            player.add_item(self.items[53])
            player.add_item(self.items[54])
            player.add_item(self.items[55])
            player.add_item(self.items[56])
            player.add_item(self.items[57])
            player.add_item(self.items[58])
            player.add_item(self.items[59])
            player.add_item(self.items[60])
            player.add_item(self.items[61])
            player.add_item(self.items[62])
            player.add_item(self.items[63])
            player.add_item(self.items[64])

    def swap_positions(self):
        p1, p2 = self.players
        p1.position, p2.position = p2.position, p1.position
        print(f"Positions swapped: {p1.name} is now at {p1.position}, {p2.name} is now at {p2.position}")
    def roll_and_move_(self):
        player = self.players[self.current_player_index]
        roll = player.roll_die()
        if player.move(roll, self.board.snakes, self.board.ladders):
            print(f"{player.name} rolled a {roll} and moved to {player.position}.")
            if player.position == 100:
                print(f"{player.name} wins!")
                self.history.append((player.name, player.position, roll))
                return True
            self.history.append((player.name, player.position, roll))
        return False

    def switch_player_(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def activate_immune__mode(self):
        player = self.players[self.current_player_index]
        player.activate__immunity()
        print(f"{player.name} activated immunity mode.")

    def handle_status__effects(self):
        for player in self.players:
            player.apply_status_effects()
            player.decrement_cooldowns()

    def special_abilities__phase(self):
        for i, player in enumerate(self.players):
            if player.special_abilities:
                print(f"{player.name}'s Special Abilities:")
                for j, ability in enumerate(player.special_abilities):
                    print(f"{j}. {ability.name} (Cooldown: {player.special_ability_cooldowns[ability.name]})")
                choice = int(input(f"Select ability for {player.name}: "))
                player.use_special_ability(choice)
                self.special_abilities_used[player.name] = player.special_abilities[choice]

    def save_history_(self):
        with open('game_history.txt', 'w') as file:
            for entry in self.history:
                file.write(f"{entry[0]} moved to {entry[1]} after rolling {entry[2]}\n")

    def load_history_(self):
        try:
            with open('game_history.txt', 'r') as file:
                for line in file:
                    print(line.strip())
        except FileNotFoundError:
            print("No game history found.")
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
