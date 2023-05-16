import numpy as np
import time
import os

from AlphaZero.test_alphazero import run_test_multiprocess

def main():
    try:
        n_cores = int(os.environ["SLURM_JOB_CPUS_PER_NODE"])
        cluster = "cluster"
    except:
        n_cores = 10
        cluster = "local"
    
    opponent = "rule"
    num_rounds = 50
    multiprocessing = True
    
    mcts_params = {
        "mcts_steps": 10,
        "n_of_sims": 1,
        "nn_scaler": 0,
        "ucb_c": 300,
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
        model_paths
    )
    
    scores_round, alpha_eval_time, _ = run_test_multiprocess(n_cores, opponent, num_rounds, mcts_params, model_paths, multiprocessing)
    
    mean_score = sum(scores_round)/len(scores_round)
    
    print(
        "score:",
        round(mean_score, 1),
        "std_score:",
        round(np.std(scores_round) / np.sqrt(len(scores_round)), 1),
        "eval_time(ms):",
        alpha_eval_time,
    )

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Total time: ", time.time() - start_time)