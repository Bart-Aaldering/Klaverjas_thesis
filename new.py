import numpy as np
import random
import pandas as pd


from helper import *
from round import Round





class rule_based_player:
    #Returns the card for the rule-based player
    def get_card_good_player(self, round: Round):
        trick = round.tricks[-1]
        trump = round.trump_suit
        legal_moves = round.legal_moves()
        cant_follow = 0
        if len(trick.cards) == 0:
            for card in legal_moves:
                if card_to_value(card) == round.get_highest_card(card.suit):
                    return card
            return self.get_lowest_card(legal_moves, trump)

        if legal_moves[0].suit == trick.cards[0].suit:
            cant_follow = 1
            
        if len(trick.cards) == 1:
            for card in legal_moves:
                if card_to_value(card) == round.get_highest_card(trick.cards[0].suit):
                    return card
            return self.get_lowest_card(legal_moves, trump)
                

        if len(trick.cards) == 2:
            if cant_follow:
                return self.get_lowest_card(legal_moves, trump)

            if trick.cards[0].value == round.get_highest_card(trick.cards[0].suit):
                return self.get_highest_card(legal_moves, trump)


            for card in legal_moves:
                if card_to_value(card) == round.get_highest_card(trick.cards[0].suit):
                    return card

            return self.get_lowest_card(legal_moves, trump)

        else:
            
            if trick.winner(trump) %2 == 1:
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


def main():
    points = [0, 0]
    meld = [0, 0]
    import time 
    start = time.time()
    player = rule_based_player()
    for i in range(10000):
        round = Round(i % 4, 'k')
        round.deal_cards()

        # print_hands(round.player_hands)



        for _ in range(8):
            for _ in range(2):


                legal_moves = round.legal_moves()
                round.play_card(random.choice(legal_moves))
                
                choice = player.get_card_good_player(round, round.to_play())
                round.play_card(choice)


                
            # print("ROUND COMPLETE")
            if not round.complete_trick():
                print("ERROR")

        points[0] += round.points[0]
        points[1] += round.points[1]
        meld[0] += round.meld[0]
        meld[1] += round.meld[1]
    end = time.time()
    print("Time: ", end - start)
    print("Points: ", points)
    print("Meld: ", meld)

if __name__ == "__main__":
    main()