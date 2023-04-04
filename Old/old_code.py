# from deck import Card


# meld_20 = []
# meld_50 = []
# meld_100 = []
# possible_street = []
# suits = ['k', 'h', 'r', 's']
# values = [7, 8, 9, 10, 11, 12, 13, 14]
# for suit in suits:
#     for idx in range(7,13):
#         meld_20.append({Card(value, suit)
#                         for value in range(idx, idx + 3)})
#     for idx in range(7,12):
#         meld_50.append({Card(value, suit)
#                         for value in range(idx, idx + 4)})
#     for idx in range(7,14):
#         possible_street.append({Card(value, suit)
#                         for value in [idx, idx+1]})
#     for idx in range(7,13):
#         possible_street.append({Card(value, suit)
#                         for value in [idx, idx+2]})

# for value in values:
#     meld_100.append({Card(value, suit) for suit in suits})


# #Checks whether there are meld points on the board
# def meld_points(trick, trump_suit):
#     for meld in meld_100:
#         if meld <= set(trick):
#             return 100

#     points = 0
#     royal = {Card(trump_suit, 12), Card(trump_suit, 13)}
#     if royal <= set(trick):
#         points = 20

#     for meld in meld_50:
#         if meld <= set(trick):
#             return points + 50
#     for meld in meld_20:
#         if meld <= set(trick):
#             return points + 20
#     return points

# #Checks whether a street can be made
# def check_possible_street(center, card):
#     center.append(card)
#     for meld in meld_20:
#         if meld <= set(center):
#             center.pop()
#             return 1
#     center.pop()
#     return 0

#     def set_state_with_round(self, round: Round):
#         own_hand = round.player_hands[self.own_position] 
#         # The hand of the transformed to the game state representation
#         self.own_hand = [card_transform(card.id, round.trump_suit) for card in own_hand] + [-1]*(8-len(own_hand))
        
#         # 1 if the team of Player is declaring, 0 if the team of Player not declaring
#         if round.declaring_team == self.own_position%2:
#             self.declaring = 1
#         else:
#             self.declaring = 0
        
#         # # Creating the game state representation of the tricks
#         # played_tricks = [self.trick_transform(trick) for trick in reversed(round.tricks)] # The tricks that have been played starting from Player
#         # unplayed_tricks = [[-1, -1, -1, -1]]*(8-len(round.tricks))  # The tricks that have not been played
#         # tricks = played_tricks + unplayed_tricks # Combination of the played and unplayed tricks
#         # self.tricks = [item for sublist in tricks for item in sublist] # Flatten the list
    
#         # The current score of the round
#         self.points = round.points
       
#     # def trick_transform(self, trick: Trick) -> list[int]:
#     #     "Makes the trick start with the cards of Player"
#     #     cards = [-1, -1, -1, -1]
#     #     for i, card in enumerate(trick.cards):
#     #         cards[(i+trick.starting_player+(3-self.own_position))%4] = card
#     #     return cards
    

#     def mcts2(self, round: Round):
#         number_of_simulations = 50
#         root = Node(round)
#         # current_node = copy.deepcopy(root)
#         current_node = root
#         tijd = 10
#         # print("hallo", round.legal_moves())
#         for i in range(tijd):
        
#             # Selection
#             while not current_node.state.is_complete() and current_node.children:
#                 current_node = current_node.select_child_ucb()
                
#             # Expansion
#             if not current_node.state.is_complete():
#                 current_node.expand(self.player_position)
#                 current_node = current_node.select_child_random()
            
#             # Simulation
#             explore_round = copy.deepcopy(current_node.state)
#             points = 0
#             for _ in range(number_of_simulations):
#                 while not explore_round.is_complete():
#                     explore_round.play_card(random.choice(explore_round.legal_moves()))
#                 points += explore_round.get_score(self.player_position)
#             points /= number_of_simulations
            
#             # Backpropagation
#             while current_node.parent is not None:
#                 current_node.visits += 1
#                 current_node.score += points
#                 current_node = current_node.parent
#             root.visits += 1
            
            
        
