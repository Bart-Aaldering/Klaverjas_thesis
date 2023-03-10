from deck import Card


meld_20 = []
meld_50 = []
meld_100 = []
possible_street = []
suits = ['k', 'h', 'r', 's']
values = [7, 8, 9, 10, 11, 12, 13, 14]
for suit in suits:
    for idx in range(7,13):
        meld_20.append({Card(value, suit)
                        for value in range(idx, idx + 3)})
    for idx in range(7,12):
        meld_50.append({Card(value, suit)
                        for value in range(idx, idx + 4)})
    for idx in range(7,14):
        possible_street.append({Card(value, suit)
                        for value in [idx, idx+1]})
    for idx in range(7,13):
        possible_street.append({Card(value, suit)
                        for value in [idx, idx+2]})

for value in values:
    meld_100.append({Card(value, suit) for suit in suits})


#Checks whether there are meld points on the board
def meld_points(trick, trump_suit):
    for meld in meld_100:
        if meld <= set(trick):
            return 100

    points = 0
    royal = {Card(trump_suit, 12), Card(trump_suit, 13)}
    if royal <= set(trick):
        points = 20

    for meld in meld_50:
        if meld <= set(trick):
            return points + 50
    for meld in meld_20:
        if meld <= set(trick):
            return points + 20
    return points

#Checks whether a street can be made
def check_possible_street(center, card):
    center.append(card)
    for meld in meld_20:
        if meld <= set(center):
            center.pop()
            return 1
    center.pop()
    return 0

    def set_state_with_round(self, round: Round):
        own_hand = round.player_hands[self.own_position] 
        # The hand of the transformed to the game state representation
        self.own_hand = [card_transform(card.id, round.trump_suit) for card in own_hand] + [-1]*(8-len(own_hand))
        
        # 1 if the team of Player is declaring, 0 if the team of Player not declaring
        if round.declaring_team == self.own_position%2:
            self.declaring = 1
        else:
            self.declaring = 0
        
        # # Creating the game state representation of the tricks
        # played_tricks = [self.trick_transform(trick) for trick in reversed(round.tricks)] # The tricks that have been played starting from Player
        # unplayed_tricks = [[-1, -1, -1, -1]]*(8-len(round.tricks))  # The tricks that have not been played
        # tricks = played_tricks + unplayed_tricks # Combination of the played and unplayed tricks
        # self.tricks = [item for sublist in tricks for item in sublist] # Flatten the list
    
        # The current score of the round
        self.points = round.points
       
    # def trick_transform(self, trick: Trick) -> list[int]:
    #     "Makes the trick start with the cards of Player"
    #     cards = [-1, -1, -1, -1]
    #     for i, card in enumerate(trick.cards):
    #         cards[(i+trick.starting_player+(3-self.own_position))%4] = card
    #     return cards
    

    def mcts2(self, round: Round):
        number_of_simulations = 50
        root = Node(round)
        # current_node = copy.deepcopy(root)
        current_node = root
        tijd = 10
        # print("hallo", round.legal_moves())
        for i in range(tijd):
        
            # Selection
            while not current_node.state.is_complete() and current_node.children:
                current_node = current_node.select_child_ucb()
                
            # Expansion
            if not current_node.state.is_complete():
                current_node.expand(self.player_position)
                current_node = current_node.select_child_random()
            
            # Simulation
            explore_round = copy.deepcopy(current_node.state)
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
        
    # def old(self, round: Round):
    #     # return move
    #     for i in range(1):
    #         node = root
    #         current_node = node
    #         # selection
    #         while not current_node.round.is_complete() and current_node.children:
    #             current_node.play_card(current_node.round.legal_moves())
    #             if round.current_player == self.player_position:
                    
    #                 game_state = current_node.round.round_to_game_state(round)
    #                 policy = np.array(self.policy_network(self.game_state)[0])

    #                 choice = np.random.choice(list(range(8)), p=policy)
    #                 cards = self.game_state[:8]
    #                 cards = [self.card_untranform(card, round.trump_suit) for card in self.game_state[:8]]
    #                 legalmoves = round.legal_moves()
                    
    #                 print("hier", cards, legalmoves)
    #                 while cards[choice] not in legalmoves:
    #                     policy[choice] = 0
    #                     # print(policy)
    #                     policy = policy/np.sum(policy)
    #                     choice = np.random.choice(list(range(8)), p=policy)
                        
            

    #                 round.play_card(cards[choice])
    #                 self.player_position = (self.player_position+1)%4
    #                 print("played card", cards[choice])
    #                 print(round.tricks[-1].cards)
    #                 print(round.player_hands)
    #                 print(round.legal_moves())
    #             else:
    #                 hand = round.player_hands[round.current_player]
                    
    #         points += round.points[self.player_position%2]
    #     print(points)
    
    # def set_state_with_round(self, round: Round):
    #     own_hand = round.player_hands[self.own_position] 
    #     # The hand of the tranformed to the game state representation
    #     self.own_hand = [self.card_transform(card.id, round.trump_suit) for card in own_hand] + [-1]*(8-len(own_hand))
        
    #     # 1 if the team of Player is declaring, 0 if the team of Player not declaring
    #     if round.declaring_team == self.own_position%2:
    #         self.declaring = 1
    #     else:
    #         self.declaring = 0
        
    #     # Creating the game state representation of the tricks
    #     played_tricks = [self.trick_transform(trick) for trick in reversed(round.tricks)] # The tricks that have been played starting from Player
    #     unplayed_tricks = [[-1, -1, -1, -1]]*(8-len(round.tricks))  # The tricks that have not been played
    #     tricks = played_tricks + unplayed_tricks # Combination of the played and unplayed tricks
    #     self.tricks = [item for sublist in tricks for item in sublist] # Flatten the list
    
    #     # The current score of the round
    #     self.score = round.points
       
    # def trick_transform(self, trick: Trick) -> list[int]:
    #     "Makes the trick start with the cards of Player"
    #     cards = [-1, -1, -1, -1]
    #     for i, card in enumerate(trick.cards):
    #         cards[(i+trick.starting_player+(3-self.own_position))%4] = card
    #     return cards
    
    # def card_transform(self, card: int, trump_suit: int) -> int:
    #     "Makes cards of the trump suit to have suit 0 and cards with suit 0 have suit trump_suit"
    #     suit = card_to_suit(card)
    #     if suit == trump_suit:
    #         return card_to_value(card)
    #     elif suit == 0:
    #         return trump_suit*10 + card_to_value(card)
    #     else:
    #         return card
    
    # def card_untranform(self, card: int, trump_suit: int) -> int:
    #     "Makes cards of the trump suit to have suit trump_suit and cards with suit trump_suit have suit 0"
    #     suit = card_to_suit(card)
    #     if suit == 0:
    #         return trump_suit*10 + card_to_value(card)
    #     elif suit == trump_suit:
    #         return card_to_value(card)
    #     else:
    #         return card
    
    
        # else:
        #     # print("Expand2")

            
        #     possible_hands = list(itertools.combinations(set(self.state.possible_cards[self.state.current_player]), 8-self.state.number_of_tricks))
        #     possible_hands = random.sample(possible_hands, min(10, len(possible_hands)))
        #     # print("TYPE", type(possible_hands[0]))
        #     # print("LEN", len(possible_hands))
        #     for hand in possible_hands:
        #         moves = self.state.legal_moves(hand)
        #         for card in moves:
        #             new_round = copy.deepcopy(self.state)
        #             new_card = [new_card for new_card in new_round.possible_cards[new_round.current_player] if new_card.id == card.id][0]
        #             # new_card = [new_card for new_card in new_round.legal_moves(hand) if new_card.id == card.id][0]
        #             new_round.play_card(new_card)
        #             self.children.append(Node(new_round, self, card))
        
