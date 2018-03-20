import underthesea as uts
from nltk.tokenize import RegexpTokenizer
import re
import nltk
import math
import numpy
import selenium_TuyenSinh.search_index as s

#tách từ
def extract_question(s):
    stop_words_tuyensinh = [u'dạ', u'cho', u'em', u'hỏi', u'ạ', u'tôi', u'cảm_ơn', u'cám_ơn', u'chị', u'anh', u'thầy_cô', u'thầy', u'cô',u'vâng', u'vậy']
    question_input = s
    question_input = re.sub(r"(\s{2,})",'',question_input)
    # tách từ
    text = uts.word_sent(question_input, format='text')
    # lấy từ và trả về một mảng danh sách các từ đã tách
    tokenizer = RegexpTokenizer('\w+')
    print('tokenizer')
    print(tokenizer)
    tokens = tokenizer.tokenize(text)
    print('tokens')
    print(tokens)
    # lấy các stop word của tiếng anh đã được download cmd: nltk.download('stopwords')
    stop_words = nltk.corpus.stopwords.words('english')
    # tạo ra một list bao gồm stop word của tiếng anh và một số từ tiếng việt cần loại bỏ khỏi câu hỏi
    word_clear = stop_words + stop_words_tuyensinh
    result = []
    for word in tokens:
        if word not in word_clear:
            result.append(word.lower())
    return result

# Đếm số lượng từ xuất hiện trong văn bản
def similarity(wi, data_input):
    ''' Tính độ tương đồng của câu'''

    if len(wi) <= 0:
        print("Array WI NO data!")
        return 0
    else:
        arr = []
        arr_qd = []
        cosin = []
        for i in wi:
            a = 0.0
            for j in i:
                a += math.pow(j,2)
            arr.append(round(math.sqrt(a), 4))

        for k in range(1,len(wi)):
            sum_qd = 0.0
            for h in range(len(wi[0])):
                sum_qd += wi[0][h] * wi[k][h]
            arr_qd.append(sum_qd)
        for m in range(len(arr_qd)):
            rs = arr_qd[m] / (arr[0] * arr[m + 1])
            cosin.append(data_input[m + 1])
            cosin.append(round(rs,4))
        return cosin
def choise_documents(cosin):
    '''sắp xếp giảm dần lấy một nữa tài l'''
    cosin.sort(reverse=True)
    for i_cosin in range(int(len(cosin)/2) + 1):
        print(cosin[i_cosin])

if __name__ == '__main__':
    q = "virus máy tính"
    d1 = "Máy tính bị nhiễm virus"
    d2 = "Xuất hiện virus mới trên điện thoại di động"
    d3 = "Tài liệu về máy tính"
    data_input= [q, d1, d2, d3]
    # mảng lưu từ đã được tách của từng tài liệu
    q_arr = []
    d1_arr = []
    d2_arr = []
    d3_arr = []
    data_out = [q_arr, d1_arr, d2_arr, d3_arr]
    kq = []     # mảng lưu các từ đã tách của tất cả các tài liệu
    for i in data_input:
        vi_tri = data_input.index(i)
        data_out[vi_tri] = extract_question(i)
        for j in data_out[vi_tri]:
            kq.append(j)
    kq_set = set(kq)  #mảng lưu từ sau khi loại bỏ từ trùng
    print('mảng lưu các từ đã tách của tất cả các tài liệu kq')
    print(kq)
    print('mảng lưu từ sau khi loại bỏ từ trùng (set kq)')
    print(kq_set)
    tfi = []
    words = []#lưu từ

    for word in kq_set:
        tfi.append(word)
        kq_index = []
        for k in data_out:
            sl = k.count(word)
            kq_index.append(sl)
        tfi.append(kq_index)
    print('cấu trúc tfi bao gồm [từ,[so lượng từ trong tài liệu kể cả câu truy vấn]]')
    print(tfi)
    # dfi : số lượng từ trong tài liệu
    dfi = []
    for word_count in range(0,len(tfi)):
        if (word_count % 2 != 0):
            sum = 0
            for counts in range(1,len(tfi[word_count])):
                sum += tfi[word_count][counts]
            dfi.append(sum)
    print('dfi: số lượng từ xuất hiện trong tài liệu')
    print(dfi)
    #idfi  = log(n/dfi)
    idfi = []
    for item_dfi in range(0, len(dfi)):
            kq = (3.0 / dfi[item_dfi])
            kq1 = math.log10(kq)
            idfi.append(round(kq1,4))
    print('idfi: Mảng chứa các phần tử đã được tính = log(n/dfi)')
    print(idfi)
    # wi = tfi x idfi
    wi = []
    tmp = []
    tmp_wi = []

    for item_tfi in range(1,len(tfi), 2):
        tmp.append(tfi[item_tfi])
    print(tmp)
    print(len(tmp))
    tmp_wi = numpy.array(tmp)
    print(type(tmp_wi))
    print(len(tmp_wi))
    print(tmp_wi)
    tm = []
    tmp_idfi = []
    for item_idfi in range(len(idfi)):
        wi_kq = tmp_wi[item_idfi] * idfi[item_idfi]
        print('phan tu thu %d ' %item_idfi)
        print(wi_kq)
        wi.append(wi_kq)
    wi = numpy.array(wi)
    print('print wi')
    print(type(wi))
    print(wi)

    items_wi = []   #chứa các mảng có các giá trị của wi theo cột(từng tài liệu)
    shape_wi = wi.shape
    x_shape_wi = shape_wi[0]#10
    y_shape_wi = shape_wi[1]  # 4

    for j_wi in range(y_shape_wi):
        item_wi = []    #chứa giá trị của tung tài liệu
        for i_wi in range(x_shape_wi):
            tmp_kq = wi[i_wi][j_wi]
            item_wi.append(tmp_kq)  #giá trịiệu theo tài liệu
        items_wi.append(item_wi)
    # ket qua dung de tinh
    print(items_wi)
    cosin = similarity(items_wi, data_input)
    print(cosin)
    # choise_documents(cosin)