#         best_score = -1
#         for child in root.children:
#             score = child.visits
#             if score > best_score:
#                 best_score = score
#                 best_child = child
#         # print("hallo2", [card.id for card in round.legal_moves()])
#         # print(best_child.move.id)
#         # return [new_card for new_card in new_round.legal_moves() if new_card.id == card.id][0]
#         return best_child.move
        
#     # def old(self, round: Round):
#     #     # return move
#     #     for i in range(1):
#     #         node = root
#     #         current_node = node
#     #         # selection
#     #         while not current_node.round.is_complete() and current_node.children:
#     #             current_node.play_card(current_node.round.legal_moves())
#     #             if round.current_player == self.player_position:
                    
#     #                 game_state = current_node.round.round_to_game_state(round)
#     #                 policy = np.array(self.policy_network(self.game_state)[0])

#     #                 choice = np.random.choice(list(range(8)), p=policy)
#     #                 cards = self.game_state[:8]
#     #                 cards = [self.card_untranform(card, round.trump_suit) for card in self.game_state[:8]]
#     #                 legalmoves = round.legal_moves()
                    
#     #                 print("hier", cards, legalmoves)
#     #                 while cards[choice] not in legalmoves:
#     #                     policy[choice] = 0
#     #                     # print(policy)
#     #                     policy = policy/np.sum(policy)
#     #                     choice = np.random.choice(list(range(8)), p=policy)
                        
            

#     #                 round.play_card(cards[choice])
#     #                 self.player_position = (self.player_position+1)%4
#     #                 print("played card", cards[choice])
#     #                 print(round.tricks[-1].cards)
#     #                 print(round.player_hands)
#     #                 print(round.legal_moves())
#     #             else:
#     #                 hand = round.player_hands[round.current_player]
                    
#     #         points += round.points[self.player_position%2]
#     #     print(points)
    
#     # def set_state_with_round(self, round: Round):
#     #     own_hand = round.player_hands[self.own_position] 
#     #     # The hand of the tranformed to the game state representation
#     #     self.own_hand = [self.card_transform(card.id, round.trump_suit) for card in own_hand] + [-1]*(8-len(own_hand))
        
#     #     # 1 if the team of Player is declaring, 0 if the team of Player not declaring
#     #     if round.declaring_team == self.own_position%2:
#     #         self.declaring = 1
#     #     else:
#     #         self.declaring = 0
        
#     #     # Creating the game state representation of the tricks
#     #     played_tricks = [self.trick_transform(trick) for trick in reversed(round.tricks)] # The tricks that have been played starting from Player
#     #     unplayed_tricks = [[-1, -1, -1, -1]]*(8-len(round.tricks))  # The tricks that have not been played
#     #     tricks = played_tricks + unplayed_tricks # Combination of the played and unplayed tricks
#     #     self.tricks = [item for sublist in tricks for item in sublist] # Flatten the list
    
#     #     # The current score of the round
#     #     self.score = round.points
       
#     # def trick_transform(self, trick: Trick) -> list[int]:
#     #     "Makes the trick start with the cards of Player"
#     #     cards = [-1, -1, -1, -1]
#     #     for i, card in enumerate(trick.cards):
#     #         cards[(i+trick.starting_player+(3-self.own_position))%4] = card
#     #     return cards
    
#     # def card_transform(self, card: int, trump_suit: int) -> int:
#     #     "Makes cards of the trump suit to have suit 0 and cards with suit 0 have suit trump_suit"
#     #     suit = card_to_suit(card)
#     #     if suit == trump_suit:
#     #         return card_to_value(card)
#     #     elif suit == 0:
#     #         return trump_suit*10 + card_to_value(card)
#     #     else:
#     #         return card
    
