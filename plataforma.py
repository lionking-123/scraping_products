import gc
import time
import mysql.connector
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def plataforma(user, pwd):
    src = 'https://plataforma.genyx.com.br/Login/Login.aspx'
    option = webdriver.ChromeOptions()
    tod = date.today().strftime("%Y-%m-%d")

    try:
        driver = webdriver.Chrome("./UI/chromedriver", options=option)
        wait = WebDriverWait(driver, 20)
        driver.get(src)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input#txtUsuario')))
        driver.execute_script("window.stop();")

        usrIn = driver.find_element_by_css_selector("input#txtUsuario")
        usrIn.send_keys(user)
        time.sleep(0.5)

        pwdIn = driver.find_element_by_css_selector("input#txtSenha")
        pwdIn.send_keys(pwd)
        time.sleep(0.5)

        signBtn = driver.find_element_by_css_selector("input#btnLogin")
        signBtn.click()
        time.sleep(15)

        driver.get("https://plataforma.genyx.com.br/Ecommerce/Kits.aspx")
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.box-ecommerce')))
        driver.execute_script("window.stop();")

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="scraping_products"
        )

        mycursor = mydb.cursor()

        divs = driver.find_elements_by_css_selector("div.box-ecommerce")
        for div in divs:
            data = {}

            try:
                lab = div.find_element_by_tag_name("label")
                data["Product_Name"] = lab.text

                spans = div.find_elements_by_tag_name("span")
                data["Product_Capacity"] = spans[0].text
                data["Product_Structure"] = spans[1].text
                data["Product_Price"] = spans[2].text
                data["Product_Low_Price"] = spans[3].text

                img = div.find_element_by_tag_name("img")
                data["Product_Image"] = img.get_attribute("src")

                sql = "INSERT INTO genyx (Product_Name, Product_Capacity, Product_Structure, Product_Price, Product_Low_Price, Product_Image, Extracted_Date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (data["Product_Name"], data["Product_Capacity"], data["Product_Structure"],
                       data["Product_Price"], data["Product_Low_Price"], data["Product_Image"], tod)
                mycursor.execute(sql, val)

                mydb.commit()
            except:
                pass

        driver.close()
    except:
        pass

    gc.collect()
