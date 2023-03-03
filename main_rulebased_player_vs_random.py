import numpy as np
import random
import time
import copy
import tensorflow.keras as keras
from tensorflow.keras import layers


from rounds import Round
from tricks import Trick
from deck import Deck



class Rule_player:
    #Returns the card for the rule-based player
    def get_card_good_player(self, round, player):
        # player = round.current_player
        trick = round.tricks[-1]
        trump = round.trump_suit
        legal_moves = round.legal_moves()
        cant_follow = 0
        if len(trick.cards) == 0:
            for card in legal_moves:
                if card.value == round.get_highest_card(card.suit):
                    return card
            return self.get_lowest_card(legal_moves, trump)

        if legal_moves[0].suit == trick.cards[0].suit:
            cant_follow = 1
            
        if len(trick.cards) == 1:
            for card in legal_moves:
                if card.value == round.get_highest_card(trick.cards[0].suit):
                    return card
            return self.get_lowest_card(legal_moves, trump)

        if len(trick.cards) == 2:
            if cant_follow:
                return self.get_lowest_card(legal_moves, trump)

            if trick.cards[0].value == round.get_highest_card(trick.cards[0].suit):
                return self.get_highest_card(legal_moves, trump)


            for card in legal_moves:
                if card.value == round.get_highest_card(trick.cards[0].suit):
                    return card

            return self.get_lowest_card(legal_moves, trump)

        else:
            
            if trick.winner(trump) %2 == round.current_player %2:
                return self.get_highest_card(legal_moves, trump)

            highest = trick.highest_card(trump)
            for card in legal_moves:
                if card.order(trump) > highest.order(trump):
                    return card

            return self.get_lowest_card(legal_moves, trump)
    
    def get_lowest_card(self, legal_moves, trump):
        lowest_points = 21
        for card in legal_moves:
            if card.points(trump) < lowest_points:
                lowest_card = card
                lowest_points = card.points(trump)
        return lowest_card

    def get_highest_card(self, legal_moves, trump):
        highest_points = -1
        for card in legal_moves:
            if card.points(trump) > highest_points:
                highest_card = card
                highest_points = card.points(trump)
        return highest_card

class policy_network:
    def __init__(self) -> None:
        
        self.model = keras.models.Sequential([
            layers.Dense(43, activation='relu', input_shape=(43, )),
        
            layers.Dense(128, activation='relu'),
            
            layers.Dense(8, activation='softmax', dtype='float64')
        ])
        
        # define how to train the model
        self.model.compile(  optimizer='adam',
                        loss='sparse_categorical_crossentropy',
                        metrics=['accuracy'])
        
        # # here we train the model
        # model.fit(x_train, y_train, epochs=1, verbose=2)  
        self.model.build((None, 43))
        
    def __call__(self, game_state):
        return self.model(np.reshape(game_state, (1, -1)))

class Node:
    def __init__(self, round: Round, parent=None, move=None):
        self.round = round
        self.children = []
        self.parent = parent
        self.move = move
        self.score = 0
        self.visits = 0
    
    def expand(self):
        # for i in range(4):
        #     print("[ ")
        #     for card in self.round.player_cards[i]:
        #         print(card.value, card.suit)
        #     print("]")
        
        for card in self.round.legal_moves():
            new_round = copy.deepcopy(self.round)
            new_card = [new_card for new_card in new_round.legal_moves() if new_card.id == card.id][0]
            new_round.play_card(new_card)
            self.children.append(Node(new_round, self, card))

    def select_child_random(self):
        # print("Node", self, self.visits)
        return random.choice(self.children)
    
    def select_child_ucb(self):
        # print("Node", self, self.visits)
        # print("Children", [child.visits for child in self.children])
        c = 1.41
        ucbs = []
        for child in self.children:
            if child.visits == 0:
                return child
            if self.visits == 0:
                raise Exception("Visits is 0")
            ucbs.append(child.score / child.visits + c * np.sqrt(np.log(self.visits) / child.visits))
        index_max = np.argmax(np.array([ucbs]))
        return self.children[index_max]
    

