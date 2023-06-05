import os
import wandb
import math
import time
import copy

from AlphaZero.train_alphazero import train
from AlphaZero.AlphaZeroPlayer.networks import create_simple_nn, create_normal_nn, create_large_nn, create_two_headed_nn


def run_train(
    run_settings,
    model_params,
    selfplay_params,
    fit_params,
    test_params,
):
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

    wandb.init(
        # set the wandb project where this run will be logged
        project=run_settings["project_name"],
        # name of the run
        name=model_name,
        # track hyperparameters and run metadata
        config={
            "run_settings": run_settings,
            "selfplay_params": selfplay_params,
            "fit_params": fit_params,
            "test_params": test_params,
        },
    )
    print("starting training")
    print("run settings:", run_settings)
    print("selfplay params:", selfplay_params)
    print("fit params:", fit_params)
    print("test params:", test_params)

    if starting_step == 0:
        try:
            os.mkdir(f"Data/RL_data/{model_name}/")
        except:
            print("\n\n\n============model already exists============\n\n\n")
        if model_params["model_type"] == "simple":
            model = create_simple_nn(learning_rate)
        elif model_params["model_type"] == "normal":
            model = create_normal_nn(learning_rate)
        elif model_params["model_type"] == "large":
            model = create_large_nn(learning_rate)
        elif model_params["model_type"] == "two_head":
            model = create_two_headed_nn(learning_rate)
        else:
            raise Exception("model type not recognized")

        model.save(f"Data/Models/{model_name}/{model_name}_0.h5")

    total_time, selfplay_time, training_time, testing_time = train(
        budget,
        starting_step,
        model_name,
        max_memory,
        multiprocessing,
        n_cores,
        rounds_per_step,
        mcts_params,
        fit_params,
        test_params,
    )
    print("total time:", total_time)
    print("selfplay time:", selfplay_time)
    print("training time:", training_time)
    print("testing time:", testing_time)
    wandb.finish()


def main():
    try:
        n_cores = int(os.environ["SLURM_JOB_CPUS_PER_NODE"])
        cluster = "cluster"
    except:
        n_cores = 10
        cluster = "local"
    print(f"Using {n_cores} cores on {cluster}")

    model_name = "optimised_50_steps"
    run_settings = {
        "project_name": "Thesis_test16",
        "model_name": model_name,
        "starting_step": 0,
        "budget": 0.01,  # hours
        "multiprocessing": True,
        "n_cores": n_cores,
    }
    model_params = {
        "model_type": "two_head",
        "learning_rate": 0.0001,
    }
    selfplay_params = {
        "rounds_per_step": 1,  # amount of selfplay rounds per step
        "max_memory_multiplier": 5,  # how many times rounds_per_step * 36 can fit in memory
        "mcts_params": {
            "mcts_steps": 10,
            "n_of_sims": 0,
            "nn_scaler": 1,
            "ucb_c": 50,
        },
    }
    fit_params = {
        "epochs": 1,
        "batch_size": 2048,
    }
    test_params = {
        "test_rounds": 10,
        "test_frequency": 1,
        "mcts_params": {
            "mcts_steps": 10,
            "n_of_sims": 0,
            "nn_scaler": 1,
            "ucb_c": 50,
        },
    }
    run_train(
        run_settings,
        model_params,
        selfplay_params,
        fit_params,
        test_params,
    )

    # for rounds_per_step in [30, 120]:
    #     selfplay_params2 = copy.deepcopy(selfplay_params)
    #     selfplay_params2["rounds_per_step"] = rounds_per_step
    #     run_settings["model_name"] = model_name + "1" + str(rounds_per_step)
    #     run_train(
    #         run_settings,
    #         model_params,
    #         selfplay_params2,
    #         fit_params,
    #         test_params,
    #     )

    # for batch_size in [512, 8192]:
    #     fit_params2 = copy.deepcopy(fit_params)
    #     fit_params2["batch_size"] = batch_size
    #     run_settings["model_name"] = model_name + "2" + str(batch_size)
    #     run_train(
    #         run_settings,
    #         model_params,
    #         selfplay_params,
    #         fit_params2,
    #         test_params,
    #     )

    # for epochs in [1, 10]:
    #     fit_params2 = copy.deepcopy(fit_params)
    #     fit_params2["epochs"] = epochs
    #     run_settings["model_name"] = model_name + "3" + str(epochs)
    #     run_train(
    #         run_settings,
    #         model_params,
    #         selfplay_params,
    #         fit_params2,
    #         test_params,
    #     )

    # for max_memory_multiplier in [10, 40]:
    #     selfplay_params2 = copy.deepcopy(selfplay_params)
    #     selfplay_params2["max_memory_multiplier"] = max_memory_multiplier
    #     run_settings["model_name"] = model_name + "4" + str(max_memory_multiplier)
    #     run_train(
    #         run_settings,
    #         model_params,
    #         selfplay_params2,
    #         fit_params,
    #         test_params,
    #     )

    # for learning_rate in [0.0001, 0.01]:
    #     model_params2 = copy.deepcopy(model_params)
    #     model_params2["learning_rate"] = learning_rate
    #     run_settings["model_name"] = model_name + "5" + str(learning_rate)
    #     run_train(
    #         run_settings,
    #         model_params2,
    #         selfplay_params,
    #         fit_params,
    #         test_params,
    #     )
    # for model_type in ["normal", "large"]:
    #     model_params2 = copy.deepcopy(model_params)
    #     model_params2["model_type"] = model_type
    #     run_settings["model_name"] = model_name + "6" + str(model_type)
    #     run_train(
    #         run_settings,
    #         model_params2,
    #         selfplay_params,
    #         fit_params,
    #         test_params,
    #     )


if __name__ == "__main__":
    starting_time = time.time()
    main()
    print("total run time:", time.time() - starting_time)
