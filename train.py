import os

from AlphaZero.alphazero import AlphaZero_train
from AlphaZero.networks import create_normal_nn, create_large_nn


def main():
    try:
        n_cores = int(os.environ["SLURM_JOB_CPUS_PER_NODE"])
        cluster = "cluster"
    except:
        n_cores = 10
        cluster = "local"
    print(f"Using {n_cores} cores on {cluster}")

    budget = 0.1  # hours
    step = 0

    rounds = 60
    rounds = rounds // n_cores * n_cores  # make sure rounds is divisible by n_cores
    mcts_steps = 10
    n_of_sims = 1
    nn_scaler = 0.5
    ucb_c = 50
    epochs = 5
    batch_size = 2048
    max_memory = rounds * 132 * 10

    # model_name = f"{mcts_steps}_{n_of_sims}_{nn_scaler}_{ucb_c}"
    model_name = "fast_test_1"
    try:
        os.mkdir(f"Data/RL_data/{model_name}/")
    except:
        print("\n\n\n============model already exists============\n\n\n")
    model = create_normal_nn()
    model.save(f"Data/Models/{model_name}/{model_name}_0.h5")

    print(
        "model name",
        model_name,
        "budget",
        budget,
        "rounds per step",
        rounds,
        "epochs",
        epochs,
        "batch size",
        batch_size,
        "\n",
        "mcts steps",
        mcts_steps,
        "number of simulations",
        n_of_sims,
        "nn scaler",
        nn_scaler,
        "\n",
        "ucb_c",
        ucb_c,
        "max memory",
        max_memory,
        "starting_step",
        step,
    )

    selfplay_params = {
        "rounds_per_step": rounds,
        "mcts_params": {
            "mcts_steps": mcts_steps,
            "n_of_sims": n_of_sims,
            "nn_scaler": nn_scaler,
            "ucb_c": ucb_c,
        },
    }
    fit_params = {
        "epochs": epochs,
        "batch_size": batch_size,
    }
    
    AlphaZero_train().train(budget, model_name, n_cores, step, selfplay_params, fit_params, max_memory)


if __name__ == "__main__":
    main()
