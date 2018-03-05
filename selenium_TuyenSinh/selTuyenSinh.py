# -*- coding: utf-8 -*-
from selenium import webdriver
from pymongo import MongoClient
import time
import re

class SelTuyenSinh:
    def __init__(self, driver):
        self.driver = driver
    def hoidap(self):
        driver.get("http://hoidap.thongtintuyensinh.vn")
        time.sleep(10)
        driver.find_element_by_id("tli_1").click()#click Điểm chuẩn, nguyện vọng
        client = MongoClient('mongodb://localhost:27017/')#kết nối DB
        db = client.DBTuyenSinh  # tao ket noi tới DB
        collection = db.AnswerQuestion
        for i in range(1, 11):
            time.sleep(5)
            print("Page: " + str(i))
            list_ids = []
            list_answers = []
            list_dates = []
            driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[21]/a["+str(i)+"]").click()
            list_questions = driver.find_elements_by_css_selector(""".othertopic p""")  #lấy câu hỏi
            for ques in list_questions:
                print("******** Question ********\n\t" + ques.text)

            doc = driver.page_source    #lấy source HTML
            id_questions = re.findall(r'cnt[0-9]{4,5}', doc)    # lấy id cau hoi, tra loi
            for j in range(len(id_questions)):
                if j % 3 == 0:
                    list_ids.append(id_questions[j])

            for list_id in list_ids:    #lấy câu trả lời display:None =>innerHTML
                answer_id = driver.find_element_by_id(list_id)
                answers = answer_id.get_attribute("textContent")
                answers.strip()
                ngay = re.search("([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})",answers, re.M|re.I|re.U)
                if ngay != None:
                    list_dates.append(ngay.group(1))
                else:
                    list_dates.append("Ngày đang cập nhật")
                answers = re.sub(r"((\s{2,})|(\\[ntuva]))", "", answers)
                list_answers.append(answers)
            for ans in list_answers:
                print("******** answer ********\n\t" + ans)
            for day in list_dates:
                print("******** date ********\n\t" + day)

            for question, answer, date in zip(list_questions, list_answers, list_dates):    # lưu data vào MongoDB
                document = collection.insert([{"questions": question.text,"answers": answer ,"dates": date}])
                # driver = webdriver.PhantomJS()
                # tralois = driver.find_element_by_id("cnt34506")
                # print(tralois.get_attribute("innerHTML"))
                # print(driver.execute_script("return arguments[0].innerHTML", tralois))
                # print(tralois.get_attribute("textContent"))
                # print(driver.execute_script("return arguments[0].textContent", tralois))
    def cauhoithuonggap(self):
        driver.get("https://bigschool.vn/hoi-dap-ve-quy-che-tuyen-sinh-2017")
        client = MongoClient('mongodb://localhost:27017/')  # kết nối DB
        db = client.DBTuyenSinh  # tao ket noi tới DB
        collection = db.AnswerQuestion
        first_questions = driver.find_elements_by_css_selector("div.cct-text-read > div.des > p")#lấy câu hỏi đầu tiên
        source = driver.find_elements_by_class_name("ExternalClass0C7C753CD6524B6EB1708DFBCB2C3915")#lấy toàn bộ câu trả lời lẫn câu hỏi còn lại
        list_questions = []#danh sách câu hỏi
        list_answers = []#danh sách câu trả lời
        list_dates = []
        for i in first_questions:#lấy câu hỏi đầu tiên bỏ vào danh sách
            list_questions.append(i.text)
        for j in source:
            all_questions = re.findall(r"Hỏi:.*", j.text, re.M)#lấy toàn bộ câu hỏi còn lại
            answers = re.sub(r"Hỏi:.*", "", j.text)#cắt toàn bộ câu hỏi, để lại câu trả lời
            answers = answers.strip()
            all_answers = re.split("Trả lời:\s*", answers)#cắt chuỗi lớn bao gồm toàn bộ câu tl thành từng câu trả lời cho mỗi câu hỏi
            for k in all_questions:     #thêm các câu hỏi còn lại vào list
                list_questions.append(k)
            for h in all_answers:       #thêm các câu trả lời có nội dung vào list
                if h != '':
                    list_answers.append(h)
        date_long = driver.find_elements_by_class_name("cct-time")#lấy ngày 03/02/2017 | 15:02 GMT+7
        for n in date_long:
            date_short = re.search("([0-9]{2}/[0-9]{2}/[0-9]{4})", n.text)
            for m in range(len(list_questions)):
                list_dates.append(date_short.group())

        for question, answer, date in zip(list_questions, list_answers, list_dates):
            print("********Câu hỏi:******\n\t" + question)
            print("********Trả lời:******\n\t" + answer)
            print(date)
            document = collection.insert([{"questions": question, "answers": answer, "dates": date}])

if __name__ == '__main__':
    chrome_path = r"D:\\chromedriver_win32\\chromedriver.exe"
    chrome_opptions = webdriver.ChromeOptions()
    chrome_opptions.add_argument("--incognito")
    driver = webdriver.Chrome(chrome_path, chrome_options=chrome_opptions)
    tuyen_sinh = SelTuyenSinh(driver)
    tuyen_sinh.hoidap()
    tuyen_sinh.cauhoithuonggap()
    # driver.close()
    #driver.quit()

