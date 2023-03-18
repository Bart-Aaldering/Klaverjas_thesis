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

    # def set_legal_children(self):
    #     legal_moves = self.state.legal_moves()
    #     self.legal_children = set()
    #     for move in legal_moves:
    #         new_state = copy.deepcopy(self.state)
    #         new_state.do_move(move)
    #         self.legal_children.add(Node(new_state, self, move))
    def set_legal_moves(self, state: State):
        self.legal_moves = state.legal_moves()
        
    def expand(self):
        for move in self.legal_moves - self.children_moves:
            self.children.add(Node(self, move))
            self.children_moves.add(move)
            
        # for node in self.legal_children:
        #     self.children.add(node)

    def select_child_random(self) -> Node:
        # return random.choice(list(self.legal_children.intersection(self.children)))
        choice = random.choice([child for child in self.children if child.move in self.legal_moves])
        # print("random choice child", self.children)
        # print("random", choice)
        return choice
    
    def select_child_ucb(self) -> Node:
        c = 1
        ucbs = []
        legal_children = [child for child in self.children if child.move in self.legal_moves]
        # legal_children = list(self.legal_children.intersection(self.children))
        for child in legal_children:
            if child.visits == 0:
                return child
            ucbs.append(child.score / child.visits + c * np.sqrt(np.log(self.visits) / child.visits))
        index_max = np.argmax(np.array([ucbs]))
        # print("ucb choice child", self.children)
        # print("legal", legal_children[index_max])
        return legal_children[index_max]

class AlphaZero_player:
    def __init__(self, round: Round, player_position: int):
        self.player_position = player_position
        self.state = State(round, player_position)
        # self.policy_network = policy_network()
        
    def update_state(self, move: int, trump_suit: str):
        move = Card(card_transform(move, ['k', 'h', 'r', 's'].index(trump_suit)))
        self.state.do_move(move, simulation=False)

    def get_move(self, trump_suit: str):
        card_id = self.mcts().id
        return card_untransform(card_id, ['k', 'h', 'r', 's'].index(trump_suit))

    def mcts(self):
        current_state = copy.deepcopy(self.state)
        current_node = Node()
        number_of_simulations = 5
        tijd = 10
        tijden = [0, 0, 0, 0, 0]
        tijden2 = [0, 0]
        print("possible moves", current_state.possible_cards)
        determinizations = current_state.find_x_determinizations(tijd)
        print("determinizations", determinizations)
        
        for i in range(tijd):
            # tijd = time.time()
            
            # Determination
            # current_state.determine()
            # 
            other_players = [0,1,2,3]
            other_players.pop(current_state.own_position)
            for j in range(3):
                print("DET", determinizations[i])
                print("left", current_state.cards_left[other_players[j]])
                if len(determinizations[i][j]) != current_state.cards_left[other_players[j]]:
                    raise Exception("Determinization not correct")

            current_state.set_determinization(determinizations[i])
            # tijden2[0] += time.time()-tijd
            # tijd2 = time.time()
            # current_node.set_legal_children()
            current_node.set_legal_moves(current_state)
            # tijden2[1] += time.time()-tijd2
            # tijden[0] += time.time()-tijd
            
            # tijd = time.time()
            # Selection
            # while not current_node.state.round_complete() and current_node.legal_children-current_node.children == set():
            while not current_state.round_complete() and current_node.legal_moves-current_node.children_moves == set():
                # prev_state = copy.deepcopy(current_node.state)
                current_node = current_node.select_child_ucb()
                current_state.do_move(current_node.move)
                # current_node.state = prev_state
                # current_node.set_legal_children()
                current_node.set_legal_moves(current_state)
            # tijden[1] += time.time()-tijd
            
            # tijd = time.time()
            # Expansion
            if not current_state.round_complete():
                current_node.expand()
                current_node = current_node.select_child_random()
                current_state.do_move(current_node.move)
            # tijden[2] += time.time()-tijd
            # tijd = time.time()
            # Simulation
            points = 0
            for _ in range(number_of_simulations):
                moves = []

                # Do random moves until round is complete
                while not current_state.round_complete():
                    
                    move = random.choice(list(current_state.legal_moves()))
                    moves.append(move)
                    current_state.do_move(move)
                
                # Add score to points
                points += current_state.get_score(self.player_position)
                
                # Undo moves
                moves.reverse()
                for move in moves:
                    current_state.undo_move(move)
                
            points /= number_of_simulations
            # tijden[3] += time.time()-tijd
            # tijd = time.time()
            # Backpropagation
            while current_node.parent is not None:
                current_node.visits += 1
                current_node.score += points
                current_state.undo_move(current_node.move)
                current_node = current_node.parent
                
            current_node.visits += 1
            # tijden[4] += time.time()-tijd
        best_score = -1
        for child in current_node.children:
            score = child.visits
            if score > best_score:
                best_score = score
                best_child = child
        # print(tijden)
        # print(tijden2)
        return best_child.move
