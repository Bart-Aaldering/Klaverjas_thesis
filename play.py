import random
import numpy as np

from Lennard.rounds import Round
from AlphaZero.AlphaZeroPlayer.Klaverjas.card import Card
from AlphaZero.AlphaZeroPlayer.alphazero_player import AlphaZero_player
from AlphaZero.AlphaZeroPlayer.Klaverjas.helper import card_transform, card_untransform

def print_state(state):
    cards = state[:288]
    cards = cards.reshape((32, 9))
    print(cards)
    print(state[288:])
    
def main():
    mcts_params = {
        "mcts_steps": 10,
        "n_of_sims": 0,
        "nn_scaler": 1,
        "ucb_c": 50,
    }
    model = None
    
    alpha_player_1 = AlphaZero_player(1, mcts_params, model)
    alpha_player_2 = AlphaZero_player(2, mcts_params, model)
    alpha_player_3 = AlphaZero_player(3, mcts_params, model)
    random.seed(0)
    while input("New Game? (y/n)") == "y":
        round = Round(random.choice([0, 1, 2, 3]), "k", random.choice([0, 1, 2, 3]))

        alpha_player_1.new_round(round)
        alpha_player_2.new_round(round)
        alpha_player_3.new_round(round)
        print(round.player_hands)
        print(alpha_player_1.state.hands)
        print(alpha_player_2.state.hands)
        print(alpha_player_3.state.hands)
        for trick in range(8):
            for j in range(4):
                current_player = round.current_player
                moves = round.legal_moves()
                if current_player == 0:
                    print(moves)
                    played_card = int(input("Choose a card: "))

                elif current_player == 1:
                    played_card, _ = alpha_player_1.get_move()
                    played_card = card_untransform(played_card.id, ["k", "h", "r", "s"].index(round.trump_suit))
                elif current_player == 2:
                    played_card, _ = alpha_player_2.get_move()
                    played_card = card_untransform(played_card.id, ["k", "h", "r", "s"].index(round.trump_suit))
                else:
                    played_card, _ = alpha_player_3.get_move()
                    played_card = card_untransform(played_card.id, ["k", "h", "r", "s"].index(round.trump_suit))
                
                
                found = False
                for move in moves:
                    if move.id == played_card:
                        played_card = move
                        found = True
                        break
                if not found:
                    raise Exception("move not found")
                
                print(played_card)
                a = alpha_player_1.state.to_nparray()
                b = alpha_player_2.state.to_nparray()
                c = alpha_player_3.state.to_nparray()
                print_state(a)
                
                round.play_card(played_card)
                move = Card(card_transform(played_card.id, ["k", "h", "r", "s"].index(round.trump_suit)))
                alpha_player_1.update_state(move)
                alpha_player_2.update_state(move)
                alpha_player_3.update_state(move)

np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=np.inf)
if __name__ == "__main__":
    main()