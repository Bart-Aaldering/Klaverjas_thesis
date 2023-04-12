import numpy as np
import pandas as pd
import json

from rounds import Round
from AlphaZero.alphazero import AlphaZero_player


def process_data():
    """Create the originalDB.csv file from the originalDB.txt file"""
    data = pd.read_csv("Data/originalDB.txt", sep=";",low_memory=False)
    data = data.drop(columns=["ID", "TableKey", "TableDbID", "ScoreDbID", "TimeStamp", "Settings"])
    data = data.drop([1313, 1374]) # remove rows with no starting cards
    data.reset_index(drop=True).to_csv("Data/originalDB.csv")

# process_data.sample(n=50000).reset_index(drop=True).to_csv("Data/HistoryDB2.csv")
# print(data.head())

def create_train_data():
    data = pd.read_csv("Data/originalDB.csv", low_memory=False, converters={"Cards": pd.eval})

    data_len = len(data)

    X_train = np.zeros((data_len, 268))
    y_train = np.zeros((data_len, 1))
    for round_num in range(data_len):
        if round_num % 1000 == 0:
            print(round_num)
        round = Round(data.loc[round_num]["FirstPlayer"], data.loc[round_num]["Troef"][0] , data.loc[round_num]["Gaat"])
        round.set_cards(data.loc[round_num]["Cards"])
        
        alpha_player_0 = AlphaZero_player(round, 0)
        X_train[round_num] = alpha_player_0.state.to_nparray()
        y_train[round_num] = json.loads(data.Scores[round_num])["We"] - json.loads(data.Scores[round_num])["They"]
        
    train_data = np.concatenate((X_train, y_train), axis=1)
    
    np.save("Data/train_data.npy", train_data)
    # np.savetxt("Data/train_data.csv", train_data, delimiter=",")
    
if __name__ == "__main__":
    # process_data()
    create_train_data()
    
    