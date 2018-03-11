from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/') #kết nối MongoDB
db = client.TuyenSinh #ket noi database
collection = db.WordSegmentation
select_table = collection.find({}, {"_id":0})
i = 1
ques = input('Nhập câu hỏi của bạn: ')
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
ix = create_in("/home/bichmi/Desktop/KhoaLuanCrawl/KhoaLuan/selenium_TuyenSinh/Data_index", schema)
writer = ix.writer()
for item in select_table:
    conten = item['questions'] + ' ' + item['answers'] + ' ' + item['dates']
    writer.add_document(title=item['questions'], path=u"/a",
                        content=conten)
writer.commit()
# khoong chaaps nhaajn cos daaus chaams hoir
with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse('Em thi trường sĩ_quan nhưng không đủ điểm vậy em có_thể đem điểm xét vào trường khác được không  Điểm em trên điểm sàn vậy xét nguyện_vọng nào')

    results = searcher.search(query)
    print(type(results))
    print(len(results))
    print(results[0])