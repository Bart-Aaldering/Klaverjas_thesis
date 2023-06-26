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

settings = """{
    "model_path": null,
    "mcts_params": {
        "mcts_steps": 10,
        "n_of_sims": 1,
        "nn_scaler": 0,
        "ucb_c": 200
    }
}
"""

b = """{
    "BriefNamesWe":"WO",
    "BriefNamesThey":"ZN",
    "LaatsteRoem":0,
    "PlayersTurnCompas":"Zuid",
    "StapelTroefs":{
        "Cards":[
            {
                "k":"r2",
                "e":null
            }
        ],
        "InitialCards":null
    },
    "VerzaaktAkkoord":[
        -1,
        -1,
        -1,
        -1
    ],
    "VerzaaktMelderNaam":"",
    "VerzaaktTeam":"",
    "GameMode":2,
    "MyName":"Hist3",
    "WaitingForOthers":false,
    "ClosedCardsCount":0,
    "PlayedCards":null,
    "Messages":[
        
    ],
    "MessageCounter":0,
    "OtherPlayers":[
        {
            "Name":"Hist0",
            "Compas":"West",
            "NrCards":4,
            "AI":true
        },
        {
            "Name":"Hist1",
            "Compas":"Noord",
            "NrCards":3,
            "AI":true
        },
        {
            "Name":"Hist2",
            "Compas":"Oost",
            "NrCards":3,
            "AI":true
        }
    ],
    "FirstPlayerAbsolute":1,
    "HasPlayerColor":[
        {
            "m_MaxCapacity":2147483647,
            "Capacity":16,
            "m_StringValue":"1111",
            "m_currentThread":0
        },
        {
            "m_MaxCapacity":2147483647,
            "Capacity":16,
            "m_StringValue":"1111",
            "m_currentThread":0
        },
        {
            "m_MaxCapacity":2147483647,
            "Capacity":16,
            "m_StringValue":"1001",
            "m_currentThread":0
        },
        {
            "m_MaxCapacity":2147483647,
            "Capacity":16,
            "m_StringValue":"0111",
            "m_currentThread":0
        }
    ],
    "MateSeintColorBits":[
        
    ],
    "Variant":2,
    "PlayableCardsCount":2,
    "PlayableCardBits":".11.00..",
    "ColorPlayed":{
        "k":4,
        "h":5,
        "r":4,
        "s":5
    },
    "RemainingCards":{
        "k":{
            "Cards":[
                {
                    "k":"k11",
                    "e":""
                },
                {
                    "k":"k14",
                    "e":""
                }
            ],
            "InitialCards":null
        },
        "h":{
            "Cards":[
                {
                    "k":"h13",
                    "e":""
                }
            ],
            "InitialCards":null
        },
        "r":{
            "Cards":[
                {
                    "k":"r7",
                    "e":""
                },
                {
                    "k":"r10",
                    "e":""
                },
                {
                    "k":"r11",
                    "e":""
                },
                {
                    "k":"r12",
                    "e":""
                }
            ],
            "InitialCards":null
        },
        "s":{
            "Cards":[
                {
                    "k":"s10",
                    "e":""
                },
                {
                    "k":"s13",
                    "e":""
                },
                {
                    "k":"s14",
                    "e":""
                }
            ],
            "InitialCards":null
        }
    },
    "ExpectedCard":null,
    "Round":0,
    "Extra":0,
    "MyPlayableCards":{
        "Cards":[
            {
                "k":"h8",
                "e":null
            },
            {
                "k":"h14",
                "e":null
            }
        ],
        "InitialCards":null
    },
    "Troef":"r2",
    "TroefKleur":"ruiten",
    "ScoreWe":36,
    "ScoreThey":37,
    "RoefWe":0,
    "RoefThey":0,
    "NamesWe":"Hist1 en Hist3",
    "NamesThey":"Hist0 en Hist2",
    "PlayersTurn":0,
    "HighestPlayer":-1,
    "FirstPlayer":2,
    "History":[
        {
            "First":2,
            "Highest":1,
            "Title":"1e slag",
            "Cards":[
                {
                    "Compas":"Zuid",
                    "Card":"s9",
                    "Extra":null
                },
                {
                    "Compas":"West",
                    "Card":"s11",
                    "Extra":null
                },
                {
                    "Compas":"Noord",
                    "Card":"s8",
                    "Extra":null
                },
                {
                    "Compas":"Oost",
                    "Card":"s12",
                    "Extra":null
                }
            ],
            "Count":4
        },
        {
            "First":1,
            "Highest":2,
            "Title":"2e slag",
            "Cards":[
                {
                    "Compas":"Zuid",
                    "Card":"r13",
                    "Extra":null
                },
                {
                    "Compas":"West",
                    "Card":"r14",
                    "Extra":null
                },
                {
                    "Compas":"Noord",
                    "Card":"k12",
                    "Extra":null
                },
                {
                    "Compas":"Oost",
                    "Card":"r8",
                    "Extra":null
                }
            ],
            "Count":4
        },
        {
            "First":2,
            "Highest":3,
            "Title":"3e slag",
            "Cards":[
                {
                    "Compas":"Zuid",
                    "Card":"h11",
                    "Extra":null
                },
                {
                    "Compas":"West",
                    "Card":"h10",
                    "Extra":null
                },
                {
                    "Compas":"Noord",
                    "Card":"h7",
                    "Extra":null
                },
                {
                    "Compas":"Oost",
                    "Card":"h9",
                    "Extra":null
                }
            ],
            "Count":4
        },
        {
            "First":3,
            "Highest":2,
            "Title":"4e slag",
            "Cards":[
                {
                    "Compas":"Zuid",
                    "Card":"k13",
                    "Extra":null
                },
                {
                    "Compas":"West",
                    "Card":"k8",
                    "Extra":null
                },
                {
                    "Compas":"Noord",
                    "Card":"k7",
                    "Extra":null
                },
                {
                    "Compas":"Oost",
                    "Card":"r9",
                    "Extra":null
                }
            ],
            "Count":4
        }
    ],
    "Center":[
        {
            "Compas":"Noord",
            "Card":"h12",
            "Extra":null
        },
        {
            "Compas":"Oost",
            "Card":"s7",
            "Extra":null
        }
    ],
    "CenterDeck":{
        "Cards":[
            {
                "k":"h12",
                "e":null
            },
            {
                "k":"s7",
                "e":null
            }
        ],
        "FirstPlayer":1,
        "MaxPlayers":4,
        "Count":2
    },
    "ScoreRound":{
        "Slagen":[
            0,
            0
        ],
        "We":36,
        "They":17,
        "WeRoem":0,
        "TheyRoem":20,
        "WeRoef":0,
        "TheyRoef":0,
        "WeVerzaakt":false,
        "TheyVerzaakt":false,
        "WePit":false,
        "TheyPit":false,
        "WeNat":false,
        "TheyNat":false,
        "ID":0,
        "Round":0,
        "Gaat":0,
        "Troef":null,
        "WinningPlayer":1,
        "TimeStamp":"0001-01-01T00:00:00",
        "WeDescr":"36",
        "TheyDescr":"17"
    },
    "ScoreGame":{
        "Slagen":[
            0,
            0
        ],
        "We":0,
        "They":0,
        "WeRoem":0,
        "TheyRoem":0,
        "WeRoef":0,
        "TheyRoef":0,
        "WeVerzaakt":false,
        "TheyVerzaakt":false,
        "WePit":false,
        "TheyPit":false,
        "WeNat":false,
        "TheyNat":false,
        "ID":0,
        "Round":0,
        "Gaat":0,
        "Troef":null,
        "WinningPlayer":0,
        "TimeStamp":"0001-01-01T00:00:00",
        "WeDescr":"0",
        "TheyDescr":"0"
    },
    "TeamGaat":0,
    "GaatDialog":null,
    "GaatChange":"",
    "PlayerNrGaat":2,
    "PlayerNameGaat":"Hist1",
    "VerzaaktMelder":-1,
    "TroefRegel":"Er mag direct gegaan worden op een van de vier kleuren of 1x passen.",
    "TroefSetting":3,
    "Ronde":1,
    "AutoSort":false,
    "AllAIPlayers":true,
    "NoAIPlayers":false,
    "Celebrate":{
        "Title":"",
        "MessageHTML":"",
        "Extra":"",
        "Positive":true,
        "ShowAnimation":true
    },
    "VoorkomVerzaakt":2,
    "MayUndo":true,
    "Faster":false,
    "MayHistory":true,
    "HideScores":false,
    "AllAskCards":true,
    "AutoMoveChair":false,
    "HideCards":false,
    "ShowDealerIcon":false,
    "DealerNr":2,
    "GaatInfoDialog":null,
    "MyNr":3,
    "MyAI":true,
    "MyColumnCount":0,
    "MyDeck":{
        "Cards":[
            {
                "k":".",
                "e":null
            },
            {
                "k":"h8",
                "e":null
            },
            {
                "k":"h14",
                "e":null
            },
            {
                "k":".",
                "e":null
            },
            {
                "k":"k9",
                "e":null
            },
            {
                "k":"k10",
                "e":null
            },
            {
                "k":".",
                "e":null
            },
            {
                "k":".",
                "e":null
            }
        ],
        "InitialCards":null
    },
    "MyCards":". h8 h14 . k9 k10 . .",
    "WaitingFor":"",
    "WaitingPresent":"",
    "Dialogs":[
        {
            "Key":"TakeOverFromAI",
            "Title":"Je kijkt mee ...",
            "Text":"Dit is een computer speler. Wil jij aanschuiven en 't overnemen?",
            "Error":null,
            "Input":null,
            "ShowInput":false,
            "CanClose":false,
            "CloseAction":null,
            "Buttons":[
                {
                    "Text":"Aanschuiven",
                    "Color":null,
                    "Action":"TurnOffAI",
                    "ActionType":0,
                    "SendInput":false,
                    "ActionParameter":null,
                    "ActionIntParameter":0
                }
            ]
        },
        {
            "Key":"TakeOverFromAI",
            "Title":"Je kijkt mee ...",
            "Text":"Dit is een computer speler. Wil jij aanschuiven en 't overnemen?",
            "Error":null,
            "Input":null,
            "ShowInput":false,
            "CanClose":false,
            "CloseAction":null,
            "Buttons":[
                {
                    "Text":"Aanschuiven",
                    "Color":null,
                    "Action":"TurnOffAI",
                    "ActionType":0,
                    "SendInput":false,
                    "ActionParameter":null,
                    "ActionIntParameter":0
                }
            ]
        }
    ],
    "MayAskNewCards":false
}"""
c = """{
    "BriefNamesWe":"WO",
    "BriefNamesThey":"ZN",
    "LaatsteRoem":0,
    "PlayersTurnCompas":"Zuid",
    "StapelTroefs":{
        "Cards":[
            {
                "k":"r2",
                "e":null
            }
        ],
        "InitialCards":null
    },
    "VerzaaktAkkoord":[
        -1,
        -1,
        -1,
        -1
    ],
    "VerzaaktMelderNaam":"",
    "VerzaaktTeam":"",
    "GameMode":2,
    "MyName":"Hist3",
    "WaitingForOthers":false,
    "ClosedCardsCount":0,
    "PlayedCards":null,
    "Messages":[
        
    ],
    "MessageCounter":0,
    "OtherPlayers":[
        {
            "Name":"Hist0",
            "Compas":"West",
            "NrCards":2,
            "AI":true
        },
        {
            "Name":"Hist1",
            "Compas":"Noord",
            "NrCards":2,
            "AI":true
        },
        {
            "Name":"Hist2",
            "Compas":"Oost",
            "NrCards":2,
            "AI":true
        }
    ],
    "FirstPlayerAbsolute":3,
    "HasPlayerColor":[
        {
            "m_MaxCapacity":2147483647,
            "Capacity":16,
            "m_StringValue":"1111",
            "m_currentThread":0
        },
        {
            "m_MaxCapacity":2147483647,
            "Capacity":16,
            "m_StringValue":"0011",
            "m_currentThread":0
        },
        {
            "m_MaxCapacity":2147483647,
            "Capacity":16,
            "m_StringValue":"1011",
            "m_currentThread":0
        },
        {
            "m_MaxCapacity":2147483647,
            "Capacity":16,
            "m_StringValue":"0011",
            "m_currentThread":0
        }
    ],
    "MateSeintColorBits":[
        
    ],
    "Variant":2,
    "PlayableCardsCount":2,
    "PlayableCardBits":"..1....1",
    "ColorPlayed":{
        "k":6,
        "h":7,
        "r":7,
        "s":4
    },
    "RemainingCards":{
        "k":{
            "Cards":[
                {
                    "k":"k9",
                    "e":""
                },
                {
                    "k":"k13",
                    "e":""
                }
            ],
            "InitialCards":null
        },
        "h":{
            "Cards":[
                
            ],
            "InitialCards":null
        },
        "r":{
            "Cards":[
                {
                    "k":"r13",
                    "e":""
                }
            ],
            "InitialCards":null
        },
        "s":{
            "Cards":[
                {
                    "k":"s7",
                    "e":""
                },
                {
                    "k":"s8",
                    "e":""
                },
                {
                    "k":"s13",
                    "e":""
                }
            ],
            "InitialCards":null
        }
    },
    "ExpectedCard":null,
    "Round":0,
    "Extra":0,
    "MyPlayableCards":{
        "Cards":[
            {
                "k":"h14",
                "e":null
            },
            {
                "k":"s10",
                "e":null
            }
        ],
        "InitialCards":null
    },
    "Troef":"r2",
    "TroefKleur":"ruiten",
    "ScoreWe":144,
    "ScoreThey":25,
    "RoefWe":0,
    "RoefThey":0,
    "NamesWe":"Hist1 en Hist3",
    "NamesThey":"Hist0 en Hist2",
    "PlayersTurn":0,
    "HighestPlayer":0,
    "FirstPlayer":0,
    "History":[
        {
            "First":0,
            "Highest":2,
            "Title":"1e slag",
            "Cards":[
                {
                    "Compas":"Zuid",
                    "Card":"s11",
                    "Extra":null
                },
                {
                    "Compas":"West",
                    "Card":"s9",
                    "Extra":null
                },
                {
                    "Compas":"Noord",
                    "Card":"s14",
                    "Extra":null
                },
                {
                    "Compas":"Oost",
                    "Card":"s12",
                    "Extra":null
                }
            ],
            "Count":4
        },
        {
            "First":2,
            "Highest":1,
            "Title":"2e slag",
            "Cards":[
                {
                    "Compas":"Zuid",
                    "Card":"h9",
                    "Extra":null
                },
                {
                    "Compas":"West",
                    "Card":"h11",
                    "Extra":null
                },
                {
                    "Compas":"Noord",
                    "Card":"h8",
                    "Extra":null
                },
                {
                    "Compas":"Oost",
                    "Card":"r7",
                    "Extra":null
                }
            ],
            "Count":4
        },
        {
            "First":1,
            "Highest":1,
            "Title":"3e slag",
            "Cards":[
                {
                    "Compas":"Zuid",
                    "Card":"k12",
                    "Extra":null
                },
                {
                    "Compas":"West",
                    "Card":"k8",
                    "Extra":null
                },
                {
                    "Compas":"Noord",
                    "Card":"k7",
                    "Extra":null
                },
                {
                    "Compas":"Oost",
                    "Card":"k11",
                    "Extra":null
                }
            ],
            "Count":4
        },
        {
            "First":1,
            "Highest":0,
            "Title":"4e slag",
            "Cards":[
                {
                    "Compas":"Zuid",
                    "Card":"r10",
                    "Extra":null
                },
                {
                    "Compas":"West",
                    "Card":"r9",
                    "Extra":null
                },
                {
                    "Compas":"Noord",
                    "Card":"r12",
                    "Extra":null
                },
                {
                    "Compas":"Oost",
                    "Card":"r11",
                    "Extra":null
                }
            ],
            "Count":4
        },
        {
            "First":0,
            "Highest":1,
            "Title":"5e slag",
            "Cards":[
                {
                    "Compas":"Zuid",
                    "Card":"h7",
                    "Extra":null
                },
                {
                    "Compas":"West",
                    "Card":"r14",
                    "Extra":null
                },
                {
                    "Compas":"Noord",
                    "Card":"h13",
                    "Extra":null
                },
                {
                    "Compas":"Oost",
                    "Card":"h12",
                    "Extra":null
                }
            ],
            "Count":4
        },
        {
            "First":1,
            "Highest":0,
            "Title":"6e slag",
            "Cards":[
                {
                    "Compas":"Zuid",
                    "Card":"k10",
                    "Extra":null
                },
                {
                    "Compas":"West",
                    "Card":"h10",
                    "Extra":null
                },
                {
                    "Compas":"Noord",
                    "Card":"k14",
                    "Extra":null
                },
                {
                    "Compas":"Oost",
                    "Card":"r8",
                    "Extra":null
                }
            ],
            "Count":4
        }
    ],
    "Center":[
        
    ],
    "CenterDeck":{
        "Cards":[
            
        ],
        "FirstPlayer":-1,
        "MaxPlayers":4,
        "Count":0
    },
    "TeamGaat":0,
    "GaatDialog":null,
    "GaatChange":"",
    "PlayerNrGaat":0,
    "PlayerNameGaat":"Jij",
    "VerzaaktMelder":-1,
    "TroefRegel":"Er mag direct gegaan worden op een van de vier kleuren of 1x passen.",
    "TroefSetting":3,
    "Ronde":1,
    "AutoSort":false,
    "AllAIPlayers":true,
    "NoAIPlayers":false,
    "Celebrate":{
        "Title":"",
        "MessageHTML":"",
        "Extra":"",
        "Positive":true,
        "ShowAnimation":true
    },
    "VoorkomVerzaakt":2,
    "MayUndo":true,
    "Faster":false,
    "MayHistory":true,
    "HideScores":false,
    "AllAskCards":true,
    "AutoMoveChair":false,
    "HideCards":false,
    "ShowDealerIcon":false,
    "DealerNr":2,
    "GaatInfoDialog":null,
    "MyNr":3,
    "MyAI":true,
    "MyColumnCount":0,
    "MyDeck":{
        "Cards":[
            {
                "k":".",
                "e":null
            },
            {
                "k":".",
                "e":null
            },
            {
                "k":"h14",
                "e":null
            },
            {
                "k":".",
                "e":null
            },
            {
                "k":".",
                "e":null
            },
            {
                "k":".",
                "e":null
            },
            {
                "k":".",
                "e":null
            },
            {
                "k":"s10",
                "e":null
            }
        ],
        "InitialCards":null
    },
    "MyCards":". . h14 . . . . s10",
    "MayAskNewCards":false
}"""
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
            # for index in range(4):
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


def main(json_state, alpha_player_settings):
    global model

    # # load the data string from the command line in as a json object
    # json_state = json.loads(sys.argv[1])
    # alpha_player_settings = json.loads(sys.argv[2])

    ## Can be used for testing:
    json_state = json.loads(json_state)
    alpha_player_settings = json.loads(alpha_player_settings)

    mcts_params = alpha_player_settings["mcts_params"]

    ### Only needed if a model will be used:
    # model_path = alpha_player_settings["model_path"]
    # if model_path is not None and model is None:
    # model = tf.keras.models.load_model(model_path)

    alphazero_player = AlphaZero_player(0, mcts_params, model)
    hand, starting_player, declaring_team, played_cards = process_klaverlive_json(json_state)
    print(hand, starting_player, declaring_team, played_cards)
    alphazero_player.new_round_klaverlive(hand, starting_player, declaring_team)

    for card in played_cards:
        alphazero_player.update_state(Card(card))

    move = alphazero_player.get_move()[0].id
    return alpha_card_to_klaverlive_card(move, json_state["TroefKleur"])


if __name__ == "__main__":
    move = main(b, settings)
    print(move)
