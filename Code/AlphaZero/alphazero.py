from __future__ import annotations # To use the class name in the type hinting

import numpy as np
import random
import copy
import time

from typing import List


from AlphaZero.card import Card
from rounds import Round
from AlphaZero.state import State
from AlphaZero.helper import card_transform, card_untransform


class Node:
    def __init__(self, state: State, parent: Node = None, move: Card = None):
        self.state = state
        self.children = set()
        self.children_moves = set()
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

    # def set_legal_children(self):
    #     legal_moves = self.state.legal_moves()
    #     self.legal_children = set()
    #     for move in legal_moves:
    #         new_state = copy.deepcopy(self.state)
    #         new_state.play_card(move)
    #         self.legal_children.add(Node(new_state, self, move))
    def set_legal_moves(self):
        self.legal_moves = self.state.legal_moves()
        
    def expand(self):
        for move in self.legal_moves - self.children_moves:
            new_state = copy.deepcopy(self.state)
            new_state.play_card(move)
            self.children.add(Node(new_state, self, move))
            
        # for node in self.legal_children:
        #     self.children.add(node)

    def select_child_random(self) -> Node:
        # return random.choice(list(self.legal_children.intersection(self.children)))
        return random.choice([child for child in self.children if child.move in self.legal_moves])
    
    def select_child_ucb(self) -> Node:
        c = 1
        ucbs = []
        legal_children = [child for child in self.children if child.move in self.legal_moves]
        for child in legal_children:
            if child.visits == 0:
                return child
            ucbs.append(child.score / child.visits + c * np.sqrt(np.log(self.visits) / child.visits))
        index_max = np.argmax(np.array([ucbs]))
        return legal_children[index_max]
    
class AlphaZero_player:
    def __init__(self, round: Round, player_position: int):
        self.player_position = player_position
        self.state = State(round, player_position)
        # self.policy_network = policy_network()
        
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
        tijd = 20
        tijden = [0, 0, 0, 0, 0]
        tijden2 = [0, 0]
        for _ in range(tijd):
            # tijd = time.time()
            # Determination
            current_node.state.determine()
            # tijden2[0] += time.time()-tijd
            # tijd2 = time.time()
            # current_node.set_legal_children()
            current_node.set_legal_moves()
            # tijden2[1] += time.time()-tijd2
            # tijden[0] += time.time()-tijd
            
            # tijd = time.time()
            # Selection
            # while not current_node.state.round_complete() and current_node.legal_children-current_node.children == set():
            while not current_node.state.round_complete() and current_node.legal_moves-current_node.children_moves == set():
                prev_state = copy.deepcopy(current_node.state)
                current_node = current_node.select_child_ucb()
                prev_state.play_card(current_node.move)
                current_node.state = prev_state
                # current_node.set_legal_children()
                current_node.set_legal_moves()
            # tijden[1] += time.time()-tijd
            
            # tijd = time.time()
            # Expansion
            if not current_node.state.round_complete():
                current_node.expand()
                current_node = current_node.select_child_random()
            # tijden[2] += time.time()-tijd
            # tijd = time.time()
            # Simulation
            points = 0
            for _ in range(number_of_simulations):
                explore_state = copy.deepcopy(current_node.state)
                while not explore_state.round_complete():
                    
                    move = random.choice(list(explore_state.legal_moves()))
                    explore_state.play_card(move)
                    
                points += explore_state.get_score(self.player_position)
            points /= number_of_simulations
            # tijden[3] += time.time()-tijd
            # tijd = time.time()
            # Backpropagation
            while current_node.parent is not None:
                current_node.visits += 1
                current_node.score += points
                current_node = current_node.parent
            root.visits += 1
            # tijden[4] += time.time()-tijd
        best_score = -1
        for child in root.children:
            score = child.visits
            if score > best_score:
                best_score = score
                best_child = child
        # print(tijden)
        # print(tijden2)
        return best_child.move

