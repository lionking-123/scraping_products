import gc
import time
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def aldo(user, pwd):
    src = 'https://www.aldo.com.br/login'
    option = webdriver.ChromeOptions()

    try:
        driver = webdriver.Chrome("./UI/chromedriver", options=option)
        wait = WebDriverWait(driver, 20)
        driver.get(src)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input#frm-login-uname')))
        driver.execute_script("window.stop();")

        usrIn = driver.find_element_by_css_selector("input#frm-login-uname")
        usrIn.send_keys(user)
        time.sleep(0.5)

        pwdIn = driver.find_element_by_css_selector("input#frm-login-pass")
        pwdIn.send_keys(pwd)
        time.sleep(0.5)

        signBtn = driver.find_element_by_css_selector("input[name='submit']")
        signBtn.click()
        time.sleep(15)

        datas = {}

        # headers = {
        #     "Cookie": "_gid=GA1.3.409842652.1631231486; Authentication=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjE3NywibmFtZSI6Ikxlb25hcmRvIENhc3RpbGhvcyIsImVtYWlsIjoibGVvcGNhc3RpbGhvc0BnbWFpbC5jb20iLCJyb2xlcyI6WyJJTlRFR1JBVE9SIl0sImlhdCI6MTYzMTI0Njc4MCwiZXhwIjoxNjMxMzMzMTgwfQ.0wsHOx-71_H4eGWxH1kE7pPRDKx4dITPY1koPt4xhdk; _ga=GA1.3.974851105.1631054628; _ga_9448RPNLYD=GS1.1.1631246277.3.1.1631246444.0",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
        # }
        # page = requests.get(
        #     "https://portalapi.nexen.com.br/erp/products?sellerId=&groupId=&term=&skip=&take=&type=", headers=headers)

        # res = page.json()
        # tot = len(res["data"]["products"])

        # for i in range(tot):
        #     data = {}
        #     data["Category_COD"] = res["data"]["products"][i]["CAT_COD"]
        #     data["Category_Name"] = res["data"]["products"][i]["CAT_DESC"]
        #     data["Producct_COD"] = res["data"]["products"][i]["B1_COD"]
        #     data["Product_Name"] = res["data"]["products"][i]["B1_DESC"]
        #     data["Product_Price"] = "R$ " + \
        #         res["data"]["products"][i]["VLR_TOT"]
        #     data["Product_image"] = "https://nexen-bucket.s3.us-east-2.amazonaws.com/products/geral/geral1.jpeg"

        #     datas[str(i)] = data

        driver.close()
    except:
        pass

    df = pd.DataFrame(data=datas).T
    df.to_csv("./results/contas.csv")

    gc.collect()


aldo("leonardo.faria@hotmail.com", "12345678")
