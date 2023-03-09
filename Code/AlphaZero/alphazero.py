import numpy as np
import random
import copy
import itertools

from typing import List

from rounds import Round
# from tricks import Trick
from AlphaZero.state import State
from AlphaZero.helper import card_transform, card_untransform
# from helper import *


class Node:
    def __init__(self, state: State, parent=None, move=None):
        self.state = state
        self.children = []
        self.parent = parent
        self.move = move
        self.score = 0
        self.visits = 0
    
    def expand(self, alpha_player):

        if self.state.current_player == alpha_player:
            # print("Expand")
            for card in self.state.legal_moves(None):
                new_round = copy.deepcopy(self.state)
                new_card = [new_card for new_card in new_round.legal_moves(None) if new_card.id == card.id][0]
                new_round.play_card(new_card)
                self.children.append(Node(new_round, self, card))
        else:
            # print("Expand2")

            
            possible_hands = list(itertools.combinations(set(self.state.possible_cards[self.state.current_player]), 8-self.state.number_of_tricks))
            possible_hands = random.sample(possible_hands, min(100, len(possible_hands)))
            # print("TYPE", type(possible_hands[0]))
            # print("LEN", len(possible_hands))
            for hand in possible_hands:
                moves = self.state.legal_moves(hand)
                for card in moves:
                    new_round = copy.deepcopy(self.state)
                    new_card = [new_card for new_card in new_round.possible_cards[new_round.current_player] if new_card.id == card.id][0]
                    # new_card = [new_card for new_card in new_round.legal_moves(hand) if new_card.id == card.id][0]
                    new_round.play_card(new_card)
                    self.children.append(Node(new_round, self, card))

    def select_child_random(self):
        # print("Node", self, self.visits)
        return random.choice(self.children)
    
    def select_child_ucb(self):
        # print("Node", self, self.visits)
        # print("Children", [child.visits for child in self.children])
        c = 1.41
        ucbs = []
        for child in self.children:
            if child.visits == 0:
                return child
            if self.visits == 0:
                raise Exception("Visits is 0")
            ucbs.append(child.score / child.visits + c * np.sqrt(np.log(self.visits) / child.visits))
        index_max = np.argmax(np.array([ucbs]))
        return self.children[index_max]    
    
