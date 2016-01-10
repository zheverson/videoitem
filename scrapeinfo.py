from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import time

def getupc(data, sleeptime):
    a = webdriver.Chrome()
    for i in data:
        a.get('https://www.google.com/ncr')
        time.sleep(sleeptime)
        search = WebDriverWait(a, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text']")))
        ActionChains(a).move_to_element(search).click(search).send_keys(i['name'] + ' upc', Keys.ENTER).perform()
        time.sleep(sleeptime)
        contents = WebDriverWait(a, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='g']")))
        try:
            upc = next(
                    (re.split(r'/', href.find_element_by_tag_name('a').get_attribute('href'))[-1] for
                     href in contents if
                     href.find_element_by_tag_name('a').get_attribute('href').startswith(
                             'http://www.upcitemdb.com/upc')))
            i['upc'] = upc
        except StopIteration:
            pass
    return data


def getpinimage(data, sleeptime):
    a = webdriver.Chrome()
    for i in data:
        a.get('https://www.pinterest.com')
        time.sleep(sleeptime)
        login = WebDriverWait(a, 5).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.Button.Module.NavigateButton.btn.emailLogin.hasText.rounded')))
        ActionChains(a).move_to_element(login).click(login).perform()
        time.sleep(sleeptime)
        a.find_element_by_name('username_or_email').send_keys('172329313@qq.com')
        a.find_element_by_name('password').send_keys('8326022')
        a.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(sleeptime)
        a.find_element_by_tag_name('input').send_keys(i['name'], Keys.RETURN)
        time.sleep(sleeptime)
        imageurl = WebDriverWait(a, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='heightContainer']/img"))).get_attribute('src')
        i['iamgeurl'] = imageurl
    return data
