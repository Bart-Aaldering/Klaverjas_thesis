

from typing import List

from rounds import Round
from AlphaZero.trick import Trick
from AlphaZero.card import Card
from AlphaZero.helper import *


class State:
    def __init__(self, round: Round, own_position: int) -> None:
        self.own_position = own_position
        self.trump_suit = ['k', 'h', 'r', 's'].index(round.trump_suit)
        
        self.current_player = round.current_player
        self.declaring_team = round.declaring_team
        
        own_hand = round.player_hands[self.own_position] 
        # The hand of the transformed to the game state representation
        self.own_hand = [card_transform(card.id, ['k', 'h', 'r', 's'].index(round.trump_suit)) for card in own_hand]
        
        all_cards = set([suit*10 + value for suit in range(4) for value in range(8)])
        other_players_cards = list(all_cards - set(self.own_hand))
        other_players_cards = [Card(id) for id in other_players_cards]
        
        self.own_hand = [Card(id) for id in self.own_hand]
        self.possible_cards = [other_players_cards for i in range(4)]
        self.possible_cards[self.own_position] = self.own_hand

        # self.information_set_id = hash of the information set
        
        # 1 if the team of Player is declaring, 0 if the team of Player not declaring
        if round.declaring_team == self.own_position%2:
            self.declaring = 1
        else:
            self.declaring = 0
        
        self.centre = Trick(self.current_player)
        
        self.has_lost = [False, False]
        self.number_of_tricks = 0
        # The current score of the round
        self.points = [0, 0]
        self.meld = [0, 0]
    
    def legal_moves(self, hand: List[Card]) -> List[Card]:
        if hand is None:
            hand = self.possible_cards[self.current_player]
            if self.current_player != self.own_position:
                raise Exception("Not the current players turn")
            
        # print("hand", hand)
        if len(hand) == 0:
            print(self.possible_cards)
            raise Exception("No cards in hand")
        # print('centre', self.centre)
        leading_suit = self.centre.leading_suit()

        if leading_suit is None:
            # print("HIER1")
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
            # print("HIER2")
            return follow

        if (current_winner + self.current_player) % 2 == 0:
            # print("HIER3")
            return hand
        # print("HIER4")
        return trump_higher or trump or hand

    def play_card(self, card: Card):
        # print("play_card", card)
        # print("centre", self.centre)
        # print("current_player", self.current_player)
        # print("own_position", self.own_position)
        # print("possible_cards", self.possible_cards)
        self.centre.add_card(card)

        card_removed = False
        for i in range(4):
            if card in self.possible_cards[i]:
                self.possible_cards[i].remove(card)
                card_removed = True
                
        if not card_removed:
            raise Exception("Card not in hand")
        
        if self.centre.trick_complete():
            
            self.number_of_tricks += 1
            
            winner = self.centre.winner()
            team_winner = team(winner)
            
            self.has_lost[1-team_winner] = True
            
            points = self.centre.points()
            meld = self.centre.meld()
            
            self.points[team_winner] += points
            self.meld[team_winner] += meld

            if self.round_complete():
                # print("Round complete")

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
            self.current_player = (self.current_player + 1) % 4
    
    def round_complete(self):
        if self.number_of_tricks == 8:
            for i in range(4):
                if len(self.possible_cards[i]) != 0:
                    raise Exception("Not all cards played")
            return True
        return False

    def get_score(self, player: int) -> int:
        local_team = team(player)
        return self.points[local_team] - self.points[1-local_team] + self.meld[local_team] - self.meld[1-local_team]

    def set_state_with_round(self, round: Round):
        own_hand = round.player_hands[self.own_position] 
        # The hand of the transformed to the game state representation
        self.own_hand = [card_transform(card.id, round.trump_suit) for card in own_hand] + [-1]*(8-len(own_hand))
        
        # 1 if the team of Player is declaring, 0 if the team of Player not declaring
        if round.declaring_team == self.own_position%2:
            self.declaring = 1
        else:
            self.declaring = 0
        
        # # Creating the game state representation of the tricks
        # played_tricks = [self.trick_transform(trick) for trick in reversed(round.tricks)] # The tricks that have been played starting from Player
        # unplayed_tricks = [[-1, -1, -1, -1]]*(8-len(round.tricks))  # The tricks that have not been played
        # tricks = played_tricks + unplayed_tricks # Combination of the played and unplayed tricks
        # self.tricks = [item for sublist in tricks for item in sublist] # Flatten the list
    
        # The current score of the round
        self.points = round.points
       
    # def trick_transform(self, trick: Trick) -> list[int]:
    #     "Makes the trick start with the cards of Player"
    #     cards = [-1, -1, -1, -1]
    #     for i, card in enumerate(trick.cards):
    #         cards[(i+trick.starting_player+(3-self.own_position))%4] = card
    #     return cards
    


