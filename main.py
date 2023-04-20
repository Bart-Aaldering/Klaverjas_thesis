import random
import time
import pandas as pd
import os 

from multiprocessing import Pool
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from AlphaZero.alphazero import *
from AlphaZero.value_network import Value_random_forest
from Lennard.rule_based_agent import Rule_player
from Lennard.rounds import Round
from AlphaZero.state import State

    
def simulation(rounds_amount: int, process_num: int):
    # random.seed(13)
    
    tijden = [0,0,0,0,0]
    point_cumulative = [0,0]
    scores_alpha = []
    scores_round = []

    if rounds_amount*(process_num+1) > 50000:
        raise "too many rounds"
    
    rounds = pd.read_csv("Data/originalDB.csv", low_memory=False, converters={"Cards": pd.eval})
    
    rule_player = Rule_player()
    alpha_player_0 = AlphaZero_player()
    alpha_player_2 = AlphaZero_player()
    
    for round_num in range(rounds_amount*process_num, rounds_amount*(process_num+1)):
        if not process_num and round_num % 50 == 0:
            print(round_num)
        print(round_num)
        # round = Round((starting_player + 1) % 4, random.choice(['k', 'h', 'r', 's']), random.choice([0,1,2,3]))
        
        round = Round(rounds.loc[round_num]["FirstPlayer"], rounds.loc[round_num]["Troef"][0] , rounds.loc[round_num]["Gaat"])
        round.set_cards(rounds.loc[round_num]["Cards"])
        
        
        alpha_player_0.new_round(round, 0)
        alpha_player_2.new_round(round, 2)
        for trick in range(8):
            for j in range(4):
                
                current_player = round.current_player
                if current_player == 1 or current_player == 3:
                    
                    played_card = rule_player.get_card_good_player(round, current_player)
                    # moves = round.legal_moves()
                    # played_card = random.choice(moves)
                else:
                    if current_player == 0:
                        played_card, _ = alpha_player_0.get_move(round.trump_suit)
                    else:
                        played_card, _ = alpha_player_2.get_move(round.trump_suit)
                    moves = round.legal_moves()
                    
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
                alpha_player_2.update_state(played_card.id, round.trump_suit)
        
        for i in range(5):
            tijden[i] += alpha_player_0.tijden[i]
            
        scores_alpha.append(alpha_player_0.state.get_score(0))
        scores_round.append(round.get_score(0))
        
        point_cumulative[0] += round.points[0]+round.meld[0]
        point_cumulative[1] += round.points[1]+round.meld[1]
    return scores_round, point_cumulative, tijden


def main():
    multiprocessing = False
    multiprocessing = True
    start_time = time.time()
    scores_round = []
    points_cumulative = [0, 0]
    tijden = [0,0,0,0,0]

    start_time = time.time()

    
    try:
        n_cores = int(os.environ['SLURM_JOB_CPUS_PER_NODE'])
        print("Cores: ", n_cores)
    except:
        print("not on cluster")
        n_cores = 10
    
    total_rounds = 100
    rounds_per_sim = total_rounds//n_cores
    
    if multiprocessing:
        with Pool(processes=n_cores) as pool:
            results = pool.starmap(simulation, [(rounds_per_sim, i) for i in range(n_cores)])
            
        for result in results:
            scores_round += result[0]
            points_cumulative[0] += result[1][0]
            points_cumulative[1] += result[1][1]
            tijden = [tijden[i]+result[2][i] for i in range(5)]
    else:
        scores_round, points_cumulative, tijden = simulation(rounds_per_sim, 0)

    # scores_alpha.append(sim.scores_alpha)
    # points_cumulative.append(sim.point_cumulative)
    # tijden = [tijden[i]+sim.tijden[i] for i in range(5)]
    
    if len(scores_round) != n_cores*rounds_per_sim:
        print(len(scores_round))
        print(scores_round)
        raise Exception("wrong length")
    end_time = time.time()
    
    print("Tijden: ", tijden)
    print(points_cumulative)
    print("alpha mean score, std mean and time: ", round(np.mean(scores_round),1), round(np.std(scores_round)/np.sqrt(len(scores_round)), 1), round(end_time - start_time))  

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

if __name__ == "__main__":
    main()
    # # train_nn_on_data()
    # print("starting")
    # tijd = time.time()
    # network = Value_network()
    # print(time.time() - tijd)
    # tijd = time.time()
    # round = Round(0, 'k', 0)
    # print(time.time() - tijd)
    # tijd = time.time()
    # alpha = AlphaZero_player()
    # print(time.time() - tijd)
    # tijd = time.time()
    # alpha.new_round(round, 0)
    # print(time.time() - tijd)
    # tijd = time.time()
    # b = np.array([alpha.state.to_nparray()])
    # print(time.time() - tijd)
    # tijd = time.time()
    # a = network(b)
    # print(time.time() - tijd)
    # print(a)
    # print(int(a))
    # print(type(a))
    
    # train_nn_on_data()
    # network = Value_random_forest()
    # arr = np.load("Data/train_data.npy")
    # np.savetxt("foo.csv", arr[:10], delimiter=",")

    pass