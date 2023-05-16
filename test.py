from multiprocessing import get_context
from AlphaZero.train_alphazero import selfplay


def main():
    n_cores = 10
    mcts_params = {
        "mcts_steps": 10,
        "n_of_sims": 1,
        "nn_scaler": 0,
        "ucb_c": 300,
    }
    model = None
    rounds_per_step = 100
    
    with get_context("spawn").Pool(processes=n_cores) as pool:
        data = pool.starmap(
            selfplay,
            [(mcts_params, model, rounds_per_step // n_cores) for _ in range(n_cores)],
        )
    print(data)

if __name__ == "__main__":
    main()
