from __future__ import annotations # To use the class name in the type hinting

import numpy as np
import random
import copy
import itertools
import time

from typing import List


from AlphaZero.card import Card
from rounds import Round
# from tricks import Trick
from AlphaZero.state import State
from AlphaZero.helper import card_transform, card_untransform
# from helper import *


class Node:
    def __init__(self, state: State, parent: Node = None, move: Card = None):
        self.state = state
        self.children = set()
        self.parent = parent
        self.move = move
        self.score = 0
        self.visits = 0
    
    def __repr__(self) -> str:
        return f"Node({self.move}, {self.score}, {self.visits})"
    
    def __eq__(self, other: Node) -> bool:
        # raise NotImplementedError
        return self.move == other.move
    
    def __hash__(self) -> int:
        # raise NotImplementedError
        return hash(self.move)

    def set_legal_children(self):
        legal_moves = self.state.legal_moves()
        self.legal_children = set()
        for move in legal_moves:
            new_state = copy.deepcopy(self.state)
            new_state.play_card(move)
            self.legal_children.add(Node(new_state, self, move))
        
    def expand(self):
        for node in self.legal_children:
            self.children.add(node)

    def select_child_random(self) -> Node:
        return random.choice(list(self.legal_children.intersection(self.children)))
        # return random.choice(list(self.legal_children))
    
    def select_child_ucb(self) -> Node:
        c = 1
        ucbs = []
        children_list = list(self.legal_children.intersection(self.children))
        # children_list = list(self.legal_children)
        for child in children_list:
            if child.visits == 0:
                return child
            ucbs.append(child.score / child.visits + c * np.sqrt(np.log(self.visits) / child.visits))
        index_max = np.argmax(np.array([ucbs]))
        return children_list[index_max]
    
class AlphaZero_player:
    def __init__(self, round: Round, player_position: int, debug = False):
        self.player_position = player_position
        self.state = State(round, player_position)
        # self.policy_network = policy_network()

        self.debug = debug
    def update_state(self, move: int, trump_suit: str):

        move = Card(card_transform(move, ['k', 'h', 'r', 's'].index(trump_suit)))
        self.state.play_card(move, simulation=False)

    
    def get_move(self, trump_suit: str):
        card_id = self.mcts().id
        
        return card_untransform(card_id, ['k', 'h', 'r', 's'].index(trump_suit))

    def mcts(self):
        
        root = Node(copy.deepcopy(self.state))

        current_node = root
        number_of_simulations = 5
        tijd = 10

        for _ in range(tijd):
            # Determination
            current_node.state.determine()
            current_node.set_legal_children()

            i = 0
            # Selection
            while not current_node.state.round_complete() and current_node.legal_children-current_node.children == set():
                i += 1
            # while not current_node.state.round_complete() and current_node.children:
                prev_state = copy.deepcopy(current_node.state)
                current_node = current_node.select_child_ucb()
                prev_state.play_card(current_node.move)
                current_node.state = prev_state
                current_node.set_legal_children()
            
            # Expansion
            if not current_node.state.round_complete():
                current_node.expand()
                current_node = current_node.select_child_random()
                current_node.set_legal_children()
                
            # Simulation
            # explore_state = copy.deepcopy(current_node.state)
            points = 0
            for _ in range(number_of_simulations):
                explore_state = copy.deepcopy(current_node.state)
                while not explore_state.round_complete():
                    
                    move = random.choice(list(explore_state.legal_moves()))
                    explore_state.play_card(move)
                    
                points += explore_state.get_score(self.player_position)
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

