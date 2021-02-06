from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import random
import math


class InstaBot:
    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.browser = webdriver.Chrome(
            executable_path='/home/volodia/Desktop/Mini_projects/Parse_Inst/chromedriver/chromedriver')

    def close_browser(self):
        """Method for closing the page and stop running Selenium """
        self.browser.close()
        self.browser.quit()

    def login(self):
        """Method for entering instagram """
        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(5)
        input_username = browser.find_element_by_name('username')
        input_username.clear()
        input_username.send_keys(self.username)
        time.sleep(5)
        input_password = browser.find_element_by_name('password')
        input_password.clear()
        input_password.send_keys(self.password)
        time.sleep(5)
        input_password.send_keys(Keys.ENTER)
        time.sleep(10)

    def search_and_likes_posts_by_hashtag(self, hashtag):
        """Method for searching posts by hashtag and adding likes to them. The number in the cycle needs to be changed
         depending on your desired number of likes and posts. To ensure that the script does not cause suspicion and
         does not lead to a ban, a delay has been added for the allowable number of installed likes.   """
        browser = self.browser
        browser.get(fr'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)
        for i in range(5):
            browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)
        hrefs = browser.find_elements_by_tag_name('a')
        posts = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]
        for url in posts:
            try:
                browser.get(url)
                time.sleep(5)
                like_button = '/html/body/div[1]/section/main/div/' \
                              'div[1]/article/div[3]/section[1]/span[1]/button/div/span'
                browser.find_element_by_xpath(like_button).click()
                time.sleep(random.randrange(95, 120))
            except Exception as ex:
                print(ex)
                self.close_browser()

    def xpath_find_element(self, url):
        """Method for checking conditions in other methods. """
        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def put_like_to_post(self, users_post):
        """Method for adding a like to the post you specified. Post must be passed."""
        browser = self.browser
        browser.get(users_post)
        time.sleep(5)
        page_not_found = '/html/body/div[1]/section/main/div/h2'
        if self.xpath_find_element(page_not_found):
            print('There is no such post. Check the correctness of the entered url ')
            self.close_browser()
        else:
            like_button = '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button/div/span'
            browser.find_element_by_xpath(like_button).click()
            print(f'Like the post {users_post}')
            time.sleep(5)
            self.close_browser()

    def put_likes_on_all_posts_on_this_page(self, users_page):
        """Method for adding likes to all posts of the user page you specified. To ensure that the script does not cause
         suspicion and does not lead to a ban, a delay has been added for the allowable number of installed likes. """
        browser = self.browser
        browser.get(users_page)
        time.sleep(3)
        page_not_found = '/html/body/div[1]/section/main/div/h2'
        if self.xpath_find_element(page_not_found):
            print(f'No such user {users_page} exist. Check the correctness of the entered url')
            self.close_browser()
        else:
            users_posts = int(browser.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text)
            print(users_posts)
            scrolls = math.ceil(users_posts / 12)
            posts_urls = set()
            for i in range(0, scrolls):
                hrefs = browser.find_elements_by_tag_name('a')
                posts = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]
                for post in posts:
                    posts_urls.add(post)
                browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(4)
                print(fr'Iteration #{i}')
            file_name = users_page.split('/')[-2]
            with open(f'{file_name}.txt', 'a') as file:
                for post in posts_urls:
                    file.write(post + '\n')
            with open(f'{file_name}.txt') as file:
                posts_urls_list = file.readlines()
                for url in posts_urls_list:
                    try:
                        browser.get(url)
                        time.sleep(3)
                        like_button = '/html/body/div[1]/section/main/div/div[1]/article/' \
                                      'div[3]/section[1]/span[1]/button/div/span'
                        browser.find_element_by_xpath(like_button).click()
                        print(f'Like was successfully delivered to the post {url}')
                        time.sleep(random.randrange(95, 120))
                    except Exception as ex:
                        print(ex)
                        self.close_browser()
        self.close_browser()


serg = InstaBot('username', 'password')
serg.login()
serg.search_and_likes_posts_by_hashtag('hamster')
serg.put_like_to_post('https://www.instagram.com/p/7Cg-U-BFiW/')
serg.put_likes_on_all_posts_on_this_page('https://www.instagram.com/mashka192/')
