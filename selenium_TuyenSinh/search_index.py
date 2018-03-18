from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from pymongo import MongoClient
import underthesea as uts
import re
import nltk
from nltk.tokenize import RegexpTokenizer


def extract_question():
    stop_words_tuyensinh = [u'dạ', u'cho', u'em', u'hỏi', u'ạ', u'tôi', u'cảm_ơn', u'cám_ơn', u'chị', u'anh', u'thầy_cô', u'thầy', u'cô',u'vâng', u'vậy']
    question_input = input('Nhập câu hỏi của bạn: ')
    question_input = re.sub(r"(\s{2,})",'',question_input)
    # tách từ
    text = uts.word_sent(question_input, format='text')
    # lấy từ và trả về một mảng danh sách các từ đã tách
    tokenizer = RegexpTokenizer('\w+')
    tokens = tokenizer.tokenize(text)
    # lấy các stop word của tiếng anh đã được download cmd: nltk.download('stopwords')
    stop_words = nltk.corpus.stopwords.words('english')
    # tạo ra một list bao gồm stop word của tiếng anh và một số từ tiếng việt cần loại bỏ khỏi câu hỏi
    word_clear = stop_words + stop_words_tuyensinh
    result = ''
    for word in tokens:
        if word not in word_clear:
            result += word.lower() + ' '
    result = result.strip()
    return result

def index_search():

    ques_of_you = extract_question()
    print(ques_of_you)

    client = MongoClient('mongodb://localhost:27017/') #kết nối MongoDB
    db = client.TuyenSinh #ket noi database
    collection = db.WordSegmentation
    select_table = collection.find({}, {"_id":0})

    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
    ix = create_in("/home/bichmi/Desktop/KhoaLuanCrawl/KhoaLuan/selenium_TuyenSinh/Data_index", schema)
    writer = ix.writer()
    for item in select_table:
        content = item['questions'] + ' ' + item['answers'] + ' ' + item['dates']
        writer.add_document(title=item['questions'], path=u"/a",
                            content=content)
    writer.commit()
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(ques_of_you)
        # allow_q = query.Term("chapter", "rendering")
        #a = query.terms('questions')
        results = searcher.search(query)


        print(type(results))
        print(len(results))
        #đăng kí nguyện vọng 1 như thế nào ? đăng_kí nguyện_vọng 1
        #dạ cho em hỏi, em muốn đăng kí nguyện vọng 1 thì như thế nào ạ?

        # print(results[0])
        print(results)
        if len(results) > 0:
            for hit in results:
                print('************************')
                print(hit)
                print(hit['title'])
                print(hit['path'])
                print('******************')
                # print('values')
                # print(i.values())
                # print('items')
                # print(i.items())
                # print('fields')
                # print(i.fields())
                # print('itervalues')
                # print(i.itervalues())
                # print(i.docnum)
                # with open('hit["path"]') as fileobj:
                #     filecontents = fileobj.read()
                #
                # print(hit.highlights("content", text=filecontents))



if __name__ == '__main__':
    #w = extract_question()
    #print(w)
    index_search()