class AlphaZero_player:
    def __init__(self, round: Round, player_position: int):
        self.player_position = player_position
        # self.policy_network = policy_network()
        self.game_state = State(round, player_position)

    # def new_round(self, round: Round):
    #     self.current_trick = 0 # A number representing the current trick 
    
    #     self.game_state = State(round)
    
    def update_state(self, move: int):
        cards = self.game_state.possible_cards[self.game_state.current_player]
        # print("State moves ", legal_moves)
        # print("Hand", self.game_state.possible_cards)
        # print("Current player", self.game_state.current_player)
        move = card_transform(move, self.game_state.trump_suit)
        # print("Move", move)	
        for card in cards:
            if card.id == move:
                new_move = card
                break
        self.game_state.play_card(new_move)
    
    def get_move(self):     
        card_id = self.mcts().id
        if type(self.game_state.trump_suit) == str:
            raise Exception("Trump suit is not set")
        return card_untransform(card_id, self.game_state.trump_suit)

    def mcts(self):
        
        root = Node(self.game_state)
        current_node = root
        
        number_of_simulations = 50
        tijd = 10


        for i in range(tijd):
        
            # Selection
            while not current_node.state.round_complete() and current_node.children:
                current_node = current_node.select_child_ucb()
                
            # Expansion
            if not current_node.state.round_complete():
                current_node.expand(self.player_position)
                current_node = current_node.select_child_random()
            
            # Simulation
            explore_round = copy.deepcopy(current_node.state)
            points = 0
            for _ in range(number_of_simulations):
                while not explore_round.round_complete():

                    posible_moves = random.sample(explore_round.possible_cards[explore_round.current_player], 8-explore_round.number_of_tricks)
                    
                    explore_round.play_card(random.choice(explore_round.legal_moves(posible_moves)))
                points += explore_round.get_score(self.player_position)
            points /= number_of_simulations
            
            # Backpropagation
            while current_node.parent is not None:
                current_node.visits += 1
                current_node.score += points
                current_node = current_node.parent
            root.visits += 1
            
            
        
        best_score = -1
        for child in root.children:
            score = child.visits
            if score > best_score:
                best_score = score
                best_child = child
        # print("hallo2", [card.id for card in round.legal_moves()])
        # print(best_child.move.id)
        # return [new_card for new_card in new_round.legal_moves() if new_card.id == card.id][0]
        return best_child.move

    def mcts2(self, round: Round):
        number_of_simulations = 50
        root = Node(round)
        # current_node = copy.deepcopy(root)
        current_node = root
        tijd = 10
        # print("hallo", round.legal_moves())
        for i in range(tijd):
        
            # Selection
            while not current_node.state.is_complete() and current_node.children:
                current_node = current_node.select_child_ucb()
                
            # Expansion
            if not current_node.state.is_complete():
                current_node.expand(self.player_position)
                current_node = current_node.select_child_random()
            
            # Simulation
            explore_round = copy.deepcopy(current_node.state)
            points = 0
            for _ in range(number_of_simulations):
                while not explore_round.is_complete():
                    explore_round.play_card(random.choice(explore_round.legal_moves()))
                points += explore_round.get_score(self.player_position)
            points /= number_of_simulations
            
            # Backpropagation
            while current_node.parent is not None:
                current_node.visits += 1
                current_node.score += points
                current_node = current_node.parent
            root.visits += 1
            
            
        
        best_score = -1
        for child in root.children:
            score = child.visits
            if score > best_score:
                best_score = score
                best_child = child
        # print("hallo2", [card.id for card in round.legal_moves()])
        # print(best_child.move.id)
        # return [new_card for new_card in new_round.legal_moves() if new_card.id == card.id][0]
        return best_child.move
        
    # def old(self, round: Round):
    #     # return move
    #     for i in range(1):
    #         node = root
    #         current_node = node
    #         # selection
    #         while not current_node.round.is_complete() and current_node.children:
    #             current_node.play_card(current_node.round.legal_moves())
    #             if round.current_player == self.player_position:
                    
    #                 game_state = current_node.round.round_to_game_state(round)
    #                 policy = np.array(self.policy_network(self.game_state)[0])

    #                 choice = np.random.choice(list(range(8)), p=policy)
    #                 cards = self.game_state[:8]
    #                 cards = [self.card_untranform(card, round.trump_suit) for card in self.game_state[:8]]
    #                 legalmoves = round.legal_moves()
                    
    #                 print("hier", cards, legalmoves)
    #                 while cards[choice] not in legalmoves:
    #                     policy[choice] = 0
    #                     # print(policy)
    #                     policy = policy/np.sum(policy)
    #                     choice = np.random.choice(list(range(8)), p=policy)
                        
            

    #                 round.play_card(cards[choice])
    #                 self.player_position = (self.player_position+1)%4
    #                 print("played card", cards[choice])
    #                 print(round.tricks[-1].cards)
    #                 print(round.player_hands)
    #                 print(round.legal_moves())
    #             else:
    #                 hand = round.player_hands[round.current_player]
                    
    #         points += round.points[self.player_position%2]
    #     print(points)
    
    # def set_state_with_round(self, round: Round):
    #     own_hand = round.player_hands[self.own_position] 
    #     # The hand of the tranformed to the game state representation
    #     self.own_hand = [self.card_transform(card.id, round.trump_suit) for card in own_hand] + [-1]*(8-len(own_hand))
        
    #     # 1 if the team of Player is declaring, 0 if the team of Player not declaring
    #     if round.declaring_team == self.own_position%2:
    #         self.declaring = 1
    #     else:
    #         self.declaring = 0
        
    #     # Creating the game state representation of the tricks
    #     played_tricks = [self.trick_transform(trick) for trick in reversed(round.tricks)] # The tricks that have been played starting from Player
    #     unplayed_tricks = [[-1, -1, -1, -1]]*(8-len(round.tricks))  # The tricks that have not been played
    #     tricks = played_tricks + unplayed_tricks # Combination of the played and unplayed tricks
    #     self.tricks = [item for sublist in tricks for item in sublist] # Flatten the list
    
    #     # The current score of the round
    #     self.score = round.points
       
    # def trick_transform(self, trick: Trick) -> list[int]:
    #     "Makes the trick start with the cards of Player"
    #     cards = [-1, -1, -1, -1]
    #     for i, card in enumerate(trick.cards):
    #         cards[(i+trick.starting_player+(3-self.own_position))%4] = card
    #     return cards
    
    # def card_transform(self, card: int, trump_suit: int) -> int:
    #     "Makes cards of the trump suit to have suit 0 and cards with suit 0 have suit trump_suit"
    #     suit = card_to_suit(card)
    #     if suit == trump_suit:
    #         return card_to_value(card)
    #     elif suit == 0:
    #         return trump_suit*10 + card_to_value(card)
    #     else:
    #         return card
    
    # def card_untranform(self, card: int, trump_suit: int) -> int:
    #     "Makes cards of the trump suit to have suit trump_suit and cards with suit trump_suit have suit 0"
    #     suit = card_to_suit(card)
    #     if suit == 0:
    #         return trump_suit*10 + card_to_value(card)
    #     elif suit == trump_suit:
    #         return card_to_value(card)
    #     else:
    #         return card