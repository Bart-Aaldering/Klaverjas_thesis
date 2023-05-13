import numpy as np
import pandas as pd
import json
import time
import os
import tensorflow as tf

from multiprocessing import Pool
from sklearn.model_selection import train_test_split

from Lennard.rounds import Round
from Lennard.deck import Card
from AlphaZero.alphazero import AlphaZero_play

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU


def create_train_data_SV(process_num: int, total_processes: int):

    data = pd.read_csv("Data/SL_data/originalDB.csv", low_memory=False, converters={"Cards": pd.eval, "Rounds": eval})
    # data = data[:5000]
    data_per_process = len(data.index) // total_processes
    data = data[process_num * data_per_process : (process_num + 1) * data_per_process].reset_index(drop=True)
    total_rounds = len(data)
    X_train = np.zeros((total_rounds * 132, 268), dtype=np.float16)
    y_train = np.zeros((total_rounds * 132, 1), dtype=np.float16)

    alpha_player_0 = AlphaZero_play(0)
    alpha_player_1 = AlphaZero_play(1)
    alpha_player_2 = AlphaZero_play(2)
    alpha_player_3 = AlphaZero_play(3)
    index = 0
    for round_num in range(total_rounds):
        scores = json.loads(data.loc[round_num]["Scores"])

        if scores["WeVerzaakt"] or scores["TheyVerzaakt"]:
            continue

        next_round = False

        if round_num % 500 == 0:
            print(round_num)

        round = Round(data.loc[round_num]["FirstPlayer"], data.loc[round_num]["Troef"][0], data.loc[round_num]["Gaat"])
        round.set_cards(data.loc[round_num]["Cards"])

        alpha_player_0.new_round(round)
        alpha_player_1.new_round(round)
        alpha_player_2.new_round(round)
        alpha_player_3.new_round(round)

        round_score_we = scores["We"] + scores["WeRoem"]
        round_scores_they = scores["They"] + scores["TheyRoem"]

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
                X_train[index + 1] = alpha_player_1.state.to_nparray()
                X_train[index + 2] = alpha_player_2.state.to_nparray()
                X_train[index + 3] = alpha_player_3.state.to_nparray()
                y_train[index] = round_score_we - round_scores_they
                y_train[index + 1] = round_scores_they - round_score_we
                y_train[index + 2] = round_score_we - round_scores_they
                y_train[index + 3] = round_scores_they - round_score_we

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
            X_train[index + 1] = alpha_player_1.state.to_nparray()
            X_train[index + 2] = alpha_player_2.state.to_nparray()
            X_train[index + 3] = alpha_player_3.state.to_nparray()
            y_train[index] = round_score_we - round_scores_they
            y_train[index + 1] = round_scores_they - round_score_we
            y_train[index + 2] = round_score_we - round_scores_they
            y_train[index + 3] = round_scores_they - round_score_we

            index += 4

            card_object = round.legal_moves(round.current_player)[0]
            round.play_card(card_object)
            alpha_player_0.update_state(card_object.id, round.trump_suit)
            alpha_player_1.update_state(card_object.id, round.trump_suit)
            alpha_player_2.update_state(card_object.id, round.trump_suit)
            alpha_player_3.update_state(card_object.id, round.trump_suit)

        X_train[index] = alpha_player_0.state.to_nparray()
        X_train[index + 1] = alpha_player_1.state.to_nparray()
        X_train[index + 2] = alpha_player_2.state.to_nparray()
        X_train[index + 3] = alpha_player_3.state.to_nparray()
        y_train[index] = round_score_we - round_scores_they
        y_train[index + 1] = round_scores_they - round_score_we
        y_train[index + 2] = round_score_we - round_scores_they
        y_train[index + 3] = round_scores_they - round_score_we

        if round_score_we - round_scores_they != X_train[index][-2] - X_train[index][-1]:
            print(round_num)
            print(X_train[index][-2], X_train[index][-1])
            print(round_score_we - round_scores_they, X_train[index][-2] - X_train[index][-1])
            if scores["WeNat"] or scores["TheyNat"]:
                pass
            else:
                print("Something went wrong")
                print(process_num * data_per_process + round_num)

        index += 4

    X_train = X_train[:index]
    y_train = y_train[:index]

    train_data = np.concatenate((X_train, y_train), axis=1)

    np.save(f"Data/SL_data/train_data_{process_num}.npy", train_data)
    # np.savetxt(f"Data/train_data_{process_num}.csv", train_data, delimiter=",")


def merge_npy(files):
    arrays = []
    for num in range(files):
        array = np.load(f"Data/SL_data/train_data_{num}.npy")
        arrays.append(array)
    train_data = np.concatenate(arrays, axis=0)
    np.save(f"Data/SL_data/train_data.npy", train_data)


def run_create_data():
    try:
        n_cores = int(os.environ["SLURM_JOB_CPUS_PER_NODE"])
        cluster = "cluster"
    except:
        n_cores = 10
        cluster = "local"
    print(cluster, "n_cores: ", n_cores)

    with Pool(processes=n_cores) as pool:
        pool.starmap(create_train_data_SV, [(i, n_cores) for i in range(n_cores)])


def train_nn_on_data():
    epochs = 1
    print("loading data")
    data = np.load("Data/SL_data/train_data.npy")
    print("data loaded")

    X = data[:, :268]
    y = data[:, 268]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    # network_name = "simple"
    # network = create_simple_nn()
    network_name = "normal"
    network = tf.keras.models.load_model("Data/Models/SV_nn_normal_7_8135.h5")
    done_epochs = 7

    length = len(X_train) // 10
    for i in range(10):
        network.fit(
            X_train[i * length : (i + 1) * length],
            y_train[i * length : (i + 1) * length],
            batch_size=32,
            epochs=epochs,
            verbose=2,
            validation_data=(X_test, y_test),
        )

    y_pred_test = network(X_test)

    print(X_test[:10][-5:])

    print(y_pred_test[:10])
    print(y_test[:10])

    loss = round(network.evaluate(X_test, y_test, verbose=2))

    network.save(f"Data/Models/SV_nn_{network_name}_{done_epochs+epochs}_{loss}.h5")


if __name__ == "__main__":

    tijd = time.time()
    train_nn_on_data()
    print(time.time() - tijd)
