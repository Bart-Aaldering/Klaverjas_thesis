import numpy as np
import pandas as pd



# data = pd.read_csv('code/Data/HistoryDB.csv', on_bad_lines='skip')

# # .apply(lambda x: ', '.join(x[x.notnull()]), axis = 1)


# print(data.head())

# # print(data.loc['ID'][0])
# print("HIER")
# for col in data.columns:
#     print(col)
# print(data.keys())
# print(data.columns.values)
# print(data.values)
# print(len(data.columns))
# print(data.loc[0]["ID;TableKey;TableDbID;ScoreDbID;RoundNr;Cards;Rounds;Scores;FirstPlayer;Gaat;Troef;Voorkom;TimeStamp;Settings"]) 

data = pd.read_csv("code/Data/HistoryDB.txt", sep=";",low_memory=False)
# data.to_csv("code/Data/HistoryDB.csv")
process_data = data.drop(columns=["TableKey", "TableDbID", "ScoreDbID", "TimeStamp", "Settings"])
process_data.sample(n=50000).reset_index(drop=True).to_csv("code/Data/HistoryDB2.csv")
print(data.head())