#     # def card_untranform(self, card: int, trump_suit: int) -> int:
#     #     "Makes cards of the trump suit to have suit trump_suit and cards with suit trump_suit have suit 0"
#     #     suit = card_to_suit(card)
#     #     if suit == 0:
#     #         return trump_suit*10 + card_to_value(card)
#     #     elif suit == trump_suit:
#     #         return card_to_value(card)
#     #     else:
#     #         return card
    
    
#         # else:
#         #     # print("Expand2")

            
#         #     possible_hands = list(itertools.combinations(set(self.state.possible_cards[self.state.current_player]), 8-self.state.number_of_tricks))
#         #     possible_hands = random.sample(possible_hands, min(10, len(possible_hands)))
#         #     # print("TYPE", type(possible_hands[0]))
#         #     # print("LEN", len(possible_hands))
#         #     for hand in possible_hands:
#         #         moves = self.state.legal_moves(hand)
#         #         for card in moves:
#         #             new_round = copy.deepcopy(self.state)
#         #             new_card = [new_card for new_card in new_round.possible_cards[new_round.current_player] if new_card.id == card.id][0]
#         #             # new_card = [new_card for new_card in new_round.legal_moves(hand) if new_card.id == card.id][0]
#         #             new_round.play_card(new_card)
#         #             self.children.append(Node(new_round, self, card))
        
# # def main3():
# #     random.seed(13)
# #     starting_player = random.choice([0,1,2,3])

# #     round = Round(starting_player, random.choice(['k', 'h', 'r', 's']), random.choice([0,1,2,3]))
# #     new = State(round, 0)

# #     for i in range(4):      
# #         print("own_hand: ", new.own_hand)
# #         print("possible_cards: ", new.possible_cards)
# #         print("current_player: ", new.current_player)
# #         print("cenre: ", new.centre)
# #         if new.current_player == 0:
# #             moves = new.legal_moves(new.own_hand, new.current_player)
# #             moves2 = round.legal_moves()
# #             if not set(moves) - set(moves2):
# #                 raise Exception("moves do not match")
# #         else:
# #             moves = new.legal_moves(new.possible_cards[new.current_player], new.current_player)
# #         print("moves: ", moves)
# #         if type(moves[0]) == int:
# #             raise Exception("moves are not card objects")
# #         new.play_card(moves[0], new.current_player)
        

# # def main2():
# #     random.seed(13)
# #     starting_player = random.choice([0,1,2,3])
# #     print(starting_player)
# #     round = Round(starting_player, random.choice(['k', 'h', 'r', 's']), random.choice([0,1,2,3]))

# #     player = AlphaZero_player(starting_player)
# #     move = player.get_move(round)
# #     print("hallo", [card.id for card in round.legal_moves()])
# #     print([card.id for card in round.player_hands[round.current_player]])
# #     print(move.id)

# # print("Card played: ", card)
# # print("possible_cards: ", self.possible_cards)
# # card_removed = False
# # for i in range(4):
# #     if card in self.possible_cards[i]:
# #         self.possible_cards[i].remove(card)
#         # card_removed = True
        
# # if not card_removed:
# #     raise Exception("Card not in hand")

#             # for i in range(4):
#             #     if len(self.other_players_cards) != 0:
#             #         raise Exception("Not all cards played")                
#             #     # if len(self.possible_cards[i]) != 0:
#             #     #     pass
#             #     #     raise Exception("Not all cards played")
            
#     # main2()
#     # main3()
#     # innx = 1
#     # tes = test(1)
    
#     # list = [1,2,3,4]
#     # list2 = [0,0,0,0]
#     # timetime = time.time()
#     # sum = 0
#     # for _ in range(100):
#     #     time.sleep(0.1)
#     #     for _ in range(10000):
#     #         # sum += innx
#     #         sum += tes.id
#     # print(sum)
#     # print(time.time() - timetime)
    
#             # temp_state = copy.deepcopy(self.state)
#             # new_state = self.state
#             # self.state = temp_state
#             # new_card = [new_card for new_card in new_state.legal_moves() if new_card.id == card.id][0
#         # for card in self.state.legal_moves():
#         #     new_state = copy.deepcopy(self.state)
#         #     new_state.play_card(card)
#         #     self.children.add(Node(new_state, self, card))
        





























# # from __future__ import annotations # To use the class name in the type hinting

# # import numpy as np
# # import random
# # import copy
# # import itertools
# # import time

# # from typing import List


# # from AlphaZero.card import Card
# # from rounds import Round
# # # from tricks import Trick
# # from AlphaZero.state import State
# # from AlphaZero.helper import card_transform, card_untransform
# # # from helper import *


# # class Node:
# #     def __init__(self, state: State, parent: Node = None, move: Card = None):
# #         self.state = state
# #         self.children = set()
# #         self.parent = parent
# #         self.move = move
# #         self.score = 0
# #         self.visits = 0
    
