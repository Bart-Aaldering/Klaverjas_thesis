import pandas as pd
import os
import time

from multiprocessing import Pool
from sklearn.model_selection import train_test_split

from AlphaZero.alphazero import *
from Lennard.rule_based_agent import Rule_player
from Lennard.rounds import Round


def train_nn_RL(num_rounds: int, process_num: int):

    print("starting training")
    rounds = pd.read_csv("Data/originalDB.csv", low_memory=False, converters={"Cards": pd.eval})
    print("rounds loaded")
    
    X_train = np.zeros((num_rounds*8*4, 268))
    y_train = np.zeros(num_rounds*8*4)
    
    for round_num in range(num_rounds*process_num, num_rounds*(process_num+1)):
        if not process_num and round_num % 50 == 0:
            print(round_num)
            
        # round = Round((starting_player + 1) % 4, random.choice(['k', 'h', 'r', 's']), random.choice([0,1,2,3]))
        round = Round(rounds.loc[round_num]["FirstPlayer"], rounds.loc[round_num]["Troef"][0] , rounds.loc[round_num]["Gaat"])
        round.set_cards(rounds.loc[round_num]["Cards"])
        
        alpha_player_0 = AlphaZero_player(round, 0)
        alpha_player_1 = AlphaZero_player(round, 1)
        alpha_player_2 = AlphaZero_player(round, 2)
        alpha_player_3 = AlphaZero_player(round, 3)
        
        for trick in range(8):
            for j in range(4):
                
                current_player = round.current_player

                if current_player == 0:
                    played_card, score = alpha_player_0.get_move(round.trump_suit)
                elif current_player == 1:
                    played_card, score = alpha_player_1.get_move(round.trump_suit)
                elif current_player == 2:
                    played_card, score = alpha_player_2.get_move(round.trump_suit)
                else:
                    played_card, score = alpha_player_3.get_move(round.trump_suit)

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

def run_RL():
    try:
        n_cores = int(os.environ['SLURM_JOB_CPUS_PER_NODE'])
        cluster = "cluster"
    except:
        n_cores = 10
        cluster = "local"
    print(cluster, "n_cores: ", n_cores)

    with Pool(processes=n_cores) as pool:
        pool.starmap(train_nn_RL, [(i, n_cores) for i in range(n_cores)])
        
def train_nn_on_data():
    epochs = 5
    print("loading data")
    data = np.load("Data/train_data.npy")
    print("data loaded")
    
    X = data[:, :268]
    y = data[:, 268]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    
    network = Value_network()
    network.train_model(X_train, y_train, epochs)

    network.save_model()
    
    y_pred_test = network(X_test)
    
    print(X_test[:10][-5:])
    
    print(y_pred_test[:10])
    print(y_test[:10])
    
    network.model.evaluate(X_test,  y_test, verbose=2)
    
    network.save_model(f"SV_nn_{epochs}_epochs.h5")
  
if __name__ == "__main__":
    tijd = time.time()
    # run_RL()
    train_nn_on_data()
    print(time.time() - tijd)