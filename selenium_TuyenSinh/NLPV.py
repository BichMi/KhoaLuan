# -*- coding: utf-8 -*-
import json
import io
import underthesea as uts
from pymongo import MongoClient

class DataExport:
    def __init__(self, q, a, d):
        self.question = q
        self.answer = a
        self.date = d

    def get_data(self):

        with open('data.json', encoding='utf-8') as data_file:
            data = json.loads(data_file.read())
            for i in data:
                self.question.append(i.get("questions"))
                self.answer.append(i.get("answers"))
                self.date.append(i.get("dates"))

            return self

    def segmentation(self):
        for i in range(len(self.question)):
            result_question = uts.word_sent(self.question[i], format='text')
            self.question[i] = result_question
        for j in range(len(self.question)):
            result_answer = uts.word_sent(self.answer[j], format='text')
            self.answer[j] = result_answer
        for k in range(len(self.question)):
            result_date = uts.word_sent(self.date[k], format='text')
            self.date[k] = result_date

        return self

    def export_data(self):
        client = MongoClient('mongodb://localhost:27017/')  # kết nối DB
        db = client.TuyenSinh  # tao ket noi tới DB
        collection = db.WordSegmentation
        print('bat dau luu du lieu vao database')
        for question, answer, date in zip(self.question, self.answer, self.date):
            document = collection.insert([{"questions": question, "answers": answer, "dates": date}])


if __name__ == '__main__':
    list_question = []
    list_answer = []
    list_date = []
    word_data = DataExport(list_question, list_answer, list_date)
    a = word_data.get_data()
    for i in a.question:
        print(i)
    for j in a.answer:
        print(j)
    for k in a.date:
        print(k)
    b = word_data.segmentation()
    print('**********************************************************************************')
    for l in b.question:
        print(l)
    for m in b.answer:
        print(m)
    for n in b.date:
        print(n)
    word_data.export_data()
    print('Da luu du lieu vao database')






