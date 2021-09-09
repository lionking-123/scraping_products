import gc
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def sicessolar(user, pwd):
    src = 'https://app.sicessolar.com/'
    option = webdriver.ChromeOptions()
    # option.add_argument("--headless")
    # capa = DesiredCapabilities.CHROME
    # capa["pageLoadStrategy"] = "none"

    try:
        driver = webdriver.Chrome("./UI/chromedriver", options=option)
        wait = WebDriverWait(driver, 20)
        driver.get(src)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'a.nav-link.sign-in-act')))
        driver.execute_script("window.stop();")

        signBtn = driver.find_element_by_css_selector("a.nav-link.sign-in-act")
        signBtn.click()
        time.sleep(1)

        usrIn = driver.find_element_by_css_selector("input#username")
        usrIn.send_keys(user)
        time.sleep(0.5)

        pwdIn = driver.find_element_by_css_selector("input#password")
        pwdIn.send_keys(pwd)
        time.sleep(0.5)

        signBtn = driver.find_element_by_css_selector("a.sign-in-btn")
        signBtn.click()
        time.sleep(15)

        driver.get("https://app-plt.sicessolar.com/express/product/kit")
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.sc-RbTVP.evvypI')))
        driver.execute_script("window.stop();")

        datas = {}
        cnt = 1

        while(True):
            divs = driver.find_elements_by_css_selector("div.sc-RbTVP.evvypI")
            for div in divs:
                data = {}

                img = div.find_element_by_tag_name("img")
                data["Product_image"] = img.get_attribute("src")

                spans = div.find_elements_by_tag_name("span")
                data["Product_name"] = spans[0].text
                data["Product_price"] = spans[1].text

                datas[str(cnt)] = data
                cnt += 1

            btn = driver.find_element_by_css_selector(
                "div > button:nth-child(5)")
            if(btn.get_attribute("disabled") != None):
                print("Cancel")
                break
            else:
                print(btn.get_attribute("class"))
                driver.execute_script(
                    "document.querySelector('div > button:nth-child(5)').click();")
                time.sleep(9)
                continue

        driver.close()
    except:
        pass

    df = pd.DataFrame(data=datas).T
    df.to_csv("./results/sicessolar.csv")

    gc.collect()
