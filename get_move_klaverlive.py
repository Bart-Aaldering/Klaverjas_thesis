import sys
import json
import os
import tensorflow as tf

from AlphaZero.AlphaZeroPlayer.alphazero_player import AlphaZero_player

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU

string_state = """{"BriefNamesWe":"Z&amp;N","BriefNamesThey":"W&amp;O","LaatsteRoem":0,"PlayersTurnCompas":"Zuid","History":[{"First":2,"Highest":-1,"Title":"5e slag","Cards":[{"Compas":"Zuid","Card":"h12","Extra":null},{"Compas":"West","Card":"h11","Extra":null},{"Compas":"Noord","Card":"s10","Extra":null},{"Compas":"Oost","Card":"h13","Extra":null}],"Count":4}],"StapelTroefs":{"Cards":[{"k":"s2","e":null}],"InitialCards":null},"VerzaaktAkkoord":[-1,-1,-1,-1],"VerzaaktMelderNaam":"","VerzaaktTeam":"","GameMode":2,"MyName":"Zuid","WaitingForOthers":false,"ClosedCardsCount":0,"PlayedCards":null,"Messages":[],"MessageCounter":0,"OtherPlayers":[{"Name":"West","Compas":"West","NrCards":3,"AI":true},{"Name":"Noord","Compas":"Noord","NrCards":2,"AI":true},{"Name":"Oost","Compas":"Oost","NrCards":2,"AI":true}],"Troef":"s2","TroefKleur":"schoppen","ScoreWe":101,"ScoreThey":84,"RoefWe":0,"RoefThey":0,"NamesWe":"Zuid en Noord","NamesThey":"West en Oost","PlayersTurn":0,"HighestPlayer":-1,"Center":[{"Compas":"Noord","Card":"k10","Extra":null},{"Compas":"Oost","Card":"k9","Extra":null}],"CenterDeck":{"Cards":[{"k":"k10","e":null},{"k":"k9","e":null}],"FirstPlayer":2,"MaxPlayers":4,"Count":2},"ScoreRound":{"Slagen":[0,0],"We":61,"They":44,"WeRoem":40,"TheyRoem":40,"WeRoef":0,"TheyRoef":0,"WeVerzaakt":false,"TheyVerzaakt":false,"WePit":false,"TheyPit":false,"WeNat":false,"TheyNat":false,"ID":0,"Round":0,"Gaat":0,"Troef":null,"WinningPlayer":2,"TimeStamp":"0001-01-01T00:00:00","WeDescr":"61","TheyDescr":"44"},"ScoreGame":{"Slagen":[0,0],"We":0,"They":0,"WeRoem":0,"TheyRoem":0,"WeRoef":0,"TheyRoef":0,"WeVerzaakt":false,"TheyVerzaakt":false,"WePit":false,"TheyPit":false,"WeNat":false,"TheyNat":false,"ID":0,"Round":0,"Gaat":0,"Troef":null,"WinningPlayer":0,"TimeStamp":"0001-01-01T00:00:00","WeDescr":"0","TheyDescr":"0"},"TeamGaat":0,"GaatDialog":null,"GaatChange":"","PlayerNrGaat":0,"PlayerNameGaat":"Jij","VerzaaktMelder":-1,"TroefRegel":"Er mag direct gegaan worden op een van de vier kleuren of 1x passen.","TroefSetting":3,"Ronde":1,"AutoSort":false,"AllAIPlayers":false,"NoAIPlayers":false,"Celebrate":{"Title":"","MessageHTML":"","Extra":"","Positive":true,"ShowAnimation":true},"VoorkomVerzaakt":1,"MayUndo":true,"Faster":false,"MayHistory":true,"HideScores":false,"AllAskCards":true,"AutoMoveChair":false,"HideCards":false,"ShowDealerIcon":false,"DealerNr":0,"GaatInfoDialog":null,"MyNr":0,"MyAI":false,"MyColumnCount":0,"MyDeck":{"Cards":[{"k":"h7","e":null},{"k":".","e":null},{"k":".","e":null},{"k":".","e":null},{"k":"k8","e":null},{"k":".","e":null},{"k":".","e":null},{"k":"s9","e":null}],"InitialCards":null},"MyCards":"h7 . . . k8 . . s9","WaitingFor":"","WaitingPresent":"","Dialogs":[],"MayAskNewCards":false}"""

