from __future__ import annotations # To use the class name in the type hinting

import random

from typing import List

from rounds import Round
from AlphaZero.trick import Trick
from AlphaZero.card import Card
from AlphaZero.helper import *


class State:
    def __init__(self, round: Round, own_position: int) -> None:
        self.own_position = own_position
        
        self.current_player = round.current_player
        self.declaring_team = round.declaring_team
        
        # The hand of the transformed to the game state representation
        own_hand_as_id = [card_transform(card.id, ['k', 'h', 'r', 's'].index(round.trump_suit)) 
                            for card in round.player_hands[self.own_position]]
        
        not_own_hand_as_id = set([suit*10 + value for suit in range(4) for value in range(8)]) - set(own_hand_as_id)
        
        # Cards that other players can have
        self.other_players_cards = set([Card(id) for id in not_own_hand_as_id]) 
        
        self.hands = [set() for i in range(4)]
        self.hands[own_position] = set([Card(id) for id in own_hand_as_id])
        
        # self.possible_cards = [self.other_players_cards for i in range(4)]
        # self.possible_cards[self.own_position] = self.hands[own_position]
        
        self.centre = Trick(self.current_player)
        
        self.has_lost = [False, False]
        self.cards_left = [8, 8, 8, 8]
        # The current score of the round
        self.points = [0, 0]
        self.meld = [0, 0]
    
    def __eq__(self, other: State) -> bool:
        raise NotImplementedError
        return self.__dict__ == other.__dict__
    
    def __hash__(self) -> int:
        raise NotImplementedError
        return hash(tuple(sorted(self.__dict__.items())))
    
    def determine(self):
        other_players = [i for i in range(4) if i != self.own_position]
        other_players_cards = list(self.other_players_cards)
        for player in other_players:
            self.hands[player] = set()
            for _ in range(self.cards_left[player]):
                choice = random.sample(other_players_cards, 1)[0]
                self.hands[player].add(choice)
                other_players_cards.remove(choice)
        # Kies een kaart per speler
    
    def legal_moves(self) -> List[Card]:

        hand = self.hands[self.current_player]

        leading_suit = self.centre.leading_suit()

        if leading_suit is None:
            return hand

        follow = []
        trump = []
        trump_higher = []
        highest_trump_value = self.centre.highest_trump().order()
        current_winner = self.centre.winner()
        for card in hand:
            if card.suit == leading_suit:
                follow.append(card)
            if card.suit == 0:
                trump.append(card)
                if card.order() > highest_trump_value:
                    trump_higher.append(card)

        if follow and leading_suit != 0:
            return follow

        if (current_winner+self.current_player) % 2 == 0:
            return hand
        
        return trump_higher or trump or hand

    def play_card(self, card: Card, simulation: bool = True):
        self.centre.add_card(card)

        self.cards_left[self.current_player] -= 1
        
        if simulation:
            self.hands[self.current_player].remove(card)

        else:
            if self.current_player != self.own_position:
                self.other_players_cards.remove(card)
            else:
                self.hands[self.current_player].remove(card)

        if self.centre.trick_complete():
            
            winner = self.centre.winner()
            team_winner = team(winner)
            
            self.has_lost[1-team_winner] = True
            
            points = self.centre.points()
            meld = self.centre.meld()
            
            self.points[team_winner] += points
            self.meld[team_winner] += meld

            if self.round_complete():

                # Winner of last trick gets 10 points
                self.points[team_winner] += 10
                defending_team = 1 - self.declaring_team
                
                # Check if the round has "nat"
                if (self.points[self.declaring_team] + self.meld[self.declaring_team] <=
                        self.points[defending_team] + self.meld[defending_team]):
                    self.points[defending_team] = 162
                    self.meld[defending_team] += self.meld[self.declaring_team]
                    self.points[self.declaring_team] = 0
                    self.meld[self.declaring_team] = 0
                
                # Check if the round has "pit"
                if not self.has_lost[0]:
                    self.meld[0] += 100
                elif not self.has_lost[1]:
                    self.meld[1] += 100
            else:
                self.centre = Trick(winner)
                self.current_player = winner
        else:
            self.current_player = (self.current_player+1) % 4
    
    def round_complete(self) -> bool:
        if self.centre.trick_complete() and self.hands[self.own_position] == set():
            return True
        return False

    def get_score(self, player: int) -> int:
        local_team = team(player)
        return self.points[local_team] - self.points[1-local_team] + self.meld[local_team] - self.meld[1-local_team]


    


