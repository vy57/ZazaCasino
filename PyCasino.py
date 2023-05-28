import random
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
    def __init__(self, total=100):
        self.total = total
        self.bet = 0


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
                self.chips.total += self.chips.bet * 2.5
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
                            self.chips.total -= self.chips.bet
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
                    self.chips.total += self.chips.bet
                elif dealer_value > player_value:
                    print(Fore.RED + "Sorry, you lose.")
                    self.chips.total -= self.chips.bet
                elif dealer_value < player_value:
                    print(Fore.GREEN + "Congratulations! You win!")
                    self.chips.total += self.chips.bet
                else:
                    print(Fore.YELLOW + "It's a tie!")

            print("Your chip balance:", self.chips.total)

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

class Roulette:
    def __init__(self, chips):
        self.chips = chips

    def play(self):
        print(Fore.GREEN + "Welcome to Roulette!")
        print("This is a placeholder for the Roulette game.")
        print("Please check back later for updates.")

def play_game():
    print(Fore.GREEN + "Welcome to the Casino!")

    player_chips = Chips(100)  # Start with 100 chips

    while True:
        print(Fore.CYAN + "\nWhich game would you like to play?")
        print("1. Blackjack")
        print("2. Exit")

        choice = input("Enter your choice (1-2): ")

        if choice == "1":
            blackjack = Blackjack(player_chips)
            blackjack.play()
        elif choice == "2":
            print(Fore.GREEN + "\nThanks for playing!")
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter a valid option.")

def main():
    print(Fore.GREEN + "This game was made by Zazaman4000 \u00A9")
    play_game()

if __name__ == "__main__":
    main()
