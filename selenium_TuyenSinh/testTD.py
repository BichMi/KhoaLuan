import underthesea as uts
from nltk.tokenize import RegexpTokenizer
import re
import nltk

#tách từ
def extract_question():
    stop_words_tuyensinh = [u'dạ', u'cho', u'em', u'hỏi', u'ạ', u'tôi', u'cảm_ơn', u'cám_ơn', u'chị', u'anh', u'thầy_cô', u'thầy', u'cô',u'vâng', u'vậy']
    question_input = input('Nhập câu hỏi của bạn: ')
    question_input = re.sub(r"(\s{2,})",'',question_input.lower())
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
            result += word + ' '
    result = result.strip()
    return result

# Đếm số lượng từ xuất hiện trong văn bản

if __name__ == '__main__':
    q = "virus máy tính"
    d1 = "Máy tính bị nhiễm virut"
    d2 = "Xuất hiện virut mới trên điện thoại di động"
    d3 = "Tài liệu về máy tính"

    extract_question()