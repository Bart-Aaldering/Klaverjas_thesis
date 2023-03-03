
from helper import *
from trick import Trick

import random

class Round:
    def __init__(self, starting_player: int, trump_suit: int, declarer: int):
        # players:
        #   2
        #  1 3
        #   0
        # team 0 is 0 and 2, team 1 is 1 and 3
        
        self.current_player = starting_player
        self.declaring_team = team(declarer)
        self.trump_suit = trump_suit
        self.tricks = [Trick(starting_player)]

        self.cards = [strings_to_id(value, suit) for suit in suits_list for value in values_list]

        self.points = [0, 0]
        self.meld = [0, 0]
        self.pit = [0, 0]
        self.wins = [0, 0]


        self.cardsleft = [self.cards[:8], self.cards[8:16], self.cards[16:24], self.cards[24:]]
        for i in range(4):
            if [0,1,2,3][i] == self.trump_suit:
                order = [8, 9, 14, 12, 15, 10, 11, 13]
            else:
                order = [0, 1, 2, 6, 3, 4, 5, 7]
            self.cardsleft[i] = [i for _, i in sorted(zip(order, self.cardsleft[i]))]
                
        self.deal_cards()
        
    def deal_cards(self):
        random.shuffle(self.cards)
        self.player_hands = [self.cards[:8], self.cards[8:16], self.cards[16:24], self.cards[24:]]

    #Returns the legal moves a player could make based on the current hand and played cards
    def legal_moves(self):
        hand = self.player_hands[self.current_player]
        trick = self.tricks[-1]
        leading_suit = trick.leading_suit()

        # There has not yet been played a card, all cards may be played.
        if leading_suit is None:
            return hand

        follow = []
        trump = []
        trump_higher = []
        highest_trump_value = card_to_order(trick.highest_trump(self.trump_suit), self.trump_suit)
        for card in hand:
            if card_to_suit(card) == leading_suit:
                follow.append(card)
            if card_to_suit(card) == self.trump_suit:
                trump.append(card)
                if card_to_order(card, self.trump_suit) > highest_trump_value:
                    trump_higher.append(card)

        if follow and leading_suit != self.trump_suit:
            return follow

        return trump_higher or trump or hand   
    
    #Checks whether the round is complete
    def is_complete(self):
        return len(self.tricks) == 8 and self.tricks[-1].is_complete()

    #Plays the card in a trick
    def play_card(self, card):
        if card not in self.legal_moves():
            raise Exception("Illegal move")
        self.tricks[-1].add_card(card)
        self.player_hands[self.current_player].remove(card)
        self.current_player = (self.current_player+1) % 4
        
        self.complete_trick()
           
    #Checks whether the trick is complete and handles all variables
    def complete_trick(self):
        trick = self.tricks[-1]
        if trick.is_complete():
            self.current_player = trick.winner(self.trump_suit)
            winner = trick.winner(self.trump_suit)
            points = trick.points(self.trump_suit)
            
            for card in trick.cards:
                self.cardsleft[card_to_suit(card)].remove(card)
            
            meld = trick.meld(self.trump_suit)

            self.points[team(winner)] += points
            self.meld[team(winner)] += meld

            if len(self.tricks) == 8:
                if self.points[0] > self.points[1]:
                    self.wins[0] += 1
                elif self.points[1] > self.points[0]:
                    self.wins[1] += 1
                else:
                    self.wins[0] += 0.5
                    self.wins[1] += 0.5
                self.points[team(winner)] += 10
                defending_team = 1 - self.declaring_team

                if (self.points[self.declaring_team] + self.meld[self.declaring_team] <=
                        self.points[defending_team] + self.meld[defending_team]):
                    self.points[defending_team] = 162
                    self.meld[defending_team] += self.meld[self.declaring_team]
                    self.points[self.declaring_team] = 0
                    self.meld[self.declaring_team] = 0
                elif self.is_pit():
                    self.pit[self.declaring_team] += 1
                    self.meld[self.declaring_team] += 100
            else:
                self.tricks.append(Trick(winner))
                
            return True
        return False

    #Checks whether all tricks are won by one team
    def is_pit(self):
        for trick in self.tricks:
            if team(self.declaring_team) != team(trick.winner(self.trump_suit)):
                return False
        return True

    def get_highest_card(self, suit):
        if self.cardsleft[suit]:
            return self.cardsleft[suit][-1]
        return -1