# #     def __repr__(self) -> str:
# #         return f"Node({self.move}, {self.score}, {self.visits})"
    
# #     def __eq__(self, other: Node) -> bool:
# #         # raise NotImplementedError
# #         return self.move == other.move
    
# #     def __hash__(self) -> int:
# #         # raise NotImplementedError
# #         return hash(self.move)

# #     def set_legal_children(self):
# #         legal_moves = self.state.legal_moves()
# #         self.legal_children = set()
# #         for move in legal_moves:
# #             new_state = copy.deepcopy(self.state)
# #             new_state.play_card(move)
# #             self.legal_children.add(Node(new_state, self, move))
        
# #     def expand(self):
# #         for node in self.legal_children:
# #             self.children.add(node)

# #     def select_child_random(self) -> Node:
# #         return random.choice(list(self.legal_children.intersection(self.children)))
# #         # return random.choice(list(self.legal_children))
    
# #     def select_child_ucb(self) -> Node:
# #         c = 1
# #         ucbs = []
# #         children_list = list(self.legal_children.intersection(self.children))
# #         # children_list = list(self.legal_children)
# #         for child in children_list:
# #             if child.visits == 0:
# #                 return child
# #             ucbs.append(child.score / child.visits + c * np.sqrt(np.log(self.visits) / child.visits))
# #         index_max = np.argmax(np.array([ucbs]))
# #         return children_list[index_max]
    
# # class AlphaZero_player:
# #     def __init__(self, round: Round, player_position: int, debug = False):
# #         self.player_position = player_position
# #         self.state = State(round, player_position)
# #         # self.policy_network = policy_network()

# #         self.debug = debug
# #     def update_state(self, move: int, trump_suit: str):

# #         move = Card(card_transform(move, ['k', 'h', 'r', 's'].index(trump_suit)))
# #         self.state.play_card(move, simulation=False)

    
# #     def get_move(self, trump_suit: str):
# #         card_id = self.mcts().id
        
# #         return card_untransform(card_id, ['k', 'h', 'r', 's'].index(trump_suit))

# #     def mcts(self):
        
# #         root = Node(copy.deepcopy(self.state))

# #         current_node = root
# #         number_of_simulations = 5
# #         tijd = 10

# #         for _ in range(tijd):
# #             # Determination
# #             current_node.state.determine()
# #             current_node.set_legal_children()

# #             i = 0
# #             # Selection
# #             while not current_node.state.round_complete() and current_node.legal_children-current_node.children == set():
# #                 i += 1
# #             # while not current_node.state.round_complete() and current_node.children:
# #                 prev_state = copy.deepcopy(current_node.state)
# #                 current_node = current_node.select_child_ucb()
# #                 prev_state.play_card(current_node.move)
# #                 current_node.state = prev_state
# #                 current_node.set_legal_children()
            
# #             # Expansion
# #             if not current_node.state.round_complete():
# #                 current_node.expand()
# #                 current_node = current_node.select_child_random()
# #                 current_node.set_legal_children()
                
# #             # Simulation
# #             # explore_state = copy.deepcopy(current_node.state)
# #             points = 0
# #             for _ in range(number_of_simulations):
# #                 explore_state = copy.deepcopy(current_node.state)
# #                 while not explore_state.round_complete():
                    
# #                     move = random.choice(list(explore_state.legal_moves()))
# #                     explore_state.play_card(move)
                    
# #                 points += explore_state.get_score(self.player_position)
# #             points /= number_of_simulations
            
# #             # Backpropagation
# #             while current_node.parent is not None:
# #                 current_node.visits += 1
# #                 current_node.score += points
# #                 current_node = current_node.parent
# #             root.visits += 1

# #         best_score = -1
# #         for child in root.children:
# #             score = child.visits
# #             if score > best_score:
# #                 best_score = score
# #                 best_child = child
                
# #         return best_child.move



