import random
import time
from multiprocessing import Pool

from AlphaZero.alphazero import *
from rule_based_agent import Rule_player
from rounds import Round
from AlphaZero.state import State

    
def simulation(rounds: int):
    # random.seed(13)
    
    tijden = [0,0,0,0,0]
    point_cumulative = [0,0]
    scores_alpha = []
    scores_round = []

    starting_player = 0
    for i in range(rounds):
        if i % 50 == 0:
            print(i)
        starting_player = (starting_player + 1) % 4
        round = Round(starting_player, random.choice(['k', 'h', 'r', 's']), random.choice([0,1,2,3]))
        rule_player = Rule_player()
        alpha_player_0 = AlphaZero_player(round, 0)
        alpha_player_2 = AlphaZero_player(round, 2)
        for i in range(8):
            for j in range(4):
                
                current_player = round.current_player
                if current_player == 1 or current_player == 3:
                    
                    played_card = rule_player.get_card_good_player(round, current_player)
                    # moves = round.legal_moves()
                    # played_card = random.choice(moves)
                else:
                    if current_player == 0:
                        played_card = alpha_player_0.get_move(round.trump_suit)
                    else:
                        played_card = alpha_player_2.get_move(round.trump_suit)
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
        
        point_cumulative[0] += round.points[0]+round.meld[0]
        point_cumulative[1] += round.points[1]+round.meld[1]
    return scores_round, point_cumulative, tijden


def main():
    start_time = time.time()
    scores_round = []
    points_cumulative = [0, 0]
    tijden = [0,0,0,0,0]

    start_time = time.time()
    rounds_per_sim = 1000
    sims = 10

    with Pool(processes=10) as pool:
        results = pool.map(simulation, [rounds_per_sim for _ in range(sims)])
        
    for result in results:
        scores_round += result[0]
        points_cumulative[0] += result[1][0]
        points_cumulative[1] += result[1][1]
        tijden = [tijden[i]+result[2][i] for i in range(5)]


    # scores_alpha.append(sim.scores_alpha)
    # points_cumulative.append(sim.point_cumulative)
    # tijden = [tijden[i]+sim.tijden[i] for i in range(5)]
    
    if len(scores_round) != sims*rounds_per_sim:
        print(len(scores_round))
        print(scores_round)
        raise Exception("wrong length")
    end_time = time.time()
    
    print("Tijden: ", tijden)
    print(points_cumulative)
    print("alpha mean score, std mean and time: ", round(np.mean(scores_round),1), round(np.std(scores_round)/np.sqrt(len(scores_round)), 1), round(end_time - start_time))  

if __name__ == "__main__":
    main()
    # main2()
    # a = [Card(10), Card(11)]
    # b = a.copy()
    # a.remove(Card(10))
    # a = 5
    # print(a,b)

    # tijd = time.time()
    # # # import numpy as np
    # # # from AlphaZero.state import State

    # a = [1,2,3,4,5]
    # # asdf = [x for x in range(32)]
    # for _ in range(10000000):
    #     # b = [0,1,2,3]
    #     # b.pop(2) 
    #     b = {0,1,2,3}
    #     b.remove(2)
    #     # b -= {2}
        

    # print(b)
    # print(time.time() - tijd)
    # # main2()
    # for i in range(1,2): 
    #     print("H IER")
    # hand = [set(), set(), set()]
    # possible_cards = [[27, 37, 33, 0, 32, 36, 21, 23, 7, 26, 17, 13, 14, 11, 30, 12, 35, 10], [11, 27, 10, 13, 30, 36, 21, 37, 26, 35, 33, 12, 32, 14, 17, 23], [11, 23, 17, 37, 30, 36, 12, 33, 13, 14, 10, 26, 27, 21, 32, 35]]
    # player = 0
    # num_cards_to_add = [6, 6, 6]
    # print(find_card_configuration(hand, possible_cards, player, num_cards_to_add))
    # print(hand)
    
    pass
