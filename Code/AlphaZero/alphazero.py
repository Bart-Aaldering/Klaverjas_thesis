from __future__ import annotations # To use the class name in the type hinting

import numpy as np
import random
import copy
import time

from typing import List

from rounds import Round
from AlphaZero.card import Card
from AlphaZero.state import State
from AlphaZero.helper import card_transform, card_untransform
from AlphaZero.value_network import Value_network

class Node:
    def __init__(self, parent: Node = None, move: Card = None):
        self.children = set()
        self.children_moves = set()
        self.parent = parent
        self.move = move
        self.score = 0
        self.visits = 0
    
    def __repr__(self) -> str:
        return f"Node({self.move}, {self.parent.move}, {self.score}, {self.visits})"
    
    def __eq__(self, other: Node) -> bool:
        # raise NotImplementedError
        return self.move == other.move
    
    def __hash__(self) -> int:
        # raise NotImplementedError
        return hash(self.move)

    def set_legal_moves(self, state: State):
        self.legal_moves = state.legal_moves()
        
    def expand(self):
        for move in self.legal_moves - self.children_moves:
            self.children.add(Node(self, move))
            self.children_moves.add(move)

    def select_child_random(self) -> Node:
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
        self.tijden = [0, 0, 0, 0, 0]
        # self.policy_network = Value_network()
    
    def update_state(self, move: int, trump_suit: str):
        move = Card(card_transform(move, ['k', 'h', 'r', 's'].index(trump_suit)))
        self.state.do_move(move, simulation=False)

    def get_move(self, trump_suit: str):
        move, score = self.mcts()
        # self.store_move(move)
        return card_untransform(move.id, ['k', 'h', 'r', 's'].index(trump_suit)), score
    
    def store_move(self, move):
        # Open a file with access mode 'a'
        file_object = open('Code\Data\state_scores.txt', 'a')

        # Append 'hello' at the end of file
        file_object.write(self.state.to_nparray().tostring() + " " + str(move.score/move.visits))
        # Close the file
        file_object.close()
        
    def mcts(self):
        current_state = copy.deepcopy(self.state)
        current_node = Node()
        
        tijd = 50
        number_of_simulations = 5
        nn_scaler = 0.01
        # current_state.set_determinization2()
        for i in range(tijd):
            # tijd = time.time()
            
            # Determination
            current_state.set_determinization()
            
            # self.tijden[0] += time.time()-tijd
            # tijd = time.time()
            
            # Selection
            current_node.set_legal_moves(current_state)
            while not current_state.round_complete() and current_node.legal_moves-current_node.children_moves == set():
                current_node = current_node.select_child_ucb()
                current_state.do_move(current_node.move)
                current_node.set_legal_moves(current_state)

                
            # self.tijden[1] += time.time()-tijd
            # tijd = time.time()
            
            # Expansion
            if not current_state.round_complete():
                current_node.expand()
                current_node = current_node.select_child_random()
                current_state.do_move(current_node.move)
                
            # self.tijden[2] += time.time()-tijd
            # tijd = time.time()
            
            # Simulation
            sim_score = 0
            for _ in range(number_of_simulations):
                moves = []

                # Do random moves until round is complete
                while not current_state.round_complete():
                    move = random.choice(list(current_state.legal_moves()))
                    moves.append(move)
                    current_state.do_move(move)

                # Add score to points
                sim_score += current_state.get_score(self.player_position)

                # Undo moves
                moves.reverse()
                for move in moves:
                    current_state.undo_move(move)
            sim_score /= number_of_simulations
            
            nn_score = 0
            # nn_score = self.policy_network.predict(current_state.to_nparray())
            
            # self.tijden[3] += time.time()-tijd
            # tijd = time.time()
            
            # Backpropagation
            while current_node.parent is not None:
                current_node.visits += 1
                current_node.score += sim_score + nn_scaler*nn_score
                current_state.undo_move(current_node.move)
                current_node = current_node.parent
            current_node.visits += 1
            current_node.score += sim_score + nn_scaler*nn_score
            
            # self.tijden[4] += time.time()-tijd
            
        best_score = -10
        for child in current_node.children:
            score = child.visits
            if score > best_score:
                best_score = score
                best_child = child
        
        return best_child.move, current_node.score/current_node.visits
        