# # if played_card.suit != 0 or played_card.order() < self.centre.highest_trump().order():
# #     if played_card.suit == 0:
# #         # remove higher trump cards from the current player
# #         pass
# #     else:
# #         # remove all trump cards from the current player
# #         pass
#     # if leading_suit == 0:
#     #     if played_card.suit != 0 : # and
#     #         # print("self.possible_cards[self.current_player]", self.possible_cards)
#     #         # print("cards left", self.cards_left)
#     #         # print("current player", self.current_player)
#     #         # print("card played", card_played)
#     #         # print("centre", self.centre)
#     #         # print("hier", {card for card in self.possible_cards[self.current_player] 
#     #         #                                              if card.id in {0,1,2,3,4,5,6,7}})
#     #         # remove all trump cards from the current player
#     #         pass
#     #         # self.possible_cards[self.current_player] -= {card for card in self.possible_cards[self.current_player] 
#     #         #                                              if card.id in {0,1,2,3,4,5,6,7}}
#     #         # print("self.possible_cards[self.current_player]", self.possible_cards)
#     #         # input("Press Enter to continue...")
#     #     elif (highest_trump_order := self.centre.highest_trump().order()) > played_card.order():
#     #         # print("hier2", {card for card in self.possible_cards[self.current_player] if card.id in [0,1,5,6,3,7,2,4][highest_trump_order-8:]})
#     #         # remove all trump cards higher then the highest trump card from the current player
#     #         pass
#     #         # self.possible_cards[self.current_player] -= {card for card in self.possible_cards[self.current_player] 
#     #         #                                              if card.id in [0,1,5,6,3,7,2,4][highest_trump_order-8:]}
#     # else:
#     #     if played_card.suit != leading_suit:
#     #         # print("hier3", {Card(leading_suit*10 + i) for i in range(8)})
#     #         # asdf = True
#     #         # raise Exception("card played is not of the leading suit")
#     #         # remove all cards of the leading suit from the current player
#     #         pass
#     #         # self.possible_cards[self.current_player] -= {Card(leading_suit*10 + i) for i in range(8)}

#     # # print("updated possible cards", self.possible_cards)
#     # # if asdf:
#     # #     raise Exception("card played is not of the leading suit")
        # print("HIER")
        # Kies een kaart per speler
        # other_players = [i for i in range(4) if i != self.own_position]
        # print(other_players)
        # go = True
        # count = 0
        # while go:
        #     go = False
        #     possible_cards = copy.deepcopy(self.possible_cards)

        #     count += 1
        #     if count % 10000 == 0:
        #         print(count)
        #         print(possible_cards)
        #         print(self.cards_left)
            
        #     for player in other_players:
        #         if len(possible_cards[player]) < self.cards_left[player]:
        #             go = True
        #             break
        #         self.hands[player] = set(random.sample(possible_cards[player], self.cards_left[player]))
                
        #         for cards in possible_cards:
        #             cards -= self.hands[player]
    
        # other_players = [i for i in range(4) if i != self.own_position]
        # other_players_cards = list(self.other_players_cards)
        # for player in other_players:
        #     self.hands[player] = set()
        #     for _ in range(self.cards_left[player]):
        #         choice = random.sample(other_players_cards, 1)[0]
        #         self.hands[player].add(choice)
        #         other_players_cards.remove(choice)
        
#     def find_card_configuration(self, hand: list[set], possible_cards: list[list], player: int, num_cards_to_add: list[int]) -> bool:
#         if player == 3:
#             # if num_cards_to_add != [0, 0, 0]:
#             #     raise Exception("Not all cards added")
#             return True
#         elif num_cards_to_add[player] == 0:
#             return self.find_card_configuration(hand, possible_cards, player+1, num_cards_to_add)
#         else:
#             wont_work = False
#             cards = possible_cards[player].copy()
#             # possible_cards_copy = copy.deepcopy(possible_cards)
#             for card in cards:
#                 had_card = []
#                 for other_player in range(player+1, 3):
#                     if card in possible_cards[other_player]:
#                         had_card.append(other_player)
#                         possible_cards[other_player].remove(card)
#                         if len(possible_cards[other_player]) < num_cards_to_add[other_player]:
#                             wont_work = True
#                             for player_had_card in had_card:
#                                 possible_cards[player_had_card].append(card)
#                             break
                        
