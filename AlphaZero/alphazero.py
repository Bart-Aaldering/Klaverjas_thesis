from __future__ import annotations  # To use the class name in the type hinting

import os
import numpy as np
import random
import copy
import time
import tensorflow as tf

# from typing import List
from sklearn.model_selection import train_test_split
from multiprocessing import Pool, get_context

from Lennard.rounds import Round
from AlphaZero.Klaverjas.card import Card
from AlphaZero.Klaverjas.state import State
from AlphaZero.mcts import MCTS


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU


class AlphaZero_play:
    def __init__(
        self,
        player_position: int,
        mcts_params: dict,
        model
    ):
        self.player_position = player_position
        # self.mcts_steps = mcts_steps
        # self.n_of_sims = n_of_sims
        # self.nn_scaler = nn_scaler
        # self.ucb_c = ucb_c
        self.model = model
        self.mcts = MCTS(mcts_params, model)

    def new_round(self, round: Round):
        self.state = State(round, self.player_position)

    # def update_state(self, move: int, trump_suit: str):
    #     move = Card(card_transform(move, ["k", "h", "r", "s"].index(trump_suit)))
    #     self.state.do_move(move, simulation=False)

    def update_state2(self, move: Card):
        self.state.do_move(move, simulation=False)

    # def get_move(self, trump_suit: str):
    #     move, score = self.mcts()
    #     # self.store_move(move)
    #     return card_untransform(move.id, ["k", "h", "r", "s"].index(trump_suit)), score

    def get_move2(self):
        return self.mcts(self.state)


class AlphaZero_train():       
    def selfplay(self, mcts_params, model, num_rounds):
        X_train = np.zeros((num_rounds * 132, 268), dtype=np.float16)
        y_train = np.zeros((num_rounds * 132, 1), dtype=np.float16)

        alpha_player_0 = AlphaZero_play(0, mcts_params, model)
        alpha_player_1 = AlphaZero_play(1, mcts_params, model)
        alpha_player_2 = AlphaZero_play(2, mcts_params, model)
        alpha_player_3 = AlphaZero_play(3, mcts_params, model)

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
    
    def train_nn(self, train_data, model, batch_size, epochs, callbacks):
        X_train, X_test, y_train, y_test = train_test_split(
            train_data[:, :268], train_data[:, 268], train_size=0.8, shuffle=True
        )

        model.fit(
            X_train,
            y_train,
            batch_size=batch_size,
            epochs=epochs,
            verbose=2,
            validation_data=(X_test, y_test),
            callbacks=callbacks,
        )
        
    def train(self, budget, model_name, n_cores, step, selfplay_params, fit_params, max_memory):
        start_time = time.time()
        self_play_time = 0
        training_time = 0
        
        # budget in seconds
        budget = budget * 3600
        
        # self play parameters
        rounds_per_step = selfplay_params["rounds_per_step"]
        mcts_params = selfplay_params["mcts_params"]

        # training parameters
        epochs = fit_params["epochs"]
        batch_size = fit_params["batch_size"]

        if step == 0:
            memory = None
        else:
            memory = np.load(f"Data/RL_data/{model_name}/{model_name}_{step}_memory.npy")
        
        early_stopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss", verbose=1, restore_best_weights=True)
        
        model = tf.keras.models.load_model(f"Data/Models/{model_name}/{model_name}_{step}.h5")
        
        while time.time() - start_time < budget:
            step += 1
            # generate data
            tijd = time.time()
            with get_context("spawn").Pool(processes=n_cores) as pool:
                data = pool.starmap(
                    self.selfplay,
                    [
                        (mcts_params, model, rounds_per_step // n_cores)
                        for _ in range(n_cores)
                    ],
                )
            self_play_time += time.time() - tijd

            # concatenate data and save it
            data = np.concatenate(data, axis=0)
            np.save(f"Data/RL_data/{model_name}/{model_name}_{step}.npy", data)
            
            
            # add data to memory and remove old data if memory is full
            if memory is None:
                memory = data
            else:
                memory = np.concatenate((memory, data), axis=0)
            if len(memory) > max_memory:
                memory = np.delete(memory, np.s_[0 : len(memory) - max_memory], axis=0)

            # select train data and train model
            train_data = memory[np.random.choice(len(memory), rounds_per_step * 132, replace=False), :]
            tijd = time.time()
            self.train_nn(train_data, model, batch_size, epochs, [early_stopping])
            training_time += time.time() - tijd
            
            # save model
            model.save(f"Data/Models/{model_name}/{model_name}_{step}.h5")

        np.save(f"Data/RL_data/{model_name}/{model_name}_{step}_memory.npy", memory)
        print(time.time() - start_time)
        print(f"Self play time: {self_play_time}")
        print(f"Training time: {training_time}")