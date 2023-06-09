from __future__ import annotations  # To use the class name in the type hinting

from Lennard.rounds import Round
from AlphaZero.AlphaZeroPlayer.Klaverjas.card import Card
from AlphaZero.AlphaZeroPlayer.Klaverjas.state import State
from AlphaZero.AlphaZeroPlayer.mcts import MCTS


class AlphaZero_player:
    def __init__(self, player_position: int, mcts_params: dict, model):
        self.player_position = player_position
        self.model = model
        self.mcts = MCTS(mcts_params, model, player_position)
        self.tijden = [0, 0, 0, 0, 0]
        self.state = None

    def new_round_Round(self, round: Round):
        if self.state is not None:
            for i in range(len(self.tijden)):
                self.tijden[i] += self.state.tijden[i]
        self.state = State(self.player_position)
        self.state.set_state_from_Round(round)

    def new_round_klaverlive(self, player_information):
        self.state = State(self.player_position)
        self.state.set_state_from_klaverlive(player_information)

    def update_state(self, move: Card):
        self.state.do_move(move)

    def get_move(self):
        return self.mcts(self.state)
