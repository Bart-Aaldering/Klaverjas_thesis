import numpy as np
import random
import pandas as pd



class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        # self.id = 

    #Returns the rank of the card given the trump suit
    def order(self, trump_suit):
        if self.suit == trump_suit:
            return [8, 9, 14, 12, 15, 10, 11, 13][self.value - 7]
        return [0, 1, 2, 6, 3, 4, 5, 7][self.value - 7]

    #Returns the value of the card given the trump suit
    def points(self, trump_suit):
        if self.suit == trump_suit:
            return [0, 0, 14, 10, 20, 3, 4, 11][self.value - 7]
        return [0, 0, 0, 10, 2, 3, 4, 11][self.value - 7]

def team(player):
    return player % 2

def other_team(player):
    return (player + 1) % 2

meld_20 = []
meld_50 = []
meld_100 = []
suits = ['k', 'h', 'r', 's']
values = [7, 8, 9, 10, 11, 12, 13, 14]
for suit in suits:
    for idx in range(7,13):
        meld_20.append({Card(value, suit)
                        for value in range(idx, idx + 3)})
    for idx in range(7,12):
        meld_50.append({Card(value, suit)
                        for value in range(idx, idx + 4)})


for value in values:
    meld_100.append({Card(value, suit) for suit in suits})



#Checks whether there are meld points on the board
def meld_points(trick, trump_suit):
    for meld in meld_100:
        if meld <= set(trick):
            return 100

    points = 0
    royal = {Card(trump_suit, 12), Card(trump_suit, 13)}
    if royal <= set(trick):
        points = 20

    for meld in meld_50:
        if meld <= set(trick):
            return points + 50
    for meld in meld_20:
        if meld <= set(trick):
            return points + 20
    return points


class Trick:
    def __init__(self, starting_player):
        self.cards = []
        self.starting_player = starting_player

    #Adds the played card to itself
    def add_card(self, card):
        self.cards.append(card)

    #Checks whether the trick is over
    def is_complete(self):
        return len(self.cards) == 4

    #Returns the leading suit of the trick
    def leading_suit(self):
        if self.cards:
            return self.cards[0].suit

    #Returns the winner of the trick
    def winner(self, trump_suit):
        highest = self.cards[0] 
        for card in self.cards:
            if (card.order(trump_suit) > highest.order(trump_suit) and
                (card.suit == self.leading_suit() or
                 card.suit == trump_suit)):
                highest = card        
        return (self.starting_player + self.cards.index(highest)) % 4

    #Returns the highest card currently played in this trick
    def highest_card(self, trump_suit):
        highest = self.cards[0] 
        for card in self.cards:
            if (card.order(trump_suit) > highest.order(trump_suit) and
                (card.suit == self.leading_suit() or
                 card.suit == trump_suit)):
                highest = card 
        return highest

    #Returns the player that is currently at turn
    def to_play(self):
        return (self.starting_player + len(self.cards)) % 4

    #Returns the total points of the played cards in this trick
    def points(self, trump_suit):
        return sum(card.points(trump_suit) for card in self.cards)
    
    #Returns the highest played trump card
    def highest_trump(self, trump_suit):
        return max(self.cards,
                   default=Card(7, trump_suit).order(trump_suit),
                   key=lambda card: card.order(trump_suit))

    #Returns the meld points in this trick
    def meld(self, trump_suit):
        return meld_points(self.cards, trump_suit)

