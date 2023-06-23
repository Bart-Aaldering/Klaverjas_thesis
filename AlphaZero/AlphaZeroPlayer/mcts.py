from __future__ import annotations  # To use the class name in the type hinting

import copy
import random
import numpy as np
import time

from AlphaZero.AlphaZeroPlayer.Klaverjas.card import Card
from AlphaZero.AlphaZeroPlayer.Klaverjas.state import State


class MCTS_Node:
    def __init__(self, own_team: bool = True, parent: MCTS_Node = None, move: Card = None):
        self.children = set()
        self.children_moves = set()
        self.parent = parent
        self.move = move
        self.score = 0
        self.visits = 0
        self.own_team = own_team

    def __repr__(self) -> str:
        return f"Node({self.move}, {self.parent.move}, {self.score}, {self.visits})"

    def __eq__(self, other: MCTS_Node) -> bool:
        # raise NotImplementedError
        return self.move == other.move

    def __hash__(self) -> int:
        # raise NotImplementedError
        return hash(self.move)

    def set_legal_moves(self, state: State):
        self.legal_moves = state.legal_moves()

    def expand(self):
        move = random.choice(list(self.legal_moves - self.children_moves))
        new_node = MCTS_Node(not self.own_team, self, move)
        self.children.add(new_node)
        self.children_moves.add(move)
        return new_node

    def select_child_ucb(self, c: int) -> MCTS_Node:
        ucbs = []
        legal_children = [child for child in self.children if child.move in self.legal_moves]
        for child in legal_children:
            if child.visits == 0:
                return child
            if self.own_team:
                ucbs.append(child.score / child.visits + c * np.sqrt(np.log(self.visits) / child.visits))
            else:
                ucbs.append(-child.score / child.visits + c * np.sqrt(np.log(self.visits) / child.visits))
        index_max = np.argmax(np.array([ucbs]))
        return legal_children[index_max]


class MCTS:
    def __init__(self, params: dict, model, player_position: int):
        self.mcts_steps = params["mcts_steps"]
        self.n_of_sims = params["n_of_sims"]
        self.ucb_c = params["ucb_c"]
        self.nn_scaler = params["nn_scaler"]
        self.player_position = player_position
        self.model = model
        self.tijden = [0, 0, 0, 0, 0]
        self.tijden2 = [0, 0, 0]

    def __call__(self, state: State, training: bool):
        current_state = copy.deepcopy(state)
        current_node = MCTS_Node()
        if training:
            # ucb_c = self.ucb_c * 4
            ucb_c = self.ucb_c
        else:
            ucb_c = self.ucb_c
        # current_state.set_determinization()
        for _ in range(self.mcts_steps):

            now = time.time()
            # Determination
            current_state.set_determinization()
            self.tijden[0] += time.time() - now
            now = time.time()
            # Selection
            current_node.set_legal_moves(current_state)
            while (
                not current_state.round_complete() and current_node.legal_moves - current_node.children_moves == set()
            ):
                current_node = current_node.select_child_ucb(ucb_c)
                current_state.do_move(current_node.move, "mcts_move")
                current_node.set_legal_moves(current_state)
            self.tijden[1] += time.time() - now
            now = time.time()
            # Expansion
            if not current_state.round_complete():
                new_node = current_node.expand()
                current_node = new_node
                # current_node.expand()
                # current_node = current_node.select_child_ucb(ucb_c)
                current_state.do_move(current_node.move, "mcts_move")

            self.tijden[2] += time.time() - now
            now = time.time()
            # Simulation
            if not current_state.round_complete():
                sim_score = 0
                for _ in range(self.n_of_sims):
                    children = []

                    # Do random moves until round is complete
                    while not current_state.round_complete():
                        move = random.choice(list(current_state.legal_moves()))
                        children.append(move)
                        current_state.do_move(move, "simulation")

                    # Add score to points
                    sim_score += current_state.get_score(self.player_position)

                    # Undo moves
                    children.reverse()
                    for move in children:
                        current_state.undo_move(move, False)

                # Average the score
                if self.n_of_sims > 0:
                    sim_score /= self.n_of_sims

                if self.model is not None:
                    now2 = time.time()
                    stat = current_state.to_nparray()
                    self.tijden2[0] += time.time() - now2
                    now2 = time.time()
                    arr = np.array([stat])
                    self.tijden2[1] += time.time() - now2
                    now2 = time.time()
                    nn_score = int(self.model(arr))
                    self.tijden2[2] += time.time() - now2
                else:
                    nn_score = 0
            else:
                sim_score = current_state.get_score(self.player_position)
                nn_score = sim_score

            self.tijden[3] += time.time() - now
            now = time.time()
            # Backpropagation
            while current_node.parent is not None:
                current_node.visits += 1
                current_node.score += (1 - self.nn_scaler) * sim_score + self.nn_scaler * nn_score
                current_state.undo_move(current_node.move, True)
                current_node = current_node.parent

            current_node.visits += 1
            current_node.score += (1 - self.nn_scaler) * sim_score + self.nn_scaler * nn_score
            self.tijden[4] += time.time() - now
            now = time.time()

        visits = []
        children = []
        for child in current_node.children:
            visits.append(child.visits)
            children.append(child)

        child = children[np.argmax(visits)]

        if training == True:
            visits = np.array(visits) + self.mcts_steps / 10
            probabilities = visits / np.sum(visits)
            move = np.random.choice(children, p=probabilities).move
        else:
            move = child.move

        return move
