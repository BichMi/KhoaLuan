import json
import pandas as pd

list_question = []
list_answer = []
with open('data_full1.json', encoding='utf-8') as data_file:
    data = json.loads(data_file.read())
    for i in data:
        for key, value in i.items():
            print(key[2], ":", value)

# file = 'data_full1.json'
# dl = pd.read_json(file)
#
# data = dl.head()
# # print(data.columns)
# print(repr(data))