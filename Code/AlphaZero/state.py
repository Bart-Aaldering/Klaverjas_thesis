from __future__ import annotations # To use the class name in the type hinting

import random
import copy

from typing import List, Set

from rounds import Round
from AlphaZero.trick import Trick
from AlphaZero.card import Card
from AlphaZero.helper import *


class State:
    def __init__(self, round: Round, own_position: int) -> None:
        self.own_position = own_position
        self.round = round
        self.current_player = round.current_player
        self.declaring_team = round.declaring_team
        
        # The hand of the transformed to the game state representation
        own_hand_as_id = [card_transform(card.id, ['k', 'h', 'r', 's'].index(round.trump_suit)) 
                            for card in round.player_hands[self.own_position]]
        

        not_own_hand_as_id = set([suit*10 + value for suit in range(4) for value in range(8)]) - set(own_hand_as_id)
        
        # Cards that other players can have
        # self.other_players_cards = set([Card(id) for id in not_own_hand_as_id])
        # other_players_cards = set([Card(id) for id in not_own_hand_as_id])
        
        self.hands = [set() for i in range(4)]
        self.hands[own_position] = set([Card(id) for id in own_hand_as_id])
        
        self.possible_cards = [set([Card(id) for id in not_own_hand_as_id]) for _ in range(4)]
        self.possible_cards[own_position] = set([Card(id) for id in own_hand_as_id])
        
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
    
    
    def find_card_configuration(self, hand: List[set], possible_cards: List[list], player: int, num_cards_to_add: List[int]) -> bool:
        if player == 3:
            if num_cards_to_add != [0, 0, 0]:
                raise Exception("Not all cards added")
            return True
        elif num_cards_to_add[player] == 0:
            return self.find_card_configuration(hand, possible_cards, player+1, num_cards_to_add)
        else:
            wont_work = False
            cards = possible_cards[player].copy()
            for card in cards:
                has_card = []
                for other_player in range(player+1, 3):
                    if card in possible_cards[other_player]:
                        has_card.append(other_player)
                        possible_cards[other_player].remove(card)
                        if len(possible_cards[other_player]) < num_cards_to_add[other_player]:
                            wont_work = True
                            for removed_player in has_card:
                                possible_cards[removed_player].append(card)
                            break

                if wont_work:
                    wont_work = False
                    continue
                hand[player].add(card)
                num_cards_to_add[player] -= 1

                possible_cards[player].remove(card)

                if self.find_card_configuration(hand, possible_cards, player, num_cards_to_add):
                    return True
                
                possible_cards[player].append(card)
                
                num_cards_to_add[player] += 1
                hand[player].remove(card)
                for removed_player in has_card:
                    possible_cards[removed_player].append(card)

            return False
        
    def determine(self):         
        other_players = [0,1,2,3]
        other_players.pop(self.own_position)
        
        # print("possible_cards", self.possible_cards)
        # possible_cards = copy.deepcopy(self.possible_cards)
        
        real_hands_id = [[card_transform(card.id, ['k', 'h', 'r', 's'].index(self.round.trump_suit)) 
                            for card in self.round.player_hands[i]] for i in range(4)]
        real_hands = [{Card(id) for id in hand} for hand in real_hands_id]

        # print("real hand2", real_hands)
        # for i in range(4):
        #     if real_hands[i] - possible_cards[i] != set():
        #         # print(possible_cards)
        #         raise Exception("Real hand not possible")
        
        possible_cards = [list(cards) for cards in self.possible_cards]
        # print("HIER", possible_cards)
        # print(self.own_position)
        possible_cards.pop(self.own_position)
        for i in possible_cards:
            random.shuffle(i)
        hand = [set(), set(), set()]
        cards_left = copy.deepcopy(self.cards_left)
        # cards_left = self.cards_left.copy()
        cards_left.pop(self.own_position)
        
        if not self.find_card_configuration(hand, possible_cards, 0, cards_left):
            raise Exception("Could not find a card configuration")
        if cards_left != [0, 0, 0]:
            # print(possible_cards)
            # print(hand)
            # print(cards_left)
            # print(self.cards_left)
            raise Exception("Not all cards added1")
        possible_cards = copy.deepcopy(self.possible_cards)
        possible_cards = [list(cards) for cards in possible_cards]
        # print("HIER", possible_cards)
        # print(self.own_position)
        possible_cards.pop(self.own_position)
        for i in range(3):
            if hand[i] - set(possible_cards[i]) != set():
                # print("hand", hand)
                # print(possible_cards)
                # print(self.round.player_hands)
                # print(self.round.trump_suit)
                # print(self.own_position)
                raise Exception("Not all cards added2")
        for index, player in enumerate(other_players):
            self.hands[player] = hand[index]
            if len(hand[index]) != self.cards_left[player]:
                raise Exception("Not all cards added3")



    def update_possible_cards(self, played_card: Card):
        
        # remove played card from all players possible_cards
        for player in range(4):
            self.possible_cards[player].discard(played_card)
            
        if self.current_player == self.own_position:
            return
            
        leading_suit = self.centre.leading_suit()
        if leading_suit is None:
            return

        if played_card.suit != leading_suit:
            # remove all cards of the leading suit from the current player
            self.possible_cards[self.current_player] -= {Card(leading_suit*10 + i) for i in range(8)}
            
            if played_card.suit != 0:
                # remove all trumps from the current player
                self.possible_cards[self.current_player] -= {card for card in self.possible_cards[self.current_player] 
                                                             if card.id in {0,1,2,3,4,5,6,7}}
            else:
                if (highest_trump_order := self.centre.highest_trump().order()) > played_card.order():
                    # remove all trump cards higher then the highest trump card from the current player
                    self.possible_cards[self.current_player] -= {card for card in self.possible_cards[self.current_player] 
                                                                 if card.id in [0,1,5,6,3,7,2,4][highest_trump_order-8:]}
        
        for i in range(4):
            real_hand_id = [card_transform(card.id, ['k', 'h', 'r', 's'].index(self.round.trump_suit)) 
                            for card in self.round.player_hands[i]]
            real_hand = set([Card(id) for id in real_hand_id])
            if real_hand - self.possible_cards[i] != set():
                raise Exception("Not all cards added")
    
    def legal_moves(self) -> Set[Card]:
        hand = self.hands[self.current_player]

        leading_suit = self.centre.leading_suit()

        if leading_suit is None:
            return hand

        follow = set()
        trump = set()
        trump_higher = set()
        highest_trump_value = self.centre.highest_trump().order()
        for card in hand:
            if card.suit == leading_suit:
                follow.add(card)
            if card.suit == 0:
                trump.add(card)
                if card.order() > highest_trump_value:
                    trump_higher.add(card)

        if follow:
        # if follow and leading_suit != 0:
            return follow

        # current_winner = self.centre.winner()
        # if (current_winner+self.current_player) % 2 == 0:
        #     return hand
        
        return trump_higher or trump or hand

    def play_card(self, card: Card, simulation: bool = True):
        if simulation:
            if card not in self.legal_moves():
                # print(self.legal_moves(), card)
                raise ValueError(f"Card {card} is not a legal move")
            self.hands[self.current_player].remove(card)
        else:
            self.update_possible_cards(card)
            if self.current_player != self.own_position:
                pass
                # self.other_players_cards.remove(card)
            else:
                self.hands[self.current_player].remove(card)
                             
        self.centre.add_card(card)

        self.cards_left[self.current_player] -= 1
        
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
        if self.centre.trick_complete() and len(self.hands[self.own_position]) == 0:
            return True
        return False

    def get_score(self, player: int) -> int:
        local_team = team(player)
        return self.points[local_team] - self.points[1-local_team] + self.meld[local_team] - self.meld[1-local_team]


    