# def main3():
#     random.seed(13)
#     starting_player = random.choice([0,1,2,3])

#     round = Round(starting_player, random.choice(['k', 'h', 'r', 's']), random.choice([0,1,2,3]))
#     new = State(round, 0)

#     for i in range(4):      
#         print("own_hand: ", new.own_hand)
#         print("possible_cards: ", new.possible_cards)
#         print("current_player: ", new.current_player)
#         print("cenre: ", new.centre)
#         if new.current_player == 0:
#             moves = new.legal_moves(new.own_hand, new.current_player)
#             moves2 = round.legal_moves()
#             if not set(moves) - set(moves2):
#                 raise Exception("moves do not match")
#         else:
#             moves = new.legal_moves(new.possible_cards[new.current_player], new.current_player)
#         print("moves: ", moves)
#         if type(moves[0]) == int:
#             raise Exception("moves are not card objects")
#         new.play_card(moves[0], new.current_player)
        

# def main2():
#     random.seed(13)
#     starting_player = random.choice([0,1,2,3])
#     print(starting_player)
#     round = Round(starting_player, random.choice(['k', 'h', 'r', 's']), random.choice([0,1,2,3]))

#     player = AlphaZero_player(starting_player)
#     move = player.get_move(round)
#     print("hallo", [card.id for card in round.legal_moves()])
#     print([card.id for card in round.player_hands[round.current_player]])
#     print(move.id)

# print("Card played: ", card)
# print("possible_cards: ", self.possible_cards)
# card_removed = False
# for i in range(4):
#     if card in self.possible_cards[i]:
#         self.possible_cards[i].remove(card)
        # card_removed = True
        
# if not card_removed:
#     raise Exception("Card not in hand")

            # for i in range(4):
            #     if len(self.other_players_cards) != 0:
            #         raise Exception("Not all cards played")                
            #     # if len(self.possible_cards[i]) != 0:
            #     #     pass
            #     #     raise Exception("Not all cards played")
            
    # main2()
    # main3()
    # innx = 1
    # tes = test(1)
    
    # list = [1,2,3,4]
    # list2 = [0,0,0,0]
    # timetime = time.time()
    # sum = 0
    # for _ in range(100):
    #     time.sleep(0.1)
    #     for _ in range(10000):
    #         # sum += innx
    #         sum += tes.id
    # print(sum)
    # print(time.time() - timetime)
    
            # temp_state = copy.deepcopy(self.state)
            # new_state = self.state
            # self.state = temp_state
            # new_card = [new_card for new_card in new_state.legal_moves() if new_card.id == card.id][0
        # for card in self.state.legal_moves():
        #     new_state = copy.deepcopy(self.state)
        #     new_state.play_card(card)
        #     self.children.add(Node(new_state, self, card))