# a1 = {
#     "BriefNamesWe":"Z&amp;N",
#     "BriefNamesThey":"W&amp;O",
#     "LaatsteRoem":20,
#     "PlayersTurnCompas":"Zuid",
#     "History":
#     [
#         {
#             "First":-1,
#             "Highest":-1,
#             "Title":"4e slag",
#             "Cards":[
#                 {
#                     "Compas":"Zuid",
#                     "Card":"h14",
#                     "Extra":null
#                 },
#                 {
#                     "Compas":"West",
#                     "Card":"h8",
#                     "Extra":null
#                 },
#                 {"Compas":"Noord",
#                  "Card":"h10",
#                  "Extra":null
#                 },
#                 {"Compas":"Oost",
#                  "Card":"h9",
#                  "Extra":null
#                 }
#             ],
#             "Count":4
#         }
#     ],
#     "StapelTroefs":
#     {
#         "Cards":
#         [
#             {
#                 "k":"s2","e":null
#             }
#         ],
#         "InitialCards":null
#     },
#     "VerzaaktAkkoord":[-1,-1,-1,-1],
#     "VerzaaktMelderNaam":"",
#     "VerzaaktTeam":"",
#     "GameMode":2,
#     "MyName":"Zuid",
#     "WaitingForOthers":false,
#     "ClosedCardsCount":0,
#     "PlayedCards":null,
#     "Messages":[],
#     "MessageCounter":0,
#     "OtherPlayers":
#     [
#         {
#             "Name":"West",
#             "Compas":"West",
#             "NrCards":4,
#             "AI":true
#          },
#         {
#             "Name":"Noord",
#             "Compas":"Noord",
#             "NrCards":4,
#             "AI":true
#         },
#         {
#             "Name":"Oost",
#             "Compas":"Oost",
#             "NrCards":4,
#             "AI":true
#         }
#     ],
#     "Troef":"s2",
#     "TroefKleur":"schoppen",
#     "ScoreWe":62,
#     "ScoreThey":84,
#     "RoefWe":0,
#     "RoefThey":0,
#     "NamesWe":"Zuid en Noord",
#     "NamesThey":"West en Oost",
#     "PlayersTurn":0,
#     "HighestPlayer":0,
#     "Center":[],
#     "CenterDeck":
#     {
#         "Cards":[],
#         "FirstPlayer":-1,
#         "MaxPlayers":4,
#         "Count":0
#     },
#     "ScoreRound":
#     {
#         "Slagen":[0,0],
#         "We":42,
#         "They":44,
#         "WeRoem":20,
#         "TheyRoem":40,
#         "WeRoef":0,
#         "TheyRoef":0,
#         "WeVerzaakt":false,
#         "TheyVerzaakt":false,
#         "WePit":false,
#         "TheyPit":false,
#         "WeNat":false,
#         "TheyNat":false,
#         "ID":0,
#         "Round":0,
#         "Gaat":0,
#         "Troef":null,
#         "WinningPlayer":0,
#         "TimeStamp":"0001-01-01T00:00:00",
#         "WeDescr":"42",
#         "TheyDescr":"44"
#     },
#     "ScoreGame":
#     {
#         "Slagen":[0,0],
#         "We":0,
#         "They":0,
#         "WeRoem":0,
#         "TheyRoem":0,
#         "WeRoef":0,
#         "TheyRoef":0,
#         "WeVerzaakt":false,
#         "TheyVerzaakt":false,
#         "WePit":false,
#         "TheyPit":false,
#         "WeNat":false,
#         "TheyNat":false,
#         "ID":0,
#         "Round":0,
#         "Gaat":0,
#         "Troef":null,
#         "WinningPlayer":0,
#         "TimeStamp":"0001-01-01T00:00:00",
#         "WeDescr":"0",
#         "TheyDescr":"0"
#     },
#     "TeamGaat":0,
#     "GaatDialog":null,
#     "GaatChange":"",
#     "PlayerNrGaat":0,
#     "PlayerNameGaat":"Jij",
#     "VerzaaktMelder":-1,
#     "TroefRegel":"Er mag directgegaan worden op een van de vier kleuren of 1x passen.",
#     "TroefSetting":3,
#     "Ronde":1,
#     "AutoSort":false,
#     "AllAIPlayers":false,
#     "NoAIPlayers":false,
#     "Celebrate":
#     {
#         "Title":"",
#         "MessageHTML":"",
#         "Extra":"",
#         "Positive":true,
#         "ShowAnimation":true
#     },
#     "VoorkomVerzaakt":1,
#     "MayUndo":true,
#     "Faster":false,
#     "MayHistory":true,
#     "HideScores":false,
#     "AllAskCards":true,
#     "AutoMoveChair":false,
#     "HideCards":false,
#     "ShowDealerIcon":false,
#     "DealerNr":0,
#     "GaatInfoDialog":null,
#     "MyNr":0,
#     "MyAI":false,
#     "MyColumnCount":0,
#     "MyDeck":
#     {
#         "Cards":
#         [
#             {
#                 "k":"h7",
#                 "e":null
#             },
#             {
#                 "k":"h12",
#                 "e":null
#             },
#             {
#                 "k":".",
#                 "e":null},
#             {
#                 "k":".",
#                 "e":null
#             },
#             {
#                 "k":"k8",
#                 "e":null
#             },
#             {
#                 "k":".",
#                 "e":null
#             },
#             {
#                 "k":".",
#                 "e":null
#             },
#             {
#                 "k":"s9",
#                 "e":null
#             }
#         ],
#         "InitialCards":null
#     },
#     "MyCards":"h7 h12 . . k8 . . s9",
#     "WaitingFor":"",
#     "WaitingPresent":"",
#     "Dialogs":[],
#     "MayAskNewCards":false
# }

