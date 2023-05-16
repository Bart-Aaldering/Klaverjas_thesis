import os
import wandb

from AlphaZero.train_alphazero import train
from AlphaZero.AlphaZeroPlayer.networks import create_simple_nn, create_normal_nn


def main():
    try:
        n_cores = int(os.environ["SLURM_JOB_CPUS_PER_NODE"])
        cluster = "cluster"
    except:
        n_cores = 10
        cluster = "local"
    print(f"Using {n_cores} cores on {cluster}")

    budget = 0.5  # hours
    starting_step = 0
    model_name = "simple_test_4"
    multiprocessing = True
    
    rounds_per_step = 100
    rounds_per_step = rounds_per_step // n_cores * n_cores  # make sure rounds is divisible by n_cores
    max_memory = rounds_per_step * 132 * 10
    
    mcts_params = {
        "mcts_steps": 10,
        "n_of_sims": 0,
        "nn_scaler": 1,
        "ucb_c": 50,
    }
    fit_params = {
        "epochs": 5,
        "batch_size": 256,
    }
    test_params = {
        "test_rounds": 500,
        "test_frequency": 5,
        "mcts_params": {
            "mcts_steps": 10,
            "n_of_sims": 0,
            "nn_scaler": 1,
            "ucb_c": 50,
        },
    }
    wandb.init(
        # set the wandb project where this run will be logged
        project="Thesis_test5",

        # track hyperparameters and run metadata
        config={
            "budget": budget,
            "starting_step": starting_step,
            "model_name": model_name,
            "multiprocessing": multiprocessing,
            "n_cores": n_cores,
            "max_memory": max_memory,
            "mcts_params": mcts_params,
            "fit_params": fit_params,
            "test_params": test_params,
        }
    )

    if starting_step == 0:
        try:
            os.mkdir(f"Data/RL_data/{model_name}/")
        except:
            print("\n\n\n============model already exists============\n\n\n")
        model = create_simple_nn()    
        model.save(f"Data/Models/{model_name}/{model_name}_0.h5")
    
    total_time, selfplay_time, training_time = train(budget, starting_step, model_name, max_memory, multiprocessing, n_cores, rounds_per_step, mcts_params, fit_params, test_params)
    print("total time:", total_time)
    print("selfplay time:", selfplay_time)
    print("training time:", training_time)

if __name__ == "__main__":
    main()
