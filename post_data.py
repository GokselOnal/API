import pandas as pd
import requests
import json

def post_data():
    df = pd.read_csv("data/League of Legends Champion Stats 12.12.csv", sep=";")

    for index, row in df.iterrows():
        body = '{"name": ' + '"' + row.Name + '"' + ', "class": ' + '"' + row.Class + '"' + ', "role": ' + '"' + row.Role + '"' + ', "win%": ' + '"' + \
               row["Win %"] + '"' + ', "pick%": ' + '"' + row["Pick %"] + '"' + ', "ban%": ' + '"' + row["Ban %"] + '"' + '}'
        requests.post("http://127.0.0.1:5000/api/champions", json.loads(body))

if __name__ == "__main__":
    post_data()