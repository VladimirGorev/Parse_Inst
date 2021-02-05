from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from data import username, password
import time
import random


def login(username_, password_):
    """We go to the site https://www.instagram.com , enter the name and password in the fields we found for filling """
    browser = webdriver.Chrome(
        executable_path='/home/volodia/Desktop/Mini_projects/Parse_Inst/chromedriver/chromedriver')
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


# login(username, password)

def search_and_likes(username_, password_, hashtag):

    """Function for the second branch in which we do a hashtag search and post like. Adapted to run indefinitely.  """
    browser = webdriver.Chrome(
        executable_path='/home/volodia/Desktop/Mini_projects/Parse_Inst/chromedriver/chromedriver')
    browser.get('https://www.instagram.com')
    try:
        time.sleep(3)
        input_username = browser.find_element_by_name('username')
        input_username.clear()
        input_username.send_keys(username_)
        time.sleep(3)
        input_password = browser.find_element_by_name('password')
        input_password.clear()
        input_password.send_keys(password_)
        time.sleep(3)
        input_password.send_keys(Keys.ENTER)
        time.sleep(3)
        try:
            browser.get(fr'https://www.instagram.com/explore/tags/{hashtag}/')
            time.sleep(5)
            for i in range(5):
                browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(2)
            hrefs = browser.find_elements_by_tag_name('a')

            """ We can write a simple loop to traverse and sort all links """
            # posts = []
            # for item in hrefs:
            #     href = item.get_attribute('href')
            #     if '/p/' in href:
            #         posts.append(href)
            #         print(href)

            """ Or in python zen using a generator  """
            posts = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]
            for url in posts:
                try:
                    browser.get(url)
                    time.sleep(5)
                    like = browser.find_element_by_xpath(
                        '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button/div/span') \
                        .click()
                    time.sleep(random.randrange(95, 120))
                except Exception as ex:
                    print(ex)
            browser.close()
            browser.quit()
        except Exception as ex:
            print(ex)
            browser.close()
            browser.quit()
    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()


search_and_likes(username, password, 'hamster')




