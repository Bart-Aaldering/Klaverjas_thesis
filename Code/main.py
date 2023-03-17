import random
import time

from AlphaZero.alphazero import *
from rule_based_agent import Rule_player
from rounds import Round
from AlphaZero.state import State

    
class Game:
    def __init__(self, starting_player):
        self.rounds = []
        self.score = [0,0]
        self.starting_player = starting_player
        self.time = 0
    
    #Plays a game of Klaverjas. Currently a game conists of 1 round
    def play_game(self):

        self.round = Round(self.starting_player, random.choice(['k', 'h', 'r', 's']), random.choice([0,1,2,3]))
        rule_player = Rule_player()
        alpha_player_0 = AlphaZero_player(self.round, 0)
        alpha_player_2 = AlphaZero_player(self.round, 2)
        for i in range(8):
            # print("new trick")
            for j in range(4):
                
                current_player = self.round.current_player
                if current_player == 1 or current_player == 3:
                    
                    played_card = rule_player.get_card_good_player(self.round, current_player)
                    # moves = self.round.legal_moves()
                    # played_card = random.choice(moves)
                else:
                    if current_player == 0:
                        tijd = time.time()
                        played_card = alpha_player_0.get_move(self.round.trump_suit)
                        # print("get_move ", time.time()-tijd)
                    else:
                        played_card = alpha_player_2.get_move(self.round.trump_suit)
                    moves = self.round.legal_moves()
                    
                    found = False
                    for move in moves:
                        if move.id == played_card:
                            played_card = move
                            found = True
                            break
                    if not found:
                        raise Exception("move not found")
                            
                    # moves = self.round.legal_moves()
                    # played_card = random.choice(moves)
                self.round.play_card(played_card)
                alpha_player_0.update_state(played_card.id, self.round.trump_suit)
                alpha_player_2.update_state(played_card.id, self.round.trump_suit)
                
        self.score[0] += self.round.points[0]+self.round.meld[0]
        self.score[1] += self.round.points[1]+self.round.meld[1]

def main():
    # random.seed(13)
    games = [0,0]
    games_won = [0,0]

    points = []
    point_cumulative = [0,0]
    #Simulates the 10000 pre-generated games
    start_time = time.time()
    for i in range(200):
        if i % 1 == 0:
            print(i)
            
        game = Game(random.choice([0,1,2,3]))
        game.play_game()
        starting_player = game.starting_player
        if game.score[1] > game.score[0]:
            games_won[starting_player%2] += 1
        games[starting_player % 2] += 1
        points.append(game.score)
        point_cumulative[0] += game.score[0]
        point_cumulative[1] += game.score[1]
        
    end_time = time.time()

        
    print('Games won when started: ', games_won[1]/games[1])
    print('Games won when not started: ', games_won[0]/games[0])    
    print(games_won)
    print(point_cumulative)
    print(end_time - start_time)
    print()

def print_state(state: State):
    print("Current player: ", state.current_player)
    print("Current trick: ", state.tricks[-1])
    print("hands: ", state.hands)

def main2():
    # random.seed(13)
    round = Round(0, 'k', 0)
    state = State(round, 0)
    played_moves = []
    state.determine()
    for i in range(4):
        moves = state.legal_moves()
        # print("Legal moves: ", moves)
        move = random.choice(list(moves))
        # print("Move: ", move)
        state.do_move(move)
        
    state_copy = copy.deepcopy(state)
    # state_copy = state
    
    previous = state_copy
    
    # moves = state.legal_moves()
    # move = random.choice(list(moves))
    # print_state(state)
    # state.do_move(move)
    # print_state(state)
    # state.undo_move(move)
    # print_state(state)
    players = [[], []]
    # print("hands: ", round.player_hands)
    for i in range(7):
        for j in range(4):
            # print("player: ", state.current_player)
            moves = state.legal_moves()
            # print("Legal moves: ", moves)
            move = random.choice(list(moves))
            # print("Move: ", move)
            played_moves.append(move)
            players[0].append(state.current_player)
            state.do_move(move)
            # print("hands: ", round.player_hands)
    print(state.__dict__)
    played_moves.reverse()
    for move in played_moves:
        
        state.undo_move(move)
        players[1].insert(0, state.current_player)
        
        
    print(players[0])
    print(players[1])

    new = state
    print(previous.__dict__)
    print(new.__dict__)
    if previous.__dict__ != new.__dict__:
        raise Exception("not equal")
    if previous.hands != new.hands:
        raise Exception("hands not equal")
    if previous.tricks != new.tricks:
        raise Exception("tricks not equal")
    if previous.current_player != new.current_player:
        raise Exception("current_player not equal")
    if previous.possible_cards != new.possible_cards:
        raise Exception("possible_cards not equal")
    print("equal")
    
        
if __name__ == "__main__":
    main()
    # main2()
    # a = [Card(10), Card(11)]
    # b = a.copy()
    # a.remove(Card(10))
    # a = 5
    # print(a,b)

    # tijd = time.time()
    # # import numpy as np
    # # from AlphaZero.state import State

    # a = [1,2,3,4,5]
    # # asdf = [x for x in range(32)]
    # b = 0
    # for _ in range(10000000):
    #     if len(a) == 0:
    #     # if a == []:
    #         b = 10

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
