from __future__ import annotations  # To use the class name in the type hinting

import numpy as np
from Lennard.rounds import Round
from AlphaZero.AlphaZeroPlayer.Klaverjas.card import Card
from AlphaZero.AlphaZeroPlayer.Klaverjas.state import State
from AlphaZero.AlphaZeroPlayer.mcts import MCTS


class AlphaZero_player:
    def __init__(
        self,
        player_position: int,
        mcts_params: dict,
        model,
    ):
        self.player_position = player_position
        self.model = model
        self.mcts = MCTS(mcts_params, model, player_position)
        self.tijden = [0, 0, 0, 0, 0]
        self.state = None

    def new_round_Round(self, round: Round):
        if self.state is not None:
            for i in range(len(self.tijden)):
                self.tijden[i] += self.state.tijden[i]
        # self.state = State(round, self.player_position)
        self.state = State(self.player_position)
        self.state.init_from_Round(round)

    def new_round_klaverlive(self, hand, starting_player, declaring_team):
        self.state = State(self.player_position)
        self.state.init_from_klaverlive(hand, starting_player, declaring_team)

    def update_state(self, move: Card):
        self.state.do_move(move)

    def get_move(self, training: bool = False, extra_noise_ratio: float = 0):
        if self.player_position != self.state.current_player:
            print(self.state.current_player, self.player_position)
            raise Exception("Not this player's turn")
        moves = self.mcts(self.state)

        if training:
            moves[:, 0] += int(self.mcts.mcts_steps * extra_noise_ratio)
            return np.random.choice(moves[:, 1], p=moves[:, 0] / np.sum(moves[:, 0]))
        else:
            return moves[np.argmax(moves[:, 0]), 1]
