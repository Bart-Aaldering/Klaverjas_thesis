import numpy as np

from helper import *


class Trick:
    def __init__(self, starting_player: int):
        self.cards = []
        self.starting_player = starting_player
    
    def add_card(self, card: int):
        self.cards.append(card)

    #Checks whether the trick is over
    def is_complete(self):
        return len(self.cards) == 4

    #Returns the leading suit of the trick
    def leading_suit(self):
        if self.cards:
            return card_to_suit(self.cards[0])

    #Returns the winner of the trick
    def winner(self, trump_suit: int):
        highest = self.cards[0]
        highest_order = card_to_order(highest, trump_suit)
        for card in self.cards:
            card_suit = card_to_suit(card)
            if (card_to_order(card, trump_suit) > highest_order and
                (card_suit == self.leading_suit() or
                 card_suit == trump_suit)):
                highest = card
                highest_order = card_to_order(highest, trump_suit)
        return (self.starting_player + self.cards.index(highest)) % 4

    #Returns the player that is currently at turn
    def to_play(self):
        return (self.starting_player + len(self.cards)) % 4

    #Returns the total points of the played cards in this trick
    def points(self, trump_suit: int):
        return sum(card_to_points(card, trump_suit) for card in self.cards)

    #Returns the meld points in this trick
    def meld(self, trump_suit: int):
        values = card_to_value(self.cards)
        sorted = self.cards.sort()
        point = 0

        # King and Queen of trump suit
        if trump_suit*10 + 5 in self.cards and trump_suit*10 + 6 in self.cards:
            point += 20

        # four consecutive cards of the same suit
        if card_to_suit(sorted[0]) == card_to_suit(sorted[3]) and card_to_value(sorted[0]) == card_to_value(sorted[3]) - 3:
            return point + 50

        # three consecutive cards of the same suit
        if ((card_to_suit(sorted[0]) == card_to_suit(sorted[2]) and card_to_value(sorted[0]) == card_to_value(sorted[2]) - 2) or
            (card_to_suit(sorted[1]) == card_to_suit(sorted[3]) and card_to_value(sorted[1]) == card_to_value(sorted[3]) - 2)):
            return point + 20
        
        # four cards of value Jack
        if np.all(values == 4):
            return 200

        # four cards of the same face value
        if len(set(values)) == 1:
            return 100

    #Returns the highest played trump card
    def highest_trump(self, trump_suit: int):
        return max(self.cards,
                   default=card_to_order(10*trump_suit, trump_suit),
                   key=lambda card: card_to_order(card, trump_suit))
    
    #Returns the highest card currently played in this trick
    def highest_card(self, trump_suit: int):
        highest = self.cards[0] 
        for card in self.cards:
            card_suit = card_to_suit(card)
            if (card_to_order(card, trump_suit) > card_to_order(highest, trump_suit) and
                (card_suit == self.leading_suit() or
                 card_suit == trump_suit)):
                highest = card 
        return highest
