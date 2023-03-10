import random
import time

from AlphaZero.alphazero import *
from rule_based_agent import Rule_player
from rounds import Round
from AlphaZero.state import State
from helper import *



    
class Game:
    def __init__(self, starting_player):
        self.rounds = []
        self.score = [0,0]
        self.starting_player = starting_player
    
    #Plays a game of Klaverjas. Currently a game conists of 1 round
    def play_game(self):

        self.round = Round(self.starting_player, random.choice(['k', 'h', 'r', 's']), random.choice([0,1,2,3]))
        # self.round = Round(self.starting_player, random.choice(['k', 'h', 'r', 's']))
        rule_player = Rule_player()
        alpha_player_0 = AlphaZero_player(self.round, 0)
        alpha_player_2 = AlphaZero_player(self.round, 2)
        for i in range(8):
            for j in range(4):

                current_player = self.round.current_player
                
                if current_player == 1 or current_player == 3:
                    
                    played_card = rule_player.get_card_good_player(self.round, current_player)
                    # moves = self.round.legal_moves()
                    # played_card = random.choice(moves)
                else:
                    if current_player == 0:
                        played_card = alpha_player_0.get_move(self.round.trump_suit)
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
                # print("played card: ", played_card.id)
                # print("player0")
                alpha_player_0.update_state(played_card.id, self.round.trump_suit)
                
                # print("player2")
                alpha_player_2.update_state(played_card.id, self.round.trump_suit)
                
                self.round.play_card(played_card)
            
            
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
    for i in range(1000):
        if i % 10 == 0:
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

def main2():
    random.seed(13)
    new_round = Round(0, 'k', 0)
    print(new_round.player_hands)
    alpha_player_0 = AlphaZero_player(new_round, 0)
    print(alpha_player_0.state.hands)
    played_card = alpha_player_0.get_move(new_round.trump_suit)
    
    moves = new_round.legal_moves()
    
    found = False
    for move in moves:
        if move.id == played_card:
            played_card = move
            found = True
            break
    if not found:
        raise Exception("move not found")
    new_round.play_card(move)
class test():
    def __init__(self, id) -> None:
        self.id = id
        
    # def __eq__(self, other) -> bool:
    #     return self.__dict__ == other.__dict__
    def __eq__(self, other) -> bool:
        return self.id == other.id
    def __hash__(self) -> int:
        return hash(self.id)
    
class test2():
    def __init__(self, id) -> None:
        self.id = id
        
if __name__ == "__main__":
    main()
    # main2()
    # tes2 = test(2)
    # tes1 = test(2)
    
    # print(tes1)
    # print(tes2)
    # print(set([tes1]).intersection(set([tes2])))
    # if tes1 == tes2:
    #     print("equal")
    # if set([tes1]) == set([tes2]):
    #     print("equal2")
        
    # tes1.id = "2"
    # print(tes1.id)
    # print(tes2.id)
    # if tes1 == tes2:
    #     print("equal")
    # if set([tes1]) == set([tes2]):
    #     print("equal2")
    pass