# a2 = {
#     "BriefNamesWe":"Z&amp;N",
#     "BriefNamesThey":"W&amp;O",
#     "LaatsteRoem":0,
#     "PlayersTurnCompas":"Zuid",
#     "History":[
#         {
#             "First":-1,
#             "Highest":-1,
#             "Title":"5e slag",
#             "Cards":[
#                 {
#                     "Compas":"Zuid",
#                     "Card":"h12",
#                     "Extra":null
#                 },
#                 {
#                     "Compas":"West",
#                     "Card":"h11",
#                     "Extra":null
#                 },
#                 {
#                     "Compas":"Noord",
#                     "Card":"s10",
#                     "Extra":null
#                 },
#                 {
#                     "Compas":"Oost",
#                     "Card":"h13",
#                     "Extra":null
#                 }
#             ],
#             "Count":4
#         }
#     ],
#     "StapelTroefs":{
#         "Cards":[
#             {
#                 "k":"s2",
#                 "e":null
#             }
#         ],
#         "InitialCards":null
#     },
#     "VerzaaktAkkoord":[
#         -1,
#         -1,
#         -1,
#         -1
#     ],
#     "VerzaaktMelderNaam":"",
#     "VerzaaktTeam":"",
#     "GameMode":2,
#     "MyName":"Zuid",
#     "WaitingForOthers":false,
#     "ClosedCardsCount":0,
#     "PlayedCards":null,
#     "Messages":[