class Alpha_zero_player:
    def __init__(self, player_position: int):
        self.player_position = player_position
        # self.policy_network = policy_network()
        # self.state

    def new_round(self, round: Round):
        self.current_trick = 0 # A number representing the current trick 
    
        self.game_state = self.round_to_game_state(round)
        
    def get_move(self, round: Round):
        return self.mcts(round)
        
    def mcts(self, round: Round):
        number_of_simulations = 50
        root = Node(round)
        # current_node = copy.deepcopy(root)
        current_node = root
        tijd = 10
        # print("hallo", round.legal_moves())
        for i in range(tijd):
            # Selection
            while not current_node.round.is_complete() and current_node.children:
                current_node = current_node.select_child_ucb()
                
            # Expansion
            if not current_node.round.is_complete():
                current_node.expand()
                current_node = current_node.select_child_random()
            
            # Simulation
            explore_round = copy.deepcopy(current_node.round)
            points = 0
            for _ in range(number_of_simulations):
                while not explore_round.is_complete():
                    explore_round.play_card(random.choice(explore_round.legal_moves()))
                points += explore_round.get_score(self.player_position)
            points /= number_of_simulations
            
            # Backpropagation
            while current_node.parent is not None:
                current_node.visits += 1
                current_node.score += points
                current_node = current_node.parent
            root.visits += 1
            
            
        
        best_score = -1
        for child in root.children:
            score = child.visits
            if score > best_score:
                best_score = score
                best_child = child
        # print("hallo2", [card.id for card in round.legal_moves()])
        # print(best_child.move.id)
        # return [new_card for new_card in new_round.legal_moves() if new_card.id == card.id][0]
        return best_child.move
        
    def old(self, round: Round):
        # return move
        for i in range(1):
            node = root
            current_node = node
            # selection
            while not current_node.round.is_complete() and current_node.children:
                current_node.play_card(current_node.round.legal_moves())
                if round.current_player == self.player_position:
                    
                    game_state = current_node.round.round_to_game_state(round)
                    policy = np.array(self.policy_network(self.game_state)[0])

                    choice = np.random.choice(list(range(8)), p=policy)
                    cards = self.game_state[:8]
                    cards = [self.card_untranform(card, round.trump_suit) for card in self.game_state[:8]]
                    legalmoves = round.legal_moves()
                    
                    print("hier", cards, legalmoves)
                    while cards[choice] not in legalmoves:
                        policy[choice] = 0
                        # print(policy)
                        policy = policy/np.sum(policy)
                        choice = np.random.choice(list(range(8)), p=policy)
                        
            

                    round.play_card(cards[choice])
                    self.player_position = (self.player_position+1)%4
                    print("played card", cards[choice])
                    print(round.tricks[-1].cards)
                    print(round.player_hands)
                    print(round.legal_moves())
                else:
                    hand = round.player_hands[round.current_player]
                    
            points += round.points[self.player_position%2]
        print(points)
            
    def round_to_game_state(self, round: Round):
        round_hand = round.player_hands[self.player_position] 
        # The hand of the tranformed to the game state representation
        hand = [self.card_transform(card, round.trump_suit) for card in round_hand] + [-1]*(8-len(round_hand))
        
        # 1 if the team of Player is declaring, 0 if the team of Player not declaring
        if round.declaring_team == self.player_position%2:
            declaring = 1
        else:
            declaring = 0
        
        # Creating the game state representation of the tricks
        played_tricks = [self.trick_transform(trick) for trick in reversed(round.tricks)] # The tricks that have been played starting from Player
        unplayed_tricks = [[-1, -1, -1, -1]]*(8-len(round.tricks))  # The tricks that have not been played
        tricks = played_tricks + unplayed_tricks # Combination of the played and unplayed tricks
        tricks = [item for sublist in tricks for item in sublist] # Flatten the list
    
        # The current score of the round
        score = round.points
        # print(len(hand), len(tricks), len(score))
        # Create the game state
        return np.array(hand + [declaring] + tricks + score)
       
    def trick_transform(self, trick: Trick) -> list[int]:
        "Makes the trick start with the cards of Player"
        cards = [-1, -1, -1, -1]
        for i, card in enumerate(trick.cards):
            cards[(i+trick.starting_player+(3-self.player_position))%4] = card
        return cards
    
    def card_transform(self, card: int, trump_suit: int) -> int:
        "Makes cards of the trump suit to have suit 0 and cards with suit 0 have suit trump_suit"
        suit = card_to_suit(card)
        if suit == trump_suit:
            return card_to_value(card)
        elif suit == 0:
            return trump_suit*10 + card_to_value(card)
        else:
            return card
    
    def card_untranform(self, card: int, trump_suit: int) -> int:
        "Makes cards of the trump suit to have suit trump_suit and cards with suit trump_suit have suit 0"
        suit = card_to_suit(card)
        if suit == 0:
            return trump_suit*10 + card_to_value(card)
        elif suit == trump_suit:
            return card_to_value(card)
        else:
            return card


def main2():
    random.seed(13)
    starting_player = random.choice([0,1,2,3])
    print(starting_player)
    round = Round(starting_player, random.choice(['k', 'h', 'r', 's']), random.choice([0,1,2,3]))

    player = Alpha_zero_player(starting_player)
    move = player.get_move(round)
    print("hallo", [card.id for card in round.legal_moves()])
    print([card.id for card in round.player_cards[round.current_player]])
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
        alpha_player_0 = Alpha_zero_player(0)
        alpha_player_2 = Alpha_zero_player(2)
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
                        played_card = alpha_player_0.get_move(self.round)
                    else:
                        played_card = alpha_player_2.get_move(self.round)
                    # moves = self.round.legal_moves()
                    # played_card = random.choice(moves)
                    
                
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
    for i in range(1000):
        if i % 100 == 0:
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
# 