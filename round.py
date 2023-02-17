

class Round:
    def __init__(self, starting_player: int, trump_suit: int):
        self.starting_player = starting_player
        self.current_player = starting_player
        self.trump_suit = trump_suit
        self.tricks = [Trick(starting_player)]

        self.cards = [strings_to_id(value, suit) for value in values_list for suit in suits_list]

        self.points = [0, 0]
        self.meld = [0, 0]
        
            
    def deal_cards(self):
        random.shuffle(self.cards)
        self.player_hands = [self.cards[:8], self.cards[8:16], self.cards[16:24], self.cards[24:]]

    #Returns the legal moves a player could make based on the current hand and played cards
    def legal_moves(self):
        hand = self.player_hands[self.current_player]
        trick = self.tricks[-1]
        leading_suit = trick.leading_suit()

        # There has not yet been played a card, all cards may be played.
        if leading_suit is None:
            return hand

        follow = []
        trump = []
        trump_higher = []
        highest_trump_value = trick.highest_trump(self.trump_suit).order(self.trump_suit)
        for card in hand:
            if card_to_suit(card) == leading_suit:
                follow.append(card)
            if card_to_suit(card) == self.trump_suit:
                trump.append(card)
                if card_to_order(card, self.trump_suit) > highest_trump_value:
                    trump_higher.append(card)

        if follow and leading_suit != self.trump_suit:
            return follow

        return trump_higher or trump or hand   
    
    #Checks whether the round is complete
    def is_complete(self):
        return len(self.tricks) == 8 and self.tricks[-1].is_complete()

    #Plays the card in a trick
    def play_card(self, card):
        self.tricks[-1].add_card(card)
        self.player_hands[self.current_player].remove(card)
        self.current_player = self.current_player+1 % 4
        
    #Returns the player currently at turn    
    def to_play(self):
        return self.current_player
    
    #Checks whether the trick is complete and handles all variables
    def complete_trick(self):
        trick = self.tricks[-1]
        if trick.is_complete():
            winner = trick.winner(self.trump_suit)
            points = trick.points(self.trump_suit)

            meld = trick.meld(self.trump_suit)

            self.points[team(winner)] += points
            self.meld[team(winner)] += meld
        
            if len(self.tricks) == 8:
                self.points[team(winner)] += 10
                us = team(self.starting_player)
                them = other_team(self.starting_player)

                if (self.points[us] + self.meld[us] <=
                        self.points[them] + self.meld[them]):
                    self.points[them] = 162
                    self.meld[them] += self.meld[us]
                    self.points[us] = 0
                    self.meld[us] = 0
                elif self.is_pit():
                    self.meld[us] += 100
            else:
                self.tricks.append(Trick(winner))
            return True
        return False

    #Checks whether all tricks are won by one team
    def is_pit(self):
        for trick in self.tricks:
            if team(self.starting_player) != team(trick.winner(self.trump_suit)):
                return False
        return True