#     ],
#     "MessageCounter":0,
#     "OtherPlayers":[
#         {
#             "Name":"West",
#             "Compas":"West",
#             "NrCards":3,
#             "AI":true
#         },
#         {
#             "Name":"Noord",
#             "Compas":"Noord",
#             "NrCards":2,
#             "AI":true
#         },
#         {
#             "Name":"Oost",
#             "Compas":"Oost",
#             "NrCards":2,
#             "AI":true
#         }
#     ],
#     "Troef":"s2",
#     "TroefKleur":"schoppen",
#     "ScoreWe":101,
#     "ScoreThey":84,
#     "RoefWe":0,
#     "RoefThey":0,
#     "NamesWe":"Zuid en Noord",
#     "NamesThey":"West en Oost",
#     "PlayersTurn":0,
#     "HighestPlayer":-1,
#     "Center":[
#         {
#             "Compas":"Noord",
#             "Card":"k10",
#             "Extra":null
#         },
#         {
#             "Compas":"Oost",
#             "Card":"k9",
#             "Extra":null
#         }
#     ],
#     "CenterDeck":{
#         "Cards":[
#             {
#                 "k":"k10",
#                 "e":null
#             },
#             {
#                 "k":"k9",
#                 "e":null
#             }
#         ],
#         "FirstPlayer":2,
#         "MaxPlayers":4,
#         "Count":2
#     },
#     "ScoreRound":{
#         "Slagen":[
#             0,
#             0
#         ],
#         "We":61,
#         "They":44,
#         "WeRoem":40,
#         "TheyRoem":40,
#         "WeRoef":0,
#         "TheyRoef":0,
#         "WeVerzaakt":false,
#         "TheyVerzaakt":false,
#         "WePit":false,
#         "TheyPit":false,
#         "WeNat":false,
#         "TheyNat":false,
#         "ID":0,
#         "Round":0,
#         "Gaat":0,
#         "Troef":null,
#         "WinningPlayer":2,
#         "TimeStamp":"0001-01-01T00:00:00",
#         "WeDescr":"61",
#         "TheyDescr":"44"
#     },
#     "ScoreGame":{
#         "Slagen":[
#             0,
#             0
#         ],
#         "We":0,
#         "They":0,
#         "WeRoem":0,
#         "TheyRoem":0,
#         "WeRoef":0,
#         "TheyRoef":0,
#         "WeVerzaakt":false,
#         "TheyVerzaakt":false,
#         "WePit":false,
#         "TheyPit":false,
#         "WeNat":false,
#         "TheyNat":false,
#         "ID":0,
#         "Round":0,
#         "Gaat":0,
#         "Troef":null,
#         "WinningPlayer":0,
#         "TimeStamp":"0001-01-01T00:00:00",
#         "WeDescr":"0",
#         "TheyDescr":"0"
#     },
#     "TeamGaat":0,
#     "GaatDialog":null,
#     "GaatChange":"",
#     "PlayerNrGaat":0,
#     "PlayerNameGaat":"Jij",
#     "VerzaaktMelder":-1,
#     "TroefRegel":"Er mag direct gegaan worden op een van de vier kleuren of 1x passen.",
#     "TroefSetting":3,
#     "Ronde":1,
#     "AutoSort":false,
#     "AllAIPlayers":false,
#     "NoAIPlayers":false,
#     "Celebrate":{
#         "Title":"",
#         "MessageHTML":"",
#         "Extra":"",
#         "Positive":true,
#         "ShowAnimation":true
#     },
#     "VoorkomVerzaakt":1,
#     "MayUndo":true,
#     "Faster":false,
#     "MayHistory":true,
#     "HideScores":false,
#     "AllAskCards":true,
#     "AutoMoveChair":false,
#     "HideCards":false,
#     "ShowDealerIcon":false,
#     "DealerNr":0,
#     "GaatInfoDialog":null,
#     "MyNr":0,
#     "MyAI":false,
#     "MyColumnCount":0,
#     "MyDeck":{
#         "Cards":[
#             {
#                 "k":"h7",
#                 "e":null
#             },
#             {
#                 "k":".",
#                 "e":null
#             },
#             {
#                 "k":".",
#                 "e":null
#             },
#             {
#                 "k":".",
#                 "e":null
#             },
#             {
#                 "k":"k8",
#                 "e":null
#             },
#             {
#                 "k":".",
#                 "e":null
#             },
#             {
#                 "k":".",
#                 "e":null
#             },
#             {
#                 "k":"s9",
#                 "e":null
#             }
#         ],
#         "InitialCards":null
#     },
#     "MyCards":"h7 . . . k8 . . s9",
#     "WaitingFor":"",
#     "WaitingPresent":"",
#     "Dialogs":[

#     ],
#     "MayAskNewCards":false
# }

settings = """{
    "model_path": null,
    "mcts_params": {
        "mcts_steps": 10,
        "n_of_sims": 0,
        "nn_scaler": 1,
        "ucb_c": 50
    }
}
"""

model = None


def process_klaverlive_json(json_state):

    hand = set(json_state["MyCards"].split(" ")) - {"."}
    played_cards = []
    for trick in json_state["History"]:
        for card in trick["Cards"]:
            if card["Compas"] == json_state["MyName"]:
                hand.add(card["Card"])

    played_cards = set(json_state["CenterDeck"]["Cards"]) - {"."}

    player_information = {
        "hand_current_player": json_state["MyCards"],
        "current_player": json_state["PlayersTurn"],
        "trump_suit": json_state["TroefKleur"],
        "declaring_team": json_state["TeamGaat"],
    }

    return player_information, played_cards


def main(json_state, alpha_player_settings):
    global model
    player_information = process_klaverlive_json(json_state)

    model_path = alpha_player_settings["model_path"]
    mcts_params = alpha_player_settings["mcts_params"]

    if model_path is not None and model is None:
        model = tf.keras.models.load_model(model_path)

    AlphaZero_player(0, mcts_params, model)
    AlphaZero_player.new_round_klaverlive(player_information)

    # for card in played_cards:
    #     AlphaZero_player


if __name__ == "__main__":
    # load the data string from the command line in as a json object
    json_state = json.loads(sys.argv[1])
    alpha_player_settings = json.loads(sys.argv[2])

    # json_state = json.loads(string_state)
    # alpha_player_settings = json.loads(settings)

    main(json_state, alpha_player_settings)
