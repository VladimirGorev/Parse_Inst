
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from data import username, password
import time


def login(username_, password_):
    """We go to the site https://www.instagram.com , enter the name and password in the fields we found for filling """
    browser = webdriver.Firefox(
        executable_path='/home/volodia/Desktop/Mini_projects/Parse_Inst/Firefoxdriver/geckodriver')
    browser.get('https://www.instagram.com')
    try:
        time.sleep(5)
        input_username = browser.find_element_by_name('username')
        input_username.clear()
        input_username.send_keys(username_)
        time.sleep(5)
        input_password = browser.find_element_by_name('password')
        input_password.clear()
        input_password.send_keys(password_)
        time.sleep(5)
        input_password.send_keys(Keys.ENTER)
        time.sleep(10)
        browser.close()
        browser.quit()
    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()


login(username, password)




