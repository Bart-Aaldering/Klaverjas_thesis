import os
import wandb
import math
import numpy as np
import tensorflow as tf

from AlphaZero.test_alphazero import run_test_multiprocess
from AlphaZero.train_alphazero import train_nn
from AlphaZero.AlphaZeroPlayer.networks import create_normal_nn, create_large_nn


def main():
    try:
        n_cores = int(os.environ["SLURM_JOB_CPUS_PER_NODE"])
        cluster = "cluster"
    except:
        n_cores = 10
        cluster = "local"
    print(f"Using {n_cores} cores on {cluster}")

    model_name = "large_"
    run_settings = {
        "project_name": "Thesis_test14",
        "model_name": model_name,
        "starting_step": 630,
        "budget": 3.8,  # hours
        "multiprocessing": True,
        "n_cores": n_cores,
    }
    model_params = {
        "model_type": "large",
        "learning_rate": 0.0001,
    }
    selfplay_params = {
        "rounds_per_step": 60,  # amount of selfplay rounds per step
        "max_memory_multiplier": 5,  # how many times rounds_per_step * 36 can fit in memory
        "mcts_params": {
            "mcts_steps": 50,
            "n_of_sims": 0,
            "nn_scaler": 1,
            "ucb_c": 200,
        },
    }
    fit_params = {
        "epochs": 20,
        "batch_size": 2048,
    }
    test_params = {
        "test_rounds": 5000,
        "test_frequency": 10,
        "mcts_params": {
            "mcts_steps": 10,
            "n_of_sims": 0,
            "nn_scaler": 1,
            "ucb_c": 50,
        },
    }
    budget = run_settings["budget"]
    n_cores = run_settings["n_cores"]
    starting_step = run_settings["starting_step"]
    model_name = run_settings["model_name"]
    multiprocessing = run_settings["multiprocessing"]
    learning_rate = model_params["learning_rate"]
    rounds_per_step = selfplay_params["rounds_per_step"]
    mcts_params = selfplay_params["mcts_params"]
    max_memory_multiplier = selfplay_params["max_memory_multiplier"]

    test_params["test_rounds"] = (
        math.ceil(test_params["test_rounds"] / n_cores) * n_cores
    )  # make sure rounds is divisible by n_cores and not devide to 0
    rounds_per_step = (
        math.ceil(rounds_per_step / n_cores) * n_cores
    )  # make sure rounds is divisible by n_cores and not devide to 0
    selfplay_params["rounds_per_step"] = rounds_per_step
    max_memory = rounds_per_step * 36 * max_memory_multiplier

    print("starting training")
    print("run settings:", run_settings)
    print("model params:", model_params)
    print("selfplay params:", selfplay_params)
    print("fit params:", fit_params)
    print("test params:", test_params)

    model = create_large_nn(learning_rate)

    memory = np.load(f"Data/RL_data/optimised_removed_perspectives_long4/optimised_removed_perspectives_long4_630.npy")
    for i in range(530, 630):
        loaded_memory = np.load(
            f"Data/RL_data/optimised_removed_perspectives_long4/optimised_removed_perspectives_long4_{i}.npy"
        )
        memory = np.concatenate((memory, loaded_memory), axis=0)

    budget = budget * 3600
    test_rounds = test_params["test_rounds"]
    test_frequency = test_params["test_frequency"]
    test_mcts_params = test_params["mcts_params"]

    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss", verbose=1, patience=2, restore_best_weights=True
    )
    train_nn(memory, model, fit_params, [early_stopping])
    model_path = model_name + ".h5"
    model.save(f"Data/Models/{model_path}")

    scores_round, alpha_eval_time, _ = run_test_multiprocess(
        n_cores, "rule", test_rounds, test_mcts_params, [model_path, None], multiprocessing
    )
    mean_score = sum(scores_round) / len(scores_round)

    print(
        "score:",
        round(mean_score, 1),
        "std_score:",
        round(np.std(scores_round) / np.sqrt(len(scores_round)), 1),
        "eval_time(ms):",
        alpha_eval_time,
    )


if __name__ == "__main__":
    main()
