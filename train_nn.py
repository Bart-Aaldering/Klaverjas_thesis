import pandas as pd

from sklearn.model_selection import train_test_split

from AlphaZero.alphazero import *
from Lennard.rule_based_agent import Rule_player
from Lennard.rounds import Round


def train_nn(num_rounds: int, process_num: int):

    print("starting training")
    rounds = pd.read_csv("Data/HistoryDB2.csv", low_memory=False, converters={"Cards": pd.eval})
    print("rounds loaded")
    
    X_train = np.zeros((num_rounds*8*4, 268))
    y_train = np.zeros(num_rounds*8*4)
    
    for round_num in range(num_rounds*process_num, num_rounds*(process_num+1)):
        if not process_num and round_num % 50 == 0:
            print(round_num)
            
        # round = Round((starting_player + 1) % 4, random.choice(['k', 'h', 'r', 's']), random.choice([0,1,2,3]))
        
        round = Round(rounds.loc[round_num]["FirstPlayer"], rounds.loc[round_num]["Troef"][0] , rounds.loc[round_num]["Gaat"])
        round.set_cards(rounds.loc[round_num]["Cards"])
        
        rule_player = Rule_player()
        alpha_player_0 = AlphaZero_player(round, 0)
        alpha_player_1 = AlphaZero_player(round, 1)
        alpha_player_2 = AlphaZero_player(round, 2)
        alpha_player_3 = AlphaZero_player(round, 3)
        
        for trick in range(8):
            for j in range(4):
                
                current_player = round.current_player
                if current_player == 1 or current_player == 3:
                    
                    # played_card = rule_player.get_card_good_player(round, current_player)
                    # moves = round.legal_moves()
                    # played_card = random.choice(moves)
                    if current_player == 1:
                        played_card, score = alpha_player_1.get_move(round.trump_suit)
                    else:
                        played_card, score = alpha_player_3.get_move(round.trump_suit)
                    
                else:
                    if current_player == 0:
                        played_card, score = alpha_player_0.get_move(round.trump_suit)
                    else:
                        played_card, score = alpha_player_2.get_move(round.trump_suit)
                
                moves = round.legal_moves()

                X_train[round_num*8*4+trick*4+j] = alpha_player_0.state.to_nparray()
                y_train[round_num*8*4+trick*4+j] = score
                found = False
                for move in moves:
                    if move.id == played_card:
                        played_card = move
                        found = True
                        break
                if not found:
                    raise Exception("move not found")
                            
                    # moves = round.legal_moves()
                    # played_card = random.choice(moves)

                round.play_card(played_card)
                alpha_player_0.update_state(played_card.id, round.trump_suit)
                alpha_player_1.update_state(played_card.id, round.trump_suit)
                alpha_player_2.update_state(played_card.id, round.trump_suit)
                alpha_player_3.update_state(played_card.id, round.trump_suit)
        
    print("training")
    np.savetxt("Data/traindata.csv", X_train, delimiter=",")
    np.savetxt("Data/trainlabels.csv", y_train, delimiter=",")

    network = Value_network()
    network.train_model(X_train, y_train, 50)
    
    network.save_model()

def train_nn_on_data():
    data = np.load("Data/train_data.npy")
    X = data[:, :268]
    y = data[:, 268]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    network = Value_network()
    network.train_model(X_train, y_train, 4)

    network.save_model()
    
    y_pred_test = network(X_test)
    
    print(X_test[:10][-5:])
    
    print(y_pred_test[:10])
    print(y_test[:10])
    
    network.model.evaluate(X_test,  y_test, verbose=2)
    
    network.save_model()