import os
import time
import numpy as np
import tensorflow as tf
import random

from multiprocessing import Pool, get_context
from sklearn.model_selection import train_test_split

from AlphaZero.alphazero import AlphaZero_player
from Lennard.rounds import Round

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU


def create_simple_nn():
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Dense(268, activation="relu"),
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dense(1, activation="linear"),
        ]
    )

    # define how to train the model
    model.compile(optimizer="adam", loss="mse")
    model.build(input_shape=(1, 268))

    return model


def create_normal_nn():
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Dense(268, activation="relu"),
            tf.keras.layers.Dense(512, activation="relu"),
            tf.keras.layers.Dense(512, activation="relu"),
            tf.keras.layers.Dense(512, activation="relu"),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(1, activation="linear"),
        ]
    )
    # define how to train the model
    model.compile(optimizer="adam", loss="mse")
    model.build(input_shape=(1, 268))

    return model


def generate_data_RL(
    num_rounds: int, mcts_steps: int, number_of_simulations: int, nn_scaler: float, ucb_c_value: int, model_name: str
):
    X_train = np.zeros((num_rounds * 132, 268), dtype=np.float16)
    y_train = np.zeros((num_rounds * 132, 1), dtype=np.float16)

    alpha_player_0 = AlphaZero_player(0, mcts_steps, number_of_simulations, nn_scaler, ucb_c_value, model_name)
    alpha_player_1 = AlphaZero_player(1, mcts_steps, number_of_simulations, nn_scaler, ucb_c_value, model_name)
    alpha_player_2 = AlphaZero_player(2, mcts_steps, number_of_simulations, nn_scaler, ucb_c_value, model_name)
    alpha_player_3 = AlphaZero_player(3, mcts_steps, number_of_simulations, nn_scaler, ucb_c_value, model_name)

    for round_num in range(num_rounds):
        round = Round(random.choice([0, 1, 2, 3]), random.choice(["k", "h", "r", "s"]), random.choice([0, 1, 2, 3]))

        alpha_player_0.new_round(round)
        alpha_player_1.new_round(round)
        alpha_player_2.new_round(round)
        alpha_player_3.new_round(round)

        # generate a state and score and play a card
        for trick in range(8):
            for j in range(4):
                current_player = alpha_player_0.state.current_player

                if current_player == 0:
                    played_card, score = alpha_player_0.get_move2()
                elif current_player == 1:
                    played_card, score = alpha_player_1.get_move2()
                    score = -score
                elif current_player == 2:
                    played_card, score = alpha_player_2.get_move2()
                else:
                    played_card, score = alpha_player_3.get_move2()
                    score = -score

                X_train[round_num * 132 + trick * 16 + j * 4] = alpha_player_0.state.to_nparray()
                X_train[round_num * 132 + trick * 16 + j * 4 + 1] = alpha_player_1.state.to_nparray()
                X_train[round_num * 132 + trick * 16 + j * 4 + 2] = alpha_player_2.state.to_nparray()
                X_train[round_num * 132 + trick * 16 + j * 4 + 3] = alpha_player_3.state.to_nparray()
                y_train[round_num * 132 + trick * 16 + j * 4] = score
                y_train[round_num * 132 + trick * 16 + j * 4 + 1] = -score
                y_train[round_num * 132 + trick * 16 + j * 4 + 2] = score
                y_train[round_num * 132 + trick * 16 + j * 4 + 3] = -score

                alpha_player_0.update_state2(played_card)
                alpha_player_1.update_state2(played_card)
                alpha_player_2.update_state2(played_card)
                alpha_player_3.update_state2(played_card)

        # generate state and score for end state
        X_train[round_num * 132 + 128] = alpha_player_0.state.to_nparray()
        X_train[round_num * 132 + 128 + 1] = alpha_player_1.state.to_nparray()
        X_train[round_num * 132 + 128 + 2] = alpha_player_2.state.to_nparray()
        X_train[round_num * 132 + 128 + 3] = alpha_player_3.state.to_nparray()
        y_train[round_num * 132 + 128] = alpha_player_0.state.get_score(0)
        y_train[round_num * 132 + 128 + 1] = alpha_player_1.state.get_score(1)
        y_train[round_num * 132 + 128 + 2] = alpha_player_2.state.get_score(2)
        y_train[round_num * 132 + 128 + 3] = alpha_player_3.state.get_score(3)

    train_data = np.concatenate((X_train, y_train), axis=1)
    return train_data


def train_nn():
    start_time = time.time()
    # Initialize the model and set parameters

    # budget parameters
    budget_hours = 21
    budget_minutes = 0
    total_budget = budget_hours * 3600 + budget_minutes * 60

    # training parameters
    rounds_per_step = 10000
    epochs = 1
    batch_size = 32

    # model hyperparameters
    mcts_steps = 200
    number_of_simulations = 5
    nn_scaler = 0
    ucb_c_value = 300

    step = 0
    self_play_time = 0
    training_time = 0

    # create model
    model_name = f"RL_nn_normal_{step}_2.h5"
    if step == 0:
        model = create_normal_nn()
        model.save(f"Data/Models/{model_name}")

    # set cores
    try:
        n_cores = int(os.environ["SLURM_JOB_CPUS_PER_NODE"])
        cluster = "cluster"
    except:
        n_cores = 10
        cluster = "local"
    print(f"Using {n_cores} cores on {cluster}")

    while time.time() - start_time < total_budget:

        tijd = time.time()
        # generate data and save it
        with get_context("spawn").Pool(processes=n_cores) as pool:
            data = pool.starmap(
                generate_data_RL,
                [
                    (rounds_per_step // n_cores, mcts_steps, number_of_simulations, nn_scaler, ucb_c_value, model_name)
                    for _ in range(n_cores)
                ],
            )
        self_play_time += time.time() - tijd
        data = np.concatenate(data, axis=0)
        np.save(f"Data/RL_data/train_data_{step}_2.npy", data)

        X = data[:, :268]
        y = data[:, 268]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

        # train model
        network = tf.keras.models.load_model(f"Data/Models/{model_name}")

        tijd = time.time()
        network.fit(
            X_train,
            y_train,
            batch_size=batch_size,
            epochs=epochs,
            verbose=2,
            validation_data=(X_test, y_test),
        )
        training_time += time.time() - tijd

        # save model
        step += 1
        model_name = f"RL_nn_normal_{step}_2.h5"

        network.save(f"Data/Models/{model_name}")
    print(time.time() - start_time)
    print(f"Self play time: {self_play_time}")
    print(f"Training time: {training_time}")


if __name__ == "__main__":
    tijd = time.time()
    train_nn()
    print(time.time() - tijd)