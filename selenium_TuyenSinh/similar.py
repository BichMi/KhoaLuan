from selenium_TuyenSinh import search_index
import numpy
import math
import re

def format_data(results):
    """
    :param results: list các tài liệu được tìm thấy
    :return: list các từ không trùng
    """
    kq_for_tfi = []
    data_out = []
    kq = []  # mảng lưu các từ đã tách của tất cả các tài liệu
    for item_result in results:
        i_of_item_result = search_index.word_separation(item_result)
        i_of_item_result = search_index.clearn_stop_word(i_of_item_result)
        data_out.append(i_of_item_result)
        i_of_item_result = re.findall('\w+', i_of_item_result)
        print(i_of_item_result)
        kq += i_of_item_result
        kq_for_tfi.append(i_of_item_result)
    print(kq)
    kq_set = set(kq)  # mảng lưu từ sau khi loại bỏ từ trùng
    return (kq_set, data_out, kq_for_tfi)
# tfi
def calculated_tfi(kq_set, kq_for_tfi):
    tfi = []
    for word in kq_set:
        tfi.append(word)
        kq_index = []
        for k in kq_for_tfi:
            sl = k.count(word)
            kq_index.append(sl)
        tfi.append(kq_index)
    # cấu trúc tfi bao gồm [từ,[so lượng từ trong tài liệu kể cả câu truy vấn]]'
    return tfi
# dfi
def calculated_dfi(tfi):
    dfi = []
    for word_count in range(0, len(tfi)):
        if (word_count % 2 != 0):
            sum = 0
            for counts in range(1, len(tfi[word_count])):
                if tfi[word_count][counts] > 0:
                    sum += 1
            dfi.append(sum)
    print('dfi: số lượng từ xuất hiện trong tài liệu')
    return dfi
# idfi
def calculated_idfi(dfi, data_out):
    # idfi  = log(n/dfi)
    idfi = []
    for item_dfi in range(0, len(dfi)):
        kq = ((len(data_out) - 1) * 1.0) / dfi[item_dfi]
        kq1 = math.log10(kq)
        idfi.append(round(kq1,4))
    return idfi
# wi
def calculated_wi(idfi, tfi):
    # wi = tfi x idfi
    wi = []
    tmp = []
    tmp_wi = []

    for item_tfi in range(1, len(tfi), 2):
        tmp.append(tfi[item_tfi])
    tmp_wi = numpy.array(tmp)
    for item_idfi in range(len(idfi)):
        wi_kq = tmp_wi[item_idfi] * idfi[item_idfi]
        wi.append(wi_kq)
    wi = numpy.array(wi)

    items_wi = []  # chứa các mảng có các giá trị của wi theo cột(từng tài liệu)
    shape_wi = wi.shape
    x_shape_wi = shape_wi[0]  # 10
    y_shape_wi = shape_wi[1]  # 4

    for j_wi in range(y_shape_wi):
        item_wi = []  # chứa giá trị của tung tài liệu
        for i_wi in range(x_shape_wi):
            tmp_kq = wi[i_wi][j_wi]
            item_wi.append(tmp_kq)  # giá trịiệu theo tài liệu
        items_wi.append(item_wi)
    # ket qua dung de tinh
    return items_wi

# similarity
def similarity(wi, results):
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
            arr.append(round(math.sqrt(a), 4))# tinh q2 va d2
        print('arr')
        print(arr)
        for k in range(1,len(wi)):
            sum_qd = 0.0
            for h in range(len(wi[0])):
                sum_qd += wi[0][h] * wi[k][h]
            arr_qd.append(sum_qd)
        print('tong cua q d')
        print(arr_qd)
        for m in range(len(arr_qd)):
            rs = arr_qd[m] / (arr[0] * arr[m + 1])
            cosin.append(results[m + 1])
            cosin.append(round(rs,4))
        return cosin
if __name__ == '__main__':
    #đăng kí nguyện vọng 1 như thế nào? dạ em cảm ơn
    results = search_index.search_index_main()
    print('results')
    print(len(results))
    print(results)
    kq_set, data_out, kq_for_tfi = format_data(results)
    print('kq_set')
    print(kq_set)
    print('data_out: mang luu tru du lieu cua tung tai lieu ke ca query')
    print(data_out)
    print('DO DAI MANG DATA OUT')
    print(len(data_out))
    tfi = calculated_tfi(kq_set, kq_for_tfi)
    print('tfi')
    print(tfi)
    dfi = calculated_dfi(tfi)
    print('dfi')
    print(dfi)
    print(len(dfi))
    idfi = calculated_idfi(dfi, data_out)
    print('idfi')
    print(idfi)
    wi = calculated_wi(idfi, tfi)
    print('wi')
    print(len(wi))
    print(wi)
    cosin = similarity(wi, results)
    print(cosin)

