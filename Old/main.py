import random
import numpy as np
import tensorflow.keras as keras
from tensorflow.keras import layers


from round import Round
from trick import Trick
from helper import *


class Random_player:
    def __init__(self) -> None:
        pass
    
    def new_round(self):
        pass
    
    def get_move(self, round: Round):
        return random.choice(round.legal_moves())
        
class Rule_player:
    def __init__(self) -> None:
        pass
    
    #Returns the card for the rule-based player
    def get_move(self, round: Round) -> int:
        # print("player hands: ", round.player_hands)
        # print("current player: ", round.current_player)
        # print("trump suit: ", round.trump_suit)
        # print("tricks: ", [trick.cards for trick in round.tricks])
        # print("legal moves: ", round.legal_moves())
        # print("cards left: ", round.cardsleft)
        
        trick = round.tricks[-1]
        trump = round.trump_suit
        legal_moves = round.legal_moves()
        
        if len(trick.cards) == 0:
            for card in legal_moves:
                if card_to_value(card) == round.get_highest_card(card_to_suit(card)):
                    return card
            return self.get_lowest_card(legal_moves, trump)
          
        elif len(trick.cards) == 1:
            for card in legal_moves:
                if card_to_value(card) == round.get_highest_card(card_to_suit(trick.cards[0])):
                    return card
            return self.get_lowest_card(legal_moves, trump)
                

        elif len(trick.cards) == 2:
            if card_to_suit(legal_moves[0]) == card_to_suit(trick.cards[0]):
                return self.get_lowest_card(legal_moves, trump)

            if card_to_value(trick.cards[0]) == round.get_highest_card(card_to_suit(trick.cards[0])):
                return self.get_highest_card(legal_moves, trump)


            for card in legal_moves:
                if card_to_value(card) == round.get_highest_card(card_to_suit(trick.cards[0])):
                    return card

            return self.get_lowest_card(legal_moves, trump)

        else:
            if trick.winner(trump) %2 == round.current_player%2:
                return self.get_highest_card(legal_moves, trump)

            highest = trick.highest_card(trump)
            for card in legal_moves:
                if card_to_order(card, trump) > card_to_order(highest, trump):
                    return card

            return self.get_lowest_card(legal_moves, trump)
    
    def get_lowest_card(self, legal_moves, trump):
        lowest_points = 21
        for card in legal_moves:
            if card_to_points(card, trump) < lowest_points:
                lowest_card = card
                lowest_points = card_to_points(card, trump)
        return lowest_card

    def get_highest_card(self, legal_moves, trump):
        highest_points = -1
        for card in legal_moves:
            if card_to_points(card, trump) > highest_points:
                highest_card = card
                highest_points = card_to_points(card, trump)
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

    
class Alpha_zero_player:
    def __init__(self, player_position: int):
        self.player_position = player_position
        self.policy_network = policy_network()
        # self.state

    def new_round(self, round: Round):
        self.current_trick = 0 # A number representing the current trick 
    
        self.game_state = self.round_to_game_state(round)
          
    def update(self, round: Round):
        self.game_state = self.round_to_game_state(round)
        
    def get_move(self, round: Round):
        self.policy_network(self.game_state)
        # position
        # do seach
        self.search(round)
        
        
        
    def search(self, start_state):
        pass
    def search2(self, round: Round):
        # do search
        
        points = 0
        # return move
        for i in range(1):
            while not round.is_complete():
                if round.current_player == self.player_position:
                    
                    self.game_state = self.round_to_game_state(round)
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
    # player = Alpha_zero_player(0)
    # round = Round(0, 1, 2, True)
    # player.new_round(round)
    # player.get_move(round)
    
    round = Round(0, 1, 2)
    print(round.player_hands)
    print(round.cardsleft)
    round.play_card(1)
    print(round.player_hands)
    print(round.cardsleft)

def main():
    points = [0, 0]
    meld = [0, 0]
    pit = [0, 0]
    wins = [0, 0]

    import time 
    start = time.time()

    # random.seed(13)
    # Create Players
    random_player = Random_player()
    rule_player = Rule_player()
    # alpha_zero_player = Alpha_zero_player()
    
    for _ in range(5000):

        # Create new round
        round = Round(random.choice([0,1,2,3]), random.choice([0,1,2,3]), random.choice([0,1,2,3]))

        
        # Give players the new round
        # alpha_zero_player.new_round(round)


        for _ in range(8):
            for j in range(4):
                current_player = (j + round.current_player) % 4
                
                if current_player == 0 or current_player == 2:
                    # TEAM SOUTH (0) AND NORTH (2)
                    # choice = random_player.get_move(round)
                    choice = rule_player.get_move(round)
                    # choice = alpha_zero_player.get_move()
                    
                    # print("choice", choice)

                    # Play card
                    round.play_card(choice)
                                     
                else:
                    # TEAM EAST (1) AND WEST (3)
                    choice = random_player.get_move(round)
                    # choice = rule_player.get_move(round)
                    # choice = alpha_zero_player.get_move()
                        
                    
                        
                    # Play card
                    round.play_card(choice)
                


        points[0] += round.points[0]
        points[1] += round.points[1]
        meld[0] += round.meld[0]
        meld[1] += round.meld[1]
        pit[0] += round.pit[0]
        pit[1] += round.pit[1]
        wins[0] += round.wins[0]
        wins[1] += round.wins[1]
    end = time.time()
    print("Time: ", end - start)
    print("Points: ", points)
    print("Meld: ", meld)
    print("Pit: ", pit)
    print("Wins: ", wins)

    
    
if __name__ == '__main__':
    main()
