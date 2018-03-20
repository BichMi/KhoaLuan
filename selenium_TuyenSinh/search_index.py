"""
    Đánh chỉ mục cho tài liệu và search theo query
"""
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from pymongo import MongoClient
import underthesea as uts
import re
import nltk
from nltk.tokenize import RegexpTokenizer


def word_separation(s):
    """
    Tách từ trong câu
    :return: List
    """
    # tách từ
    text = uts.word_sent(s, format='text')
    # lấy từ và trả về một mảng danh sách các từ đã tách
    tokenizer = RegexpTokenizer('\w+')
    print("tokenizer")
    print(tokenizer)
    tokens = tokenizer.tokenize(text)
    print('tokens')
    print(tokens)
    # ['đăng_kí', 'nguyện_vọng', '1', 'như', 'thế_nào', 'Em', 'cảm_ơn', 'ạ']
    return tokens

def clearn_stop_word(tokens):
    stop_words_tuyensinh = [u'dạ', u'cho', u'em', u'hỏi', u'ạ', u'tôi', u'cảm_ơn', u'cám_ơn', u'chị', u'anh',
                            u'thầy_cô', u'thầy', u'cô', u'vâng', u'vậy', u'e_e', u'c', u'ii']
    # lấy các stop word của tiếng anh đã được download cmd: nltk.download('stopwords')
    stop_words = nltk.corpus.stopwords.words('english')
    # tạo ra một list bao gồm stop word của tiếng anh và một số từ tiếng việt cần loại bỏ khỏi câu hỏi
    word_clear = stop_words + stop_words_tuyensinh
    result = ''
    for word in tokens:
        word = word.lower()
        if word not in word_clear:
            result += word + ' '
    result = result.strip()
    #đăng_kí nguyện_vọng 1 như thế_nào? em em cảm ơn
    return result

def index_search(s):
    """
    Đánh chỉ mục và search dựa vào câu query
    :param s:  câu truy vấn đã làm sạch : đăng kí nguyện vọng 1 như thế nào ?#dạ cho em hỏi, em muốn đăng kí nguyện vọng 1 thì như thế nào ạ?
    :return: list các tài liệu được tìm thấy
    """
    results_search = []
    results_search.append(s)
    client = MongoClient('mongodb://localhost:27017/') #kết nối MongoDB
    db = client.TuyenSinhDB #ket noi database
    collection = db.WordSegmentation  #ket noi collection của Database
    select_table = collection.find({}, {"_id":0})#read data
    # tiến hành đánh chỉ mục
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
    ix = create_in("/home/bichmi/Desktop/KhoaLuanCrawl/KhoaLuan/selenium_TuyenSinh/Data_index", schema)
    writer = ix.writer()
    for item in select_table:
        content = item['questions'] + ' ' + item['answers'] + ' ' + item['dates']
        writer.add_document(title=content, path=u"/a", content='')
    writer.commit()
    # tiến hành search dựa vào câu truy vấn và parse title
    with ix.searcher() as searcher:
        query = QueryParser("title", ix.schema).parse(s)
        results = searcher.search(query)
        # import pdb
        # pdb.set_trace()
        if len(results) <= 0:
            print("Không có kết quả phù hợp với câu hỏi!")
            return 0
        else:
            for hit in results:
                results_search.append(hit['title'])
            return results_search

def search_index_main():
    question_input = input('Nhập câu hỏi của bạn: ')
    question_input = re.sub(r"(\s{2,})", '', question_input)
    tokens = word_separation(question_input)
    s = clearn_stop_word(tokens)
    results_search_main = index_search(s)
    return results_search_main



if __name__ == '__main__':
    search_index_main()
