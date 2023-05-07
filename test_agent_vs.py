import time
import pandas as pd
import os
import numpy as np

from multiprocessing import Pool

from AlphaZero.alphazero import AlphaZero_player
from Lennard.rounds import Round


def test_agent(
    num_rounds: int,
    process_id: int,
    mcts_steps: int,
    number_of_simulations: int,
    nn_scaler: float,
    ucb_c_value: int,
    model_name1: str,
    model_name2: str,
):
    # random.seed(13)
    mcts_times = [0, 0, 0, 0, 0]
    point_cumulative = [0, 0]
    scores_alpha = []

    if num_rounds * (process_id + 1) > 50000:
        raise "too many rounds"

    rounds = pd.read_csv("Data/SL_data/originalDB.csv", low_memory=False, converters={"Cards": pd.eval})

    alpha_player_0 = AlphaZero_player(0, mcts_steps, number_of_simulations, nn_scaler, ucb_c_value, model_name1)
    alpha_player_1 = AlphaZero_player(1, mcts_steps, number_of_simulations, nn_scaler, ucb_c_value, model_name2)
    alpha_player_2 = AlphaZero_player(2, mcts_steps, number_of_simulations, nn_scaler, ucb_c_value, model_name1)
    alpha_player_3 = AlphaZero_player(3, mcts_steps, number_of_simulations, nn_scaler, ucb_c_value, model_name2)

    for round_num in range(num_rounds * process_id, num_rounds * (process_id + 1)):
        if not process_id and round_num % 50 == 0:
            print(round_num)
        # print(round_num)
        # round = Round((starting_player + 1) % 4, random.choice(['k', 'h', 'r', 's']), random.choice([0,1,2,3]))

        round = Round(
            rounds.loc[round_num]["FirstPlayer"], rounds.loc[round_num]["Troef"][0], rounds.loc[round_num]["Gaat"]
        )
        round.set_cards(rounds.loc[round_num]["Cards"])

        alpha_player_0.new_round(round)
        alpha_player_1.new_round(round)
        alpha_player_2.new_round(round)
        alpha_player_3.new_round(round)

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

                alpha_player_0.update_state2(played_card)
                alpha_player_1.update_state2(played_card)
                alpha_player_2.update_state2(played_card)
                alpha_player_3.update_state2(played_card)

        for i in range(5):
            mcts_times[i] += alpha_player_0.tijden[i]

        scores_alpha.append(alpha_player_0.state.get_score(0))

        point_cumulative[0] += round.points[0] + round.meld[0]
        point_cumulative[1] += round.points[1] + round.meld[1]

    return scores_alpha, point_cumulative, mcts_times


def run_test_multiprocess():
    multiprocessing = False
    multiprocessing = True

    try:
        n_cores = int(os.environ["SLURM_JOB_CPUS_PER_NODE"])
        cluster = "cluster"
    except:
        n_cores = 10
        cluster = "local"

    print(cluster, "n_cores: ", n_cores)

    total_rounds = 5000
    rounds_per_process = total_rounds // n_cores

    # hyperparameters
    mcts_steps = 200
    number_of_simulations = 1
    nn_scaler = 0.5
    ucb_c_value = 300
    model_name1 = "RL_nn_normal_1_no_CL.h5"
    model_name2 = "RL_nn_normal_45_no_CL.h5"

    print(mcts_steps, number_of_simulations, nn_scaler, ucb_c_value, model_name1, model_name2)

    start_time = time.time()
    scores_round = []
    points_cumulative = [0, 0]
    mcts_times = [0, 0, 0, 0, 0]
    if multiprocessing:
        with Pool(processes=n_cores) as pool:
            results = pool.starmap(
                test_agent,
                [
                    (
                        rounds_per_process,
                        i,
                        mcts_steps,
                        number_of_simulations,
                        nn_scaler,
                        ucb_c_value,
                        model_name1,
                        model_name2,
                    )
                    for i in range(n_cores)
                ],
            )

        for result in results:
            scores_round += result[0]
            points_cumulative[0] += result[1][0]
            points_cumulative[1] += result[1][1]
            mcts_times = [mcts_times[i] + result[2][i] for i in range(5)]

    else:
        scores_round, points_cumulative, mcts_times = test_agent(rounds_per_process, 0)

    if len(scores_round) != n_cores * rounds_per_process:
        print(len(scores_round))
        print(scores_round)
        raise Exception("wrong length")

    print("Tijden: ", mcts_times)
    print(points_cumulative)
    print(
        "score:",
        round(np.mean(scores_round), 1),
        "std_score:",
        round(np.std(scores_round) / np.sqrt(len(scores_round)), 1),
        cluster,
        " PARAMETERS:",
        "rounds:",
        total_rounds,
        "steps:",
        mcts_steps,
        "sims:",
        number_of_simulations,
        "nn_scaler:",
        nn_scaler,
        "ucb_c:",
        ucb_c_value,
        "model1:",
        model_name1,
        "model2:",
        model_name2,
    )
    print("time:", round(time.time() - start_time, 1))


if __name__ == "__main__":
    tijd = time.time()
    run_test_multiprocess()
    print(time.time() - tijd)
    pass
