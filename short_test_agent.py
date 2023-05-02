import time
import pandas as pd
import os
import numpy as np

from multiprocessing import Pool

from AlphaZero.alphazero import AlphaZero_player
from Lennard.rule_based_agent import Rule_player
from Lennard.rounds import Round


def test_agent(
    rounds_amount: int,
    process_num: int,
    mcts_steps: int,
    number_of_simulations: int,
    nn_scaler: float,
    ucb_c_value: int,
    model_name: str,
):
    # random.seed(13)

    tijden = [0, 0, 0, 0, 0]
    point_cumulative = [0, 0]
    scores_alpha = []
    scores_round = []

    if rounds_amount * (process_num + 1) > 50000:
        raise "too many rounds"

    rounds = pd.read_csv("Data/SL_data/originalDB.csv", low_memory=False, converters={"Cards": pd.eval})

    rule_player = Rule_player()
    alpha_player_0 = AlphaZero_player(0, mcts_steps, number_of_simulations, nn_scaler, ucb_c_value, model_name)
    alpha_player_2 = AlphaZero_player(2, mcts_steps, number_of_simulations, nn_scaler, ucb_c_value, model_name)

    for round_num in range(rounds_amount * process_num, rounds_amount * (process_num + 1)):
        if not process_num and round_num % 50 == 0:
            print(round_num)
        # print(round_num)
        # round = Round((starting_player + 1) % 4, random.choice(['k', 'h', 'r', 's']), random.choice([0,1,2,3]))

        round = Round(
            rounds.loc[round_num]["FirstPlayer"], rounds.loc[round_num]["Troef"][0], rounds.loc[round_num]["Gaat"]
        )
        round.set_cards(rounds.loc[round_num]["Cards"])

        alpha_player_0.new_round(round)
        alpha_player_2.new_round(round)
        for trick in range(8):
            for j in range(4):

                current_player = round.current_player
                if current_player == 1 or current_player == 3:

                    played_card = rule_player.get_card_good_player(round, current_player)
                    # moves = round.legal_moves()
                    # played_card = random.choice(moves)
                else:
                    if current_player == 0:
                        played_card, _ = alpha_player_0.get_move(round.trump_suit)
                    else:
                        played_card, _ = alpha_player_2.get_move(round.trump_suit)
                    moves = round.legal_moves()

                    found = False
                    for move in moves:
                        if move.id == played_card:
                            played_card = move
                            found = True
                            break
                    if not found:
                        raise Exception("move not found")

                    # moves = round.legal_moves()
                    # played_card = random.choice(moves)

                round.play_card(played_card)
                alpha_player_0.update_state(played_card.id, round.trump_suit)
                alpha_player_2.update_state(played_card.id, round.trump_suit)

        for i in range(5):
            tijden[i] += alpha_player_0.tijden[i]

        scores_alpha.append(alpha_player_0.state.get_score(0))
        scores_round.append(round.get_score(0))

        point_cumulative[0] += round.points[0] + round.meld[0]
        point_cumulative[1] += round.points[1] + round.meld[1]
    return scores_round, point_cumulative, tijden


def run_test_multiprocess():
    multiprocessing = False
    multiprocessing = True
    start_time = time.time()
    scores_round = []
    points_cumulative = [0, 0]
    tijden = [0, 0, 0, 0, 0]

    start_time = time.time()

    try:
        n_cores = int(os.environ["SLURM_JOB_CPUS_PER_NODE"])
        cluster = "cluster"
    except:
        n_cores = 10
        cluster = "local"

    print(cluster, "n_cores: ", n_cores)

    total_rounds = 10000
    rounds_per_sim = total_rounds // n_cores

    # hyperparameters
    mcts_steps = 200
    number_of_simulations = 0
    nn_scaler = 1
    ucb_c_value = 300
    model_name = None
    model_name = "RL_nn_normal_10.h5"

    print(mcts_steps, number_of_simulations, nn_scaler, ucb_c_value, model_name)

    if multiprocessing:
        with Pool(processes=n_cores) as pool:
            results = pool.starmap(
                test_agent,
                [
                    (rounds_per_sim, i, mcts_steps, number_of_simulations, nn_scaler, ucb_c_value, model_name)
                    for i in range(n_cores)
                ],
            )

        for result in results:
            scores_round += result[0]
            points_cumulative[0] += result[1][0]
            points_cumulative[1] += result[1][1]
            tijden = [tijden[i] + result[2][i] for i in range(5)]
    else:
        scores_round, points_cumulative, tijden = test_agent(rounds_per_sim, 0)

    if len(scores_round) != n_cores * rounds_per_sim:
        print(len(scores_round))
        print(scores_round)
        raise Exception("wrong length")
    end_time = time.time()

    print("Tijden: ", tijden)
    print(points_cumulative)
    print(
        "score:",
        round(np.mean(scores_round), 1),
        "std_score:",
        round(np.std(scores_round) / np.sqrt(len(scores_round)), 1),
        cluster,
        "time:",
        round(end_time - start_time),
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
        "model:",
        model_name,
    )


if __name__ == "__main__":
    run_test_multiprocess()

    pass