import random


from AlphaZero.alphazero import *
from rule_based_agent import Rule_player
from rounds import Round
from AlphaZero.state import State
from helper import *


def main3():
    random.seed(13)
    starting_player = random.choice([0,1,2,3])

    round = Round(starting_player, random.choice(['k', 'h', 'r', 's']), random.choice([0,1,2,3]))
    new = State(round, 0)

    for i in range(4):      
        print("own_hand: ", new.own_hand)
        print("possible_cards: ", new.possible_cards)
        print("current_player: ", new.current_player)
        print("cenre: ", new.centre)
        if new.current_player == 0:
            moves = new.legal_moves(new.own_hand, new.current_player)
            moves2 = round.legal_moves()
            if not set(moves) - set(moves2):
                raise Exception("moves do not match")
        else:
            moves = new.legal_moves(new.possible_cards[new.current_player], new.current_player)
        print("moves: ", moves)
        if type(moves[0]) == int:
            raise Exception("moves are not card objects")
        new.play_card(moves[0], new.current_player)
        

def main2():
    random.seed(13)
    starting_player = random.choice([0,1,2,3])
    print(starting_player)
    round = Round(starting_player, random.choice(['k', 'h', 'r', 's']), random.choice([0,1,2,3]))

    player = AlphaZero_player(starting_player)
    move = player.get_move(round)
    print("hallo", [card.id for card in round.legal_moves()])
    print([card.id for card in round.player_hands[round.current_player]])
    print(move.id)
    
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
                # current_player = (j + self.round.current_player) % 4
                current_player = self.round.current_player
                
                if current_player == 1 or current_player == 3:
                    
                    played_card = rule_player.get_card_good_player(self.round, current_player)
                    # moves = self.round.legal_moves()
                    # played_card = random.choice(moves)
                else:
                    if current_player == 0:
                        played_card = alpha_player_0.get_move()
                    else:
                        played_card = alpha_player_2.get_move()
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
                alpha_player_0.update_state(played_card.id)
                
                # print("player2")
                alpha_player_2.update_state(played_card.id)
                
                self.round.play_card(played_card)
            
            
        self.score[0] += self.round.points[0]+self.round.meld[0]
        self.score[1] += self.round.points[1]+self.round.meld[1]

def main():
    random.seed(13)
    games = [0,0]
    games_won = [0,0]

    points = []
    point_cumulative = [0,0]
    #Simulates the 10000 pre-generated games
    for i in range(200):
        # if i % 100 == 0:
        print(i)
            # print('Games won when started: ', games_won[1]/games[1])
        #     # print('Games won when not started: ', games_won[0]/games[0])
            # print(games_won)
        game = Game(random.choice([0,1,2,3]))
        game.play_game()
        starting_player = game.starting_player
        if game.score[1] > game.score[0]:
            games_won[starting_player%2] += 1
        games[starting_player % 2] += 1
        points.append(game.score)
        point_cumulative[0] += game.score[0]
        point_cumulative[1] += game.score[1]

        
    print('Games won when started: ', games_won[1]/games[1])
    print('Games won when not started: ', games_won[0]/games[0])    
    print(games_won)
    print(point_cumulative)

if __name__ == "__main__":
    main()
    # main2()
    # main3()
    pass