#                 if wont_work:
#                     wont_work = False
#                     continue
#                 all_possible_cards = set(possible_cards[0]) | set(possible_cards[1]) | set(possible_cards[2])
#                 # print("all_possible_cards", all_possible_cards)
#                 # print("num_cards_to_add", sum(num_cards_to_add))
#                 if len(all_possible_cards) < sum(num_cards_to_add):
#                     raise Exception("Not enough cards")
#                     for player_had_card in had_card:
#                         possible_cards[player_had_card].append(card)
#                     continue
                    
#                 hand[player].add(card)
#                 num_cards_to_add[player] -= 1

#                 possible_cards[player].remove(card)

#                 if self.find_card_configuration(hand, possible_cards, player, num_cards_to_add):
#                     return True
                
#                 possible_cards[player].append(card)
                
#                 num_cards_to_add[player] += 1
#                 hand[player].remove(card)
#                 for player_had_card in had_card:
#                     possible_cards[player_had_card].append(card)

#             return False
        
#     def determine(self):         
#         other_players = [0,1,2,3]
#         other_players.pop(self.own_position)
        
#         # print("possible_cards", self.possible_cards)
#         # possible_cards = copy.deepcopy(self.possible_cards)
        
#         # real_hands_id = [[card_transform(card.id, ['k', 'h', 'r', 's'].index(self.round.trump_suit)) 
#         #                     for card in self.round.player_hands[i]] for i in range(4)]
#         # real_hands = [{Card(id) for id in hand} for hand in real_hands_id]

#         # # print("real hand2", real_hands)
#         # for i in range(4):
#         #     if real_hands[i] - self.possible_cards[i] != set():
#         #         # print(possible_cards)
#         #         raise Exception("Real hand not possible")
        
#         possible_cards = [list(cards) for cards in self.possible_cards]
#         # print("HIER", possible_cards)
#         # print(self.own_position)
#         possible_cards.pop(self.own_position)
#         for i in possible_cards:
#             random.shuffle(i)
#         hand = [set(), set(), set()]
#         cards_left = copy.deepcopy(self.cards_left)
#         # cards_left = self.cards_left.copy()
#         cards_left.pop(self.own_position)
        
#         print(random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13]))
#         if not self.find_card_configuration(hand, possible_cards, 0, cards_left):
#             raise Exception("Could not find a card configuration")
#         # if cards_left != [0, 0, 0]:
#         #     # print(possible_cards)
#         #     # print(hand)
#         #     # print(cards_left)
#         #     # print(self.cards_left)
#         #     raise Exception("Not all cards added1")
#         # possible_cards = copy.deepcopy(self.possible_cards)
#         # possible_cards = [list(cards) for cards in possible_cards]
#         # # print("HIER", possible_cards)
#         # # print(self.own_position)
#         # possible_cards.pop(self.own_position)
#         # for i in range(3):
#         #     if hand[i] - set(possible_cards[i]) != set():
#         #         # print("hand", hand)
#         #         # print(possible_cards)
#         #         # print(self.round.player_hands)
#         #         # print(self.round.trump_suit)
#         #         # print(self.own_position)
#         #         raise Exception("Not all cards added2")
#         for index, player in enumerate(other_players):
#             self.hands[player] = hand[index]
#             # if len(hand[index]) != self.cards_left[player]:
#             #     raise Exception("Not all cards added3")

#     def to_nparray(self):
#         own_position = self.own_position
        
#         array = np.zeros((38, 1))
#         new_players = [1,-1,2,-2]
#         # add hand cards to cards section
#         for player in range(4):
#             new_player = new_players[(player - own_position) % 4]
#             for card in self.hands[player]:
#                 array[card.id] = new_player
#         # add played cards to cards section
#         for trick in self.tricks:
#             for card in trick.cards:
#                 array[card.id] = 0
#         # add centre to centre section starting from player_id's perspective
#         for i in range(4):
#             array[32+i] = -1
#         for index, card in enumerate(self.tricks[-1]):
#             array[32+(index-self.tricks[-1].starting_player+own_position)] = card.id
        
#         if self.declaring_team == own_position % 2: # if player is on declaring team
#             array[36] = 1
#         else:
#             array[36] = -1

#         array[37] = self.get_score(own_position)
        
#         return array