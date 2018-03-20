from selenium_TuyenSinh import search_index
import numpy
import math
import re

def format_data(results):#'\\w+'
    """
    :param results: list các tài liệu được tìm thấy
    :return: list các từ không trùng
    """
    data_out = []
    kq = []  # mảng lưu các từ đã tách của tất cả các tài liệu
    for item_result in results:
        i_of_item_result = search_index.word_separation(item_result)
        i_of_item_result = search_index.clearn_stop_word(i_of_item_result)
        data_out.append(i_of_item_result)
        i_of_item_result = re.findall('\w+', i_of_item_result)
        print(i_of_item_result)
        kq += i_of_item_result
    print(kq)
    kq_set = set(kq)  # mảng lưu từ sau khi loại bỏ từ trùng
    return (kq_set, data_out)
# tfi
def calculated_tfi(kq_set, data_out):
    tfi = []
    for word in kq_set:
        tfi.append(word)
        kq_index = []
        for k in data_out:
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
                sum += tfi[word_count][counts]
            dfi.append(sum)
    print('dfi: số lượng từ xuất hiện trong tài liệu')
    return dfi
# idfi
def calculated_idfi(dfi):

    # idfi  = log(n/dfi)
    idfi = []
    for item_dfi in range(0, len(dfi)):
        kq = (3.0 / dfi[item_dfi])
        kq1 = math.log10(kq)
        idfi.append(kq1)
    print('idfi: Mảng chứa các phần tử đã được tính = log(n/dfi)')
    return idfi
# wi
def calculated_wi(idfi, tfi):
    # wi = tfi x idfi
    wi = []
    tmp = []
    tmp_wi = []

    for item_tfi in range(1, len(tfi), 2):
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
        print('phan tu thu %d ' % item_idfi)
        print(wi_kq)
        wi.append(wi_kq)
    wi = numpy.array(wi)
    print('print wi')
    print(type(wi))
    print(wi)

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
    print(items_wi)

# similarity
if __name__ == '__main__':
    #đăng kí nguyện vọng 1 như thế nào? dạ em cảm ơn
    results = search_index.search_index_main()
    print(results)
    kq_set, data_out = format_data(results)
    print('kq_set')
    print(kq_set)
    print('data_out: mang luu tru du lieu cua tung tai lieu ke ca query')
    print(data_out)
    tfi = calculated_tfi(kq_set, data_out)
    print(tfi)

    dfi = calculated_dfi(tfi)
    print('dfi')
    print(dfi)
    print(len(dfi))
    idfi = calculated_idfi(dfi)
    wi = calculated_wi(idfi, tfi)

    # tfi = []
    # words = []  # lưu từ
    #
    # for word in kq_set:
    #     tfi.append(word)
    #     kq_index = []
    #     for k in data_out:
    #         sl = k.count(word)
    #         kq_index.append(sl)
    #     tfi.append(kq_index)
    # print('cấu trúc tfi bao gồm [từ,[so lượng từ trong tài liệu kể cả câu truy vấn]]')
    # print(tfi)
    # # dfi : số lượng từ trong tài liệu
    # dfi = []
    # for word_count in range(0, len(tfi)):
    #     if (word_count % 2 != 0):
    #         sum = 0
    #         for counts in range(1, len(tfi[word_count])):
    #             sum += tfi[word_count][counts]
    #         dfi.append(sum)
    # print('dfi: số lượng từ xuất hiện trong tài liệu')
    # print(dfi)
    # # idfi  = log(n/dfi)
    # idfi = []
    # for item_dfi in range(0, len(dfi)):
    #     kq = (3.0 / dfi[item_dfi])
    #     kq1 = math.log10(kq)
    #     idfi.append(round(kq1, 4))
    # print('idfi: Mảng chứa các phần tử đã được tính = log(n/dfi)')
    # print(idfi)
    # # wi = tfi x idfi
    # wi = []
    # tmp = []
    # tmp_wi = []
    #
    # for item_tfi in range(1, len(tfi), 2):
    #     tmp.append(tfi[item_tfi])
    # print(tmp)
    # print(len(tmp))
    # tmp_wi = numpy.array(tmp)
    # print(type(tmp_wi))
    # print(len(tmp_wi))
    # print(tmp_wi)
    # tm = []
    # tmp_idfi = []
    # for item_idfi in range(len(idfi)):
    #     wi_kq = tmp_wi[item_idfi] * idfi[item_idfi]
    #     print('phan tu thu %d ' % item_idfi)
    #     print(wi_kq)
    #     wi.append(wi_kq)
    # wi = numpy.array(wi)
    # print('print wi')
    # print(type(wi))
    # print(wi)
    #
    # items_wi = []  # chứa các mảng có các giá trị của wi theo cột(từng tài liệu)
    # shape_wi = wi.shape
    # x_shape_wi = shape_wi[0]  # 10
    # y_shape_wi = shape_wi[1]  # 4
    #
    # for j_wi in range(y_shape_wi):
    #     item_wi = []  # chứa giá trị của tung tài liệu
    #     for i_wi in range(x_shape_wi):
    #         tmp_kq = wi[i_wi][j_wi]
    #         item_wi.append(tmp_kq)  # giá trịiệu theo tài liệu
    #     items_wi.append(item_wi)
    # # ket qua dung de tinh
    # print(items_wi)
    # cosin = similarity(items_wi, data_input)
    # print(cosin)
    # # choise_documents(cosin)
