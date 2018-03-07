# -*- coding: utf-8 -*-
import json
import pandas as pd

list_question = []
list_answer = []
list_date = []
with open('data.json', encoding='utf-8') as data_file:
    data = json.loads(data_file.read())
    for i in data:
        print(i.get("questions"))
        list_question.append(i.get("questions"))
        list_answer.append(i.get("answers"))
        list_date.append(i.get("dates"))
    print(len(data))
    print(len(list_question))
    for j in list_question:
        print(j)
    print(len(list_answer))
    for j in list_answer:
        print(j)
    print(len(list_date))
    for j in list_date:
        print(j)
