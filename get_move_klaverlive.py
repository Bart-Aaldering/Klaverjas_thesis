import sys
import json

from AlphaZero.AlphaZeroPlayer.alphazero_player import AlphaZero_player
from AlphaZero.AlphaZeroPlayer.Klaverjas.card import Card
from AlphaZero.AlphaZeroPlayer.Klaverjas.helper import card_transform, card_untransform

### Only needed if a model will be used:
# import tensorflow as tf
# import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU


# test = """{
#     "History": [
#         {
#             "Cards":[
#                 {
#                     "Compas":"Zuid",
#                     "Card":"h10"
#                 },
#                 {
#                     "Compas":"West",
#                     "Card":"h12"
#                 },
#                 {
#                     "Compas":"Noord",
#                     "Card":"k10"
#                 },
#                 {
#                     "Compas":"Oost",
#                     "Card":"h13"
#                 }
#             ],
#             "First": 1
#         }
#     ],
#     "TroefKleur":"schoppen",
#     "Center":[
#     ],
#     "TeamGaat":0,
#     "MyCards":"h7 r7 . k9 k8 s7 r10 s9"
# }"""

# settings = """{
#     "model_path": null,
#     "mcts_params": {
#         "mcts_steps": 10,
#         "n_of_sims": 1,
#         "nn_scaler": 0,
#         "ucb_c": 200
#     }
# }
# """

model = None


def klaverlive_card_to_alpha_card(card, troefkleur):
    card_id = ["k", "h", "r", "s"].index(card[:1]) * 10 + int(card[1:]) - 7
    return card_transform(card_id, ["k", "h", "r", "s"].index(troefkleur[0].lower()))


def alpha_card_to_klaverlive_card(card_id, troefkleur):
    card_id = card_untransform(card_id, ["k", "h", "r", "s"].index(troefkleur[0].lower()))
    return ["k", "h", "r", "s"][card_id // 10] + str(card_id % 10 + 7)


def process_klaverlive_json(json_state):
    # loads cards stil in hand and transforms them to the alphaZero card format
    hand = {
        klaverlive_card_to_alpha_card(card, json_state["TroefKleur"])
        for card in set(json_state["MyCards"].split(" ")) - {"."}
    }

    played_cards = []
    for trick in json_state["History"]:
        for index in range(trick["First"], trick["First"] + 4):
            index = index % 4
            card = trick["Cards"][index]
            card_tranformed = klaverlive_card_to_alpha_card(card["Card"], json_state["TroefKleur"])
            if card["Compas"] == "Zuid":
                hand.add(card_tranformed)
            played_cards.append(card_tranformed)

    for card in json_state["Center"]:
        card_tranformed = klaverlive_card_to_alpha_card(card["Card"], json_state["TroefKleur"])

        if card["Compas"] == "Zuid":
            hand.add(card_tranformed)
        played_cards.append(card_tranformed)

    starting_player = json_state["History"][0]["First"]
    declaring_team = 1 - json_state["TeamGaat"]

    return hand, starting_player, declaring_team, played_cards


def main():
    global model

    # load the data string from the command line in as a json object
    json_state = json.loads(sys.argv[1])
    alpha_player_settings = json.loads(sys.argv[2])

    ### Can be used for testing:
    # json_state = json.loads(test)
    # alpha_player_settings = json.loads(settings)

    mcts_params = alpha_player_settings["mcts_params"]

    ### Only needed if a model will be used:
    # model_path = alpha_player_settings["model_path"]
    # if model_path is not None and model is None:
    # model = tf.keras.models.load_model(model_path)

    alphazero_player = AlphaZero_player(0, mcts_params, model)
    hand, starting_player, declaring_team, played_cards = process_klaverlive_json(json_state)
    alphazero_player.new_round_klaverlive(hand, starting_player, declaring_team)

    for card in played_cards:
        alphazero_player.update_state(Card(card))

    move = alphazero_player.get_move()[0].id
    return alpha_card_to_klaverlive_card(move, json_state["TroefKleur"])


if __name__ == "__main__":
    move = main()
    print(move)
