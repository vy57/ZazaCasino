import random
import os
import json
from colorama import init, Fore

# Initialize Colorama
init()

# Modify the code to use color formatting

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        self.deck = []

        for suit in self.suits:
            for rank in self.ranks:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Chips:
    def __init__(self):
        self.total = 1000
        self.bet = 0
        self.winnings = 0

    def save_balance(self):
        data = {
            "total": self.total
        }
        with open("chips.json", "w") as file:
            json.dump(data, file)

    def load_balance(self):
        if os.path.exists("chips.json"):
            with open("chips.json", "r") as file:
                data = json.load(file)
                self.total = data.get("total", self.total)


class Blackjack:
    def __init__(self, chips):
        self.chips = chips

    def play(self):
        print(Fore.GREEN + "Welcome to Blackjack!")
        print("Your chip balance:", self.chips.total)

        while True:
            self.take_bet()

            deck = Deck()
            deck.shuffle()

            player_hand = []
            dealer_hand = []

            player_hand.append(deck.deal())
            dealer_hand.append(deck.deal())
            player_hand.append(deck.deal())
            dealer_hand.append(deck.deal())

            print(Fore.CYAN + "\nPlayer's Hand:")
            for card in player_hand:
                print(card)

            print("Total value:", self.calculate_hand_value(player_hand))

            print("Dealer's Hand:", ", ".join(str(card) for card in dealer_hand[:1]), "and one hidden card")

            player_value = self.calculate_hand_value(player_hand)
            dealer_value = self.calculate_hand_value(dealer_hand)

            if player_value == 21:
                print(Fore.GREEN + "Congratulations! You got a Blackjack!")
                self.chips.winnings += self.chips.bet * 2.5
            else:
                while True:
                    choice = input(Fore.YELLOW + "\nDo you want to hit or stand? (h/s): ")
                    if choice.lower() == 'h':
                        player_hand.append(deck.deal())
                        player_value = self.calculate_hand_value(player_hand)
                        print(Fore.CYAN + "Player's Hand:")
                        for card in player_hand:
                            print(card)
                        print("Total value:", player_value)
                        if player_value > 21:
                            print(Fore.RED + "Busted! You lose.")
                            self.chips.winnings -= self.chips.bet
                            break
                    elif choice.lower() == 's':
                        break
                    else:
                        print(Fore.RED + "Invalid choice. Please enter 'h' or 's'.")

            if player_value <= 21:
                while dealer_value < 17:
                    dealer_hand.append(deck.deal())
                    dealer_value = self.calculate_hand_value(dealer_hand)

                print(Fore.CYAN + "\nEvaluation:")
                print("Your hand:")
                for card in player_hand:
                    print(card)
                print("Total value:", player_value)

                print("Dealer's hand:")
                for card in dealer_hand:
                    print(card)
                print("Total value:", dealer_value)

                if dealer_value > 21:
                    print(Fore.GREEN + "Congratulations! Dealer busted. You win!")
                    self.chips.winnings += self.chips.bet
                elif dealer_value > player_value:
                    print(Fore.RED + "Sorry, you lose.")
                    self.chips.winnings -= self.chips.bet
                elif dealer_value < player_value:
                    print(Fore.GREEN + "Congratulations! You win!")
                    self.chips.winnings += self.chips.bet
                else:
                    print(Fore.YELLOW + "It's a tie!")

            print("Your chip balance:", self.chips.total)
            print("Your winnings:", self.chips.winnings)

            if self.chips.total == 0:
                print(Fore.RED + "You ran out of chips. Game over.")
                break

            choice = input(Fore.YELLOW + "Do you want to play again? (y/n): ")
            if choice.lower() != 'y':
                print(Fore.GREEN + "\nThanks for playing Blackjack!")
                break

    def take_bet(self):
        while True:
            try:
                bet = int(input(Fore.YELLOW + "Place your bet: "))
                if bet > self.chips.total:
                    print(Fore.RED + "Insufficient chips. Please place a valid bet.")
                else:
                    self.chips.bet = bet
                    break
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a valid bet.")

    def calculate_hand_value(self, hand):
        value = 0
        aces = 0

        for card in hand:
            if card.rank == "Ace":
                aces += 1
                value += 11
            elif card.rank in ["King", "Queen", "Jack"]:
                value += 10
            else:
                value += int(card.rank)

        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return value

