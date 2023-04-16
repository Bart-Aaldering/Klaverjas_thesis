import numpy as np
import pandas as pd
import json

from rounds import Round
from deck import Card
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
    data = pd.read_csv("Data/originalDB.csv", low_memory=False, converters={"Cards": pd.eval, "Rounds": eval})
    data = data[:5000]
    total_rounds = len(data)

    X_train = np.zeros((total_rounds*128, 268), dtype=np.float16)
    y_train = np.zeros((total_rounds*128, 1), dtype=np.float16)
    
    index = 0
    for round_num in range(total_rounds):
        scores = json.loads(data.loc[round_num]["Scores"])
        if scores["WeVerzaakt"] or scores["TheyVerzaakt"]:
            continue
        
        next_round = False
        
        if round_num % 100 == 0:
            print(round_num)
        round = Round(data.loc[round_num]["FirstPlayer"], data.loc[round_num]["Troef"][0] , data.loc[round_num]["Gaat"])
        round.set_cards(data.loc[round_num]["Cards"])
        
        alpha_player_0 = AlphaZero_player(round, 0)
        alpha_player_1 = AlphaZero_player(round, 1)
        alpha_player_2 = AlphaZero_player(round, 2)   
        alpha_player_3 = AlphaZero_player(round, 3)
        
        
        round_score_we = scores["We"]+scores["WeRoem"]
        round_scores_they = scores["They"]+scores["TheyRoem"]
        


        # process the first 7 tricks
        for trick in data.loc[round_num]["Rounds"]:
            for _ in range(4):
                card = trick["Cards"][round.current_player]
                card_object = Card(int(card[1:]), card[0])
                # check if the card is legal
                if card_object not in round.legal_moves(round.current_player):
                    next_round = True
                    break
                
                X_train[index] = alpha_player_0.state.to_nparray()
                X_train[index+1] = alpha_player_1.state.to_nparray()
                X_train[index+2] = alpha_player_2.state.to_nparray()
                X_train[index+3] = alpha_player_3.state.to_nparray()
                y_train[index] = round_score_we-round_scores_they
                y_train[index+1] = round_scores_they-round_score_we
                y_train[index+2] = round_score_we-round_scores_they
                y_train[index+3] = round_scores_they-round_score_we


                round.play_card(card_object)
                alpha_player_0.update_state(card_object.id, round.trump_suit)
                alpha_player_1.update_state(card_object.id, round.trump_suit)
                alpha_player_2.update_state(card_object.id, round.trump_suit)
                alpha_player_3.update_state(card_object.id, round.trump_suit)
                index += 4
            if next_round:
                break
        if next_round:
            continue
        
        # process the last trick
        for _ in range(4):
            X_train[index] = alpha_player_0.state.to_nparray()
            X_train[index+1] = alpha_player_1.state.to_nparray()
            X_train[index+2] = alpha_player_2.state.to_nparray()
            X_train[index+3] = alpha_player_3.state.to_nparray()
            y_train[index] = round_score_we-round_scores_they
            y_train[index+1] = round_scores_they-round_score_we
            y_train[index+2] = round_score_we-round_scores_they
            y_train[index+3] = round_scores_they-round_score_we

            index += 4
            
            card_object = round.legal_moves(round.current_player)[0]
            round.play_card(card_object)
            alpha_player_0.update_state(card_object.id, round.trump_suit)
            alpha_player_1.update_state(card_object.id, round.trump_suit)
            alpha_player_2.update_state(card_object.id, round.trump_suit)
            alpha_player_3.update_state(card_object.id, round.trump_suit)

        X_train[index] = alpha_player_0.state.to_nparray()
        X_train[index+1] = alpha_player_1.state.to_nparray()
        X_train[index+2] = alpha_player_2.state.to_nparray()
        X_train[index+3] = alpha_player_3.state.to_nparray()
        y_train[index] = round_score_we-round_scores_they
        y_train[index+1] = round_scores_they-round_score_we
        y_train[index+2] = round_score_we-round_scores_they
        y_train[index+3] = round_scores_they-round_score_we
        
        if round_score_we-round_scores_they != X_train[index][-2] - X_train[index][-1]:
            print(round_num)
            print(X_train[index][-2], X_train[index][-1])
            print(round_score_we-round_scores_they, X_train[index][-2] - X_train[index][-1])
            if scores["WeNat"] or scores["TheyNat"]:
                pass
            else:
                raise Exception("Something went wrong")
        
        index += 4

    X_train = X_train[:index]
    y_train = y_train[:index]
    
    train_data = np.concatenate((X_train, y_train), axis=1)

    np.save("Data/train_data.npy", train_data)
    # np.savetxt("Data/train_data.csv", train_data, delimiter=",")
    
if __name__ == "__main__":
    # process_data()
    create_train_data()
    