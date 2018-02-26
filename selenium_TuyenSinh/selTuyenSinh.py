# -*- coding: utf-8 -*-
from selenium import webdriver
from pymongo import MongoClient
import time
import re

class SelTuyenSinh():

    chrome_path = r"D:\\chromedriver_win32\\chromedriver.exe"
    chrome_opptions = webdriver.ChromeOptions()
    chrome_opptions.add_argument("--incognito")
    driver = webdriver.Chrome(chrome_path, chrome_options=chrome_opptions)
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
        #lấy câu hỏi
        list_questions = driver.find_elements_by_css_selector(""".othertopic p""")
        for ques in list_questions:
            print("******** Question ********\n\t" + ques.text)

        #lấy id cau hoi, tra loi
        doc = driver.page_source
        id_questions = re.findall(r'cnt[0-9]{4,5}', doc)
        for j in range(len(id_questions)):
            if j % 3 == 0:
                list_ids.append(id_questions[j])
        #driver = webdriver.PhantomJS()
        #tralois = driver.find_element_by_id("cnt34506")
        #print(tralois.get_attribute("innerHTML"))
        #print(driver.execute_script("return arguments[0].innerHTML", tralois))
        #print(tralois.get_attribute("textContent"))
        #print(driver.execute_script("return arguments[0].textContent", tralois))
        #lấy câu trả lời display:None =>innerHTML
        for list_id in list_ids:
            #print("*********id*********\n\t" + list_id)
            answer_id = driver.find_element_by_id(list_id)
            answer = answer_id.get_attribute("textContent")
            answer.strip()
            ngay = re.search("([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})",answer, re.M|re.I|re.U)
            if ngay != None:
                list_dates.append(ngay.group(1))
            else:
                list_dates.append("Ngày đang cập nhật")
            answer = re.sub(r"((\s{2,})|(\\[ntuva]))", "", answer)
            list_answers.append(answer)
        for ans in list_answers:
            print("******** answer ********\n" + ans)
        for day in list_dates:
            print("******** date ********\n" + day)
        # for id, ques, answ, date in zip(list_ids, list_questions, list_answers, list_dates):
        #
        #     document = collection.insert([{"id_questions": id, "questions": ques.text,"answers": answ ,"dates": date}])


    driver.close()
    driver.quit()