class Mines:
    def __init__(self, chips):
        self.chips = chips

    def play(self):
        print(Fore.GREEN + "Welcome to Mines!")
        print("Your chip balance:", self.chips.total)

        while True:
            self.take_bet()

            rows = 5
            cols = 5
            num_mines = int(input(Fore.YELLOW + "Enter the number of mines to play with: "))

            grid = [[False for _ in range(cols)] for _ in range(rows)]
            revealed = [[False for _ in range(cols)] for _ in range(rows)]

            mines_placed = 0
            while mines_placed < num_mines:
                row = random.randint(0, rows - 1)
                col = random.randint(0, cols - 1)
                if not grid[row][col]:
                    grid[row][col] = True
                    mines_placed += 1

            while True:
                self.print_grid(grid, revealed)

                row = int(input(Fore.YELLOW + "Enter the row coordinate: "))
                col = int(input("Enter the column coordinate: "))

                if not self.is_valid_coordinate(row, col, rows, cols):
                    print(Fore.RED + "Invalid coordinate. Please enter valid coordinates.")
                    continue

                if revealed[row][col]:
                    print(Fore.RED + "This cell has already been revealed. Please choose another.")
                    continue

                if grid[row][col]:
                    print(Fore.RED + "Oh no! You hit a mine. Game over.")
                    self.chips.total -= self.chips.bet
                    self.chips.winnings = 0
                    break
                else:
                    print(Fore.GREEN + "Congratulations! You found a gem!")
                    self.chips.winnings += self.chips.bet * 2
                    print("Your winnings:", self.chips.winnings)
                    choice = input(Fore.YELLOW + "Do you want to take your winnings? (y/n): ")
                    if choice.lower() == 'y':
                        self.cash_out()
                        break

                revealed[row][col] = True

                if self.check_win(revealed):
                    print(Fore.GREEN + "You have revealed all the safe cells. You win!")
                    self.chips.total += self.chips.winnings
                    break

            print("Your chip balance:", self.chips.total)
            self.chips.save_balance()

            if self.chips.total == 0:
                print(Fore.RED + "You ran out of chips. Game over.")
                break

            choice = input(Fore.YELLOW + "Do you want to continue playing Mines? (y/n): ")
            if choice.lower() != 'y':
                self.cash_out()
                break

    def take_bet(self):
        while True:
            bet = int(input(Fore.YELLOW + "Place your bet: "))
            if 0 <= bet <= self.chips.total:
                self.chips.bet = bet
                break
            else:
                print(Fore.RED + "Invalid bet. Please enter a valid amount.")

    def print_grid(self, grid, revealed):
        print(Fore.BLUE + "\n--- Mines ---")
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if revealed[row][col]:
                    if grid[row][col]:
                        print(Fore.RED + "X", end=' ')
                    else:
                        print(Fore.GREEN + "O", end=' ')
                else:
                    print(Fore.BLUE + "*", end=' ')
            print()

    def is_valid_coordinate(self, row, col, rows, cols):
        return 0 <= row < rows and 0 <= col < cols

    def check_win(self, revealed):
        for row in revealed:
            if False in row:
                return False
        return True

    def cash_out(self):
        print(Fore.GREEN + "Cashing out...")
        print("Your total winnings:", self.chips.winnings)
        self.chips.total += self.chips.winnings
        print("Your final chip balance:", self.chips.total)
        self.chips.save_balance()


def main():
    chips = Chips()
    chips.load_balance()
    while True:
        print(Fore.BLUE + "\n--- ZazaCasino ---")
        print("1. Blackjack")
        print("2. Mines")
        print("3. Check Balance")
        print("4. Cash Out")
        choice = input(Fore.YELLOW + "Enter your choice: ")

        if choice == '1':
            blackjack = Blackjack(chips)
            blackjack.play()
        elif choice == '2':
            mines = Mines(chips)
            mines.play()
        elif choice == '3':
            print(Fore.GREEN + "Your current chip balance:", chips.total)
        elif choice == '4':
            mines.cash_out()
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
