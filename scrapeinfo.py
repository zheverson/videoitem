from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import time
from pyvirtualdisplay import Display

def getupc(data, sleeptime):
    display = Display(visible=0, size=(800,600))
    display.start()
    a = webdriver.Firefox()
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
    a.close()
    display.stop()
    return data


def getpinimage(data, sleeptime):
    display = Display(visible=0, size=(1600,1200))
    display.start()
    a = webdriver.Firefox()
    a.get('https://www.pinterest.com')
    time.sleep(sleeptime)
    try:
        login = WebDriverWait(a, 5).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.Button.Module.NavigateButton.btn.emailLogin.hasText.rounded')))
        ActionChains(a).move_to_element(login).click(login).perform()
        time.sleep(sleeptime)
        a.find_element_by_name('username_or_email').send_keys('172329313@qq.com')
        a.find_element_by_name('password').send_keys('8326022')
        a.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(sleeptime)
        for i in data:
            a.find_element_by_tag_name('input').send_keys(i['name'], Keys.RETURN)
            time.sleep(sleeptime)
            try:
                imageurl = WebDriverWait(a, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='pinHolder']//div[@class='heightContainer']/img"))).get_attribute('src')
                print(imageurl)
                i['iamgeurl'] = imageurl
                try: 
                    print(a.find_element_by_xpath("//form//div[@class='tokenContainer']").text)
                    a.find_element_by_xpath("//form//a[@class='removeAll']").click()
                except NoSuchElementException:
                    a.save_screenshot("home/ec2-user/china/nosearch.png")
                    pass
                                  
            except TimeoutException:
                print("no image found")
                pass
    except TimeoutException:
        print('errortimeout')
        a.save_screenshot("/home/ec2-user/china/foo.png")
    a.close()
    display.stop()
    return data
