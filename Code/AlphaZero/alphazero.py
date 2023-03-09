import numpy as np
import random
import copy
import itertools
import time

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
    
    def expand(self):
        for card in self.state.legal_moves():
            # temp_state = copy.deepcopy(self.state)
            # new_state = self.state
            # self.state = temp_state
            # new_card = [new_card for new_card in new_state.legal_moves() if new_card.id == card.id][0]
            new_state = copy.deepcopy(self.state)
            new_card = [new_card for new_card in new_state.legal_moves() if new_card.id == card.id][0]

            new_state.play_card(new_card)
            self.children.append(Node(new_state, self, card))


    def select_child_random(self):
        # print("Node", self, self.visits)
        return random.choice(self.children)
    
    def select_child_ucb(self):
        # print("Node", self, self.visits)
        # print("Children", [child.visits for child in self.children])
        c = 1
        ucbs = []
        for child in self.children: # HIER
            if child.visits == 0:
                return child
            # if self.visits == 0:
            #     raise Exception("Visits is 0")
            ucbs.append(child.score / child.visits + c * np.sqrt(np.log(self.visits) / child.visits))
        index_max = np.argmax(np.array([ucbs]))
        return self.children[index_max]
    
class AlphaZero_player:
    def __init__(self, round: Round, player_position: int):
        self.player_position = player_position
        self.state = State(round, player_position)
        self.node = Node(self.state)
        # self.policy_network = policy_network()
    
    def update_state(self, move: int):

        # Tranform the move to a card object
        if self.state.current_player == self.player_position:
            cards = self.state.hands[self.state.current_player]
        else:
            cards = self.state.other_players_cards
        move = card_transform(move, self.state.trump_suit)
        for card in cards:
            if card.id == move:
                new_move = card
                break
        
        self.state.play_card(new_move, simulation=False)
        if self.state != self.node.state:
            raise Exception("State is not the same")
    
    def get_move(self):     
        card_id = self.mcts().id
        
        if type(self.state.trump_suit) == str:
            raise Exception("Trump suit is not set")
        
        return card_untransform(card_id, self.state.trump_suit)

    def mcts(self):
        
        root = Node(self.node.state)

        # current_node = copy.deepcopy(root)
        current_node = root
        number_of_simulations = 5
        tijd = 10

        # Determination
        current_node.state.determine()
        for _ in range(tijd):

            # Selection
            current_node = self.selection()
            
            # Expansion
            if not current_node.state.round_complete():
                current_node.expand()
                current_node = current_node.select_child_random()

            # Simulation
            explore_round = copy.deepcopy(current_node.state)
            points = 0
            for _ in range(number_of_simulations):
                while not explore_round.round_complete():
                    
                    move = random.choice(list(explore_round.legal_moves()))
                    
                    explore_round.play_card(move)
                    
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
                
        return best_child.move

    def selection(self, current_node: Node):
        # zodra er ee nacti is die niet in de huidige tree zit stop
        
        while not current_node.state.round_complete() and set(current_node.state.legal_moves()) - set(current_node.children) == set():
            current_node = current_node.select_child_ucb()