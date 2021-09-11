import gc
import time
import requests
import mysql.connector
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def contas(user, pwd):
    src = 'https://contas.nexen.com.br/login'
    option = webdriver.ChromeOptions()
    tod = date.today().strftime("%Y-%m-%d")

    try:
        driver = webdriver.Chrome("./UI/chromedriver", options=option)
        wait = WebDriverWait(driver, 20)
        driver.get(src)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input#formBasicEmail')))
        driver.execute_script("window.stop();")

        usrIn = driver.find_element_by_css_selector("input#formBasicEmail")
        usrIn.send_keys(user)
        time.sleep(0.5)

        pwdIn = driver.find_element_by_css_selector("input#formBasicPassword")
        pwdIn.send_keys(pwd)
        time.sleep(0.5)

        signBtn = driver.find_element_by_css_selector("button[type='submit']")
        signBtn.click()
        time.sleep(15)

        cookies = driver.get_cookies()
        strCookie = ""
        for cookie in cookies:
            strCookie += cookie["name"] + "=" + cookie["value"] + ";"

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="scraping_products"
        )

        mycursor = mydb.cursor()

        headers = {
            "Cookie": strCookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
        }
        page = requests.get(
            "https://portalapi.nexen.com.br/erp/products?sellerId=&groupId=&term=&skip=&take=&type=", headers=headers)

        res = page.json()
        tot = len(res["data"]["products"])

        for i in range(tot):
            data = {}
            data["Category_COD"] = res["data"]["products"][i]["CAT_COD"]
            data["Category_Name"] = res["data"]["products"][i]["CAT_DESC"]
            data["Producct_COD"] = res["data"]["products"][i]["B1_COD"]
            data["Product_Name"] = res["data"]["products"][i]["B1_DESC"]
            data["Product_Price"] = "R$ " + \
                res["data"]["products"][i]["VLR_TOT"]
            data["Product_image"] = "https://nexen-bucket.s3.us-east-2.amazonaws.com/products/geral/geral1.jpeg"

            sql = "INSERT INTO nexen (Category_COD, Category_Name, Producct_COD, Product_Name, Product_Price, Product_image, Extracted_Date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (data["Category_COD"], data["Category_Name"], data["Producct_COD"],
                   data["Product_Name"], data["Product_Price"], data["Product_image"], tod)
            mycursor.execute(sql, val)

            mydb.commit()

        driver.close()
    except:
        pass

    gc.collect()
