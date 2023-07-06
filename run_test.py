import numpy as np
import time
import os
import math

from AlphaZero.test_alphazero import run_test_multiprocess


def run_test(mcts_steps, ucb):
    try:
        n_cores = int(os.environ["SLURM_JOB_CPUS_PER_NODE"])
        cluster = "cluster"
    except:
        n_cores = 10
        cluster = "local"

    opponent = "rule"
    multiprocessing = True

    num_rounds = 5000
    num_rounds = (
        math.ceil(num_rounds / n_cores) * n_cores
    )  # make sure rounds is divisible by n_cores and not devide to 0

    mcts_params = {
        "mcts_steps": mcts_steps,
        "n_of_sims": 1,
        "nn_scaler": 0,
        "ucb_c": ucb,
    }

    model_paths = [None, None]

    print(
        "cluster:",
        cluster,
        "cores",
        n_cores,
        "rounds:",
        num_rounds,
        "mcts_params:",
        mcts_params,
        "model_paths:",
        model_paths,
    )
    now = time.time()
    scores_round, alpha_eval_time, _ = run_test_multiprocess(
        n_cores, opponent, num_rounds, mcts_params, model_paths, multiprocessing
    )
    print("results", mcts_params)
    print("time:", time.time() - now)
    mean_score = sum(scores_round) / len(scores_round)

    print(
        "score:",
        round(mean_score, 1),
        "std_score:",
        round(np.std(scores_round) / np.sqrt(len(scores_round)), 1),
        "eval_time(ms):",
        alpha_eval_time,
    )
def main():
    run_test(200, 12800)
    
if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Total time: ", time.time() - start_time)
