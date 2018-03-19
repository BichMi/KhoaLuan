from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from pymongo import MongoClient
import re
import nltk

def extract():
    question_input = input('Nhập câu hỏi của bạn: ')
    question_input = re.sub(r"(\s{2,})",'',question_input.lower())
    print(question_input)
    sw = nltk.corpus.stopwords.words('english')

if __name__ == '__main__':
    extract()

    # client = MongoClient('mongodb://localhost:27017/') #kết nối MongoDB
    # db = client.TuyenSinh #ket noi database
    # collection = db.WordSegmentation
    # select_table = collection.find({}, {"_id":0})
    #
    # schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
    # ix = create_in("/home/bichmi/Desktop/KhoaLuanCrawl/KhoaLuan/selenium_TuyenSinh/Data_index", schema)
    # writer = ix.writer()
    # for item in select_table:
    #     conten = item['questions'] + ' ' + item['answers'] + ' ' + item['dates']
    #     writer.add_document(title=item['questions'], path=u"/a",
    #                         content=conten)
    # writer.commit()
    # # khoong chaaps nhaajn cos daaus chaams hoir
    # with ix.searcher() as searcher:
    #     query = QueryParser("content", ix.schema).parse('Em thi trường sĩ_quan nhưng không đủ điểm vậy em có_thể đem điểm xét vào trường khác được không  Điểm em trên điểm sàn vậy xét nguyện_vọng nào')
    #
    #     results = searcher.search(query)
    #     print(type(results))
    #     print(len(results))
    #     print(results[0])