class Round:
    def __init__(self, starting_player, trump_suit):
        self.starting_player = starting_player
        self.trump_suit = trump_suit
        self.tricks = [Trick(starting_player)]

        self.cards = [Card(value, suit) for value in values for suit in suits]

        self.points = [0, 0]
        self.meld = [0, 0]
        
    def deal_cards(self):
        random.shuffle(self.cards)
        self.player_hands = [self.cards[:8], self.cards[8:16], self.cards[16:24], self.cards[24:]]
    
    # def deal_cards(self, seed):
    #     random.seed(seed)
    #     random.shuffle(self.cards)
    #     self.player_hands = [self.cards[:8], self.cards[8:16], self.cards[16:24], self.cards[24:]]

    #Returns the legal moves a player could make based on the current hand and played cards
    def legal_moves(self):
        hand = self.player_hands[self.to_play()]
        trick = self.tricks[-1]
        leading_suit = trick.leading_suit()

        if leading_suit is None:
            return hand

        follow = []
        trump = []
        trump_higher = []
        highest_trump_value = trick.highest_trump(
            self.trump_suit).order(self.trump_suit)
        for card in hand:
            if card.suit == leading_suit:
                follow.append(card)
            if card.suit == self.trump_suit:
                trump.append(card)
                if card.order(self.trump_suit) > highest_trump_value:
                    trump_higher.append(card)

        if follow and leading_suit != self.trump_suit:
            return follow

        return trump_higher or trump or hand   
    
    #Checks whether the round is complete
    def is_complete(self):
        return len(self.tricks) == 8 and self.tricks[-1].is_complete()

    #Plays the card in a trick
    def play_card(self, card):
        current_player = self.to_play()
        self.tricks[-1].add_card(card)
        self.player_hands[current_player].remove(card)
        

    #Returns the player currently at turn    
    def to_play(self):
        return self.tricks[-1].to_play()
    
    #Checks whether the trick is complete and handles all variables
    def complete_trick(self):
        trick = self.tricks[-1]
        if trick.is_complete():
            winner = trick.winner(self.trump_suit)
            points = trick.points(self.trump_suit)
            meld = trick.meld(self.trump_suit)
            self.points[team(winner)] += points
            self.meld[team(winner)] += meld

            if len(self.tricks) == 8:
                self.points[team(winner)] += 10
                us = team(self.starting_player)
                them = other_team(self.starting_player)

                if (self.points[us] + self.meld[us] <=
                        self.points[them] + self.meld[them]):
                    self.points[them] = 162
                    self.meld[them] += self.meld[us]
                    self.points[us] = 0
                    self.meld[us] = 0
                elif self.is_pit():
                    self.meld[us] += 100
            else:
                self.tricks.append(Trick(winner))
            return True
        return False

    #Checks whether all tricks are won by one team
    def is_pit(self):
        for trick in self.tricks:
            if team(self.starting_player) != team(trick.winner(self.trump_suit)):
                return False
        return True


def print_moves(moves):
    print(list(map(card_to_string, moves)))

def card_to_string(card):
    int_to_card = ["7", "8", "9", "10", "jack", "queen", "king", "ace"]
    string_to_card = {"k": "Clubs", "r": "Diamonds", "h": "Hearts", "s": "Spades"}
    return int_to_card[card.value-7] + string_to_card[card.suit]

def print_hands(hands):
    print("Hands:")
    print(list(map(card_to_string, hands[0])))
    print(list(map(card_to_string, hands[1])))
    print(list(map(card_to_string, hands[2])))
    print(list(map(card_to_string, hands[3])))

def main():
    points = [0, 0]
    meld = [0, 0]
    import time 
    start = time.time()
    for _ in range(100):
        round = Round(0, 'k')
        round.deal_cards()

        # print_hands(round.player_hands)



        for _ in range(8):
            for _ in range(4):
                # print("CENTER:")
                # print_moves(round.tricks[-1].cards)
                # print_hands(round.player_hands)
                legal_moves = round.legal_moves()
                # print("LEGAL MOVES:")
                # print_moves(legal_moves)
                # print("TO PLAY:")
                # print(round.to_play())
                round.play_card(random.choice(legal_moves))
                
            # print("ROUND COMPLETE")
            round.complete_trick()
            # print_moves(round.tricks[-1].cards)
        # print_moves(round.tricks[-1].cards)
        # print("CENTER:")
        # print_moves(round.tricks[-1].cards)
        # print_hands(round.player_hands)
        # print("LEGAL MOVES:")
        # legal_moves = round.legal_moves()
        # print_moves(legal_moves)
        # print("TO PLAY:")
        # print(round.to_play())
        # print(round.points)
        print(round.points)
        points[0] += round.points[0]
        points[1] += round.points[1]
    end = time.time()
    print("Time: ", end - start)
    print("Points: ", points)
    print("Meld: ", meld)

def main2():
    trick = Trick(0)
    trick.add_card(Card(7, 'k'))
    trick.add_card(Card(8, 'k'))
    trick.add_card(Card(9, 'k'))
    trick.add_card(Card(7, 'h'))
    trick2 = Trick(0)
    trick2.add_card(Card(7, 'k'))
    trick2.add_card(Card(8, 'k'))
    trick2.add_card(Card(9, 'k'))
    trick2.add_card(Card(7, 'h'))
    if set(trick.cards) <= set(trick2.cards):
        print("JAA")
    print("hier", trick.meld('h'))
    print_moves(set(trick.cards))
    return
    for i in range(len(meld_20)):
        print_moves((meld_20[i]))


if __name__ == '__main__':
    main()
