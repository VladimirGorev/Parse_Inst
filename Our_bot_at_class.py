from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import random
import math
import requests
import os


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

    def put_like_to_post(self, user_post):
        """Method for adding a like to the post you specified. Post must be passed."""
        browser = self.browser
        browser.get(user_post)
        time.sleep(5)
        page_not_found = '/html/body/div[1]/section/main/div/h2'
        if self.xpath_find_element(page_not_found):
            print('There is no such post. Check the correctness of the entered url ')
            self.close_browser()
        else:
            like_button = '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button/div/span'
            browser.find_element_by_xpath(like_button).click()
            print(f'Like the post {user_post}')
            time.sleep(5)
            self.close_browser()

    def get_all_url_posts_user(self, user_page):
        """Method for collected all posts of the user page you specified."""
        browser = self.browser
        browser.get(user_page)
        time.sleep(3)
        page_not_found = '/html/body/div[1]/section/main/div/h2'
        if self.xpath_find_element(page_not_found):
            print(f'No such user {user_page} exist. Check the correctness of the entered url')
            self.close_browser()
        else:
            users_posts = int(browser.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text)
            print(f'All count posts at this user page:  {users_posts} posts')
            scrolls = math.ceil(users_posts / 12)
            print(f'Number of page scrolls: {scrolls} ')
            posts_urls = set()
            for i in range(0, scrolls):
                hrefs = browser.find_elements_by_tag_name('a')
                posts = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]
                for post in posts:
                    posts_urls.add(post)
                browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(4)
                print(f'Iteration page scroll:  {i+1}')
            file_name = user_page.split('/')[-2] + '  :  urls posts'
            with open(f'{file_name}.txt', 'a') as file:
                for post in posts_urls:
                    file.write(post + '\n')

    def put_likes_on_all_posts_on_this_page(self, user_page):
        """Method for adding likes to all posts of the user page you specified. To ensure that the script does not cause
         suspicion and does not lead to a ban, a delay has been added for the allowable number of installed likes. """
        browser = self.browser
        self.get_all_url_posts_user(user_page)
        file_name = user_page.split('/')[-2] + '  :  urls posts'

        with open(f'{file_name}.txt') as file:
            posts_urls_list = file.readlines()
            number_post = 0
            for url in posts_urls_list:
                number_post += 1
                try:
                    browser.get(url)
                    time.sleep(3)
                    like_button = '/html/body/div[1]/section/main/div/div[1]/article/' \
                                  'div[3]/section[1]/span[1]/button/div/span'
                    browser.find_element_by_xpath(like_button).click()
                    print(f'Like was successfully delivered to the post {number_post}:  {url}')
                    time.sleep(random.randrange(2, 4))
                except Exception as ex:
                    print(ex)
                    self.close_browser()
        self.close_browser()

    def download_user_content(self, user_page):
        """Method for downloading user content.We must download img and video at user page. User page must be entered"""
        browser = self.browser
        self.get_all_url_posts_user(user_page)
        user_name = user_page.split('/')[-2]
        file_name = user_page.split('/')[-2] + '  :  urls posts'
        list_img_and_video_urls = []
        if os.path.exists(f"{user_name}"):
            print(f"A folder {user_name} with the same name already exists")
        else:
            print(f'Create new dir user: {user_name}')
            os.mkdir(user_name)

        with open(f'{file_name}.txt') as file:
            posts_urls_list = file.readlines()
            for url in posts_urls_list:
                try:
                    browser.get(url)
                    time.sleep(10)
                    post_name = url.split('/')[-2]
                    path_img_src = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img'
                    path_img_src_2 = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div[1]/div[2]/div/' \
                                     'div/div/ul/li[2]/div/div/div/div[1]/img'
                    path_img_src_3 = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div[1]/' \
                                     'img'
                    path_video_src = '/html/body/div[4]/div[2]/div/article/div[2]/div/div/div[1]/div/div/video'
                    path_video_src_2 = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video'
                    if self.xpath_find_element(path_img_src):
                        img_src_url = browser.find_element_by_xpath(path_img_src).get_attribute('src')
                        list_img_and_video_urls.append(img_src_url)
                        get_img = requests.get(img_src_url)
                        with open(f"{user_name}/{user_name}_{post_name}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)
                        print(f'Img downloaded  at post: {url}')
                    elif self.xpath_find_element(path_img_src_2):
                        img_src_url = browser.find_element_by_xpath(path_img_src_2).get_attribute('src')
                        list_img_and_video_urls.append(img_src_url)
                        get_img = requests.get(img_src_url)
                        with open(f"{user_name}/{user_name}_{post_name}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)
                        print(f'Img downloaded  at post: {url}')
                    elif self.xpath_find_element(path_img_src_3):
                        img_src_url = browser.find_element_by_xpath(path_img_src_3).get_attribute('src')
                        list_img_and_video_urls.append(img_src_url)
                        get_img = requests.get(img_src_url)
                        with open(f"{user_name}/{user_name}_{post_name}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)
                        print(f'Img downloaded  at post: {url}')
                    elif self.xpath_find_element(path_video_src):
                        try:
                            video_src_url = browser.find_element_by_xpath(path_video_src).get_attribute('src')
                            list_img_and_video_urls.append(video_src_url)
                            get_video = requests.get(video_src_url)
                            with open(f"{user_name}/{user_name}_{post_name}_video.mp4", "wb") as video_file:
                                video_file.write(get_video.content)
                            print(f'Video downloaded  at post: {url}')
                        except Exception as ex:
                            print(ex)
                    elif self.xpath_find_element(path_video_src_2):
                        try:
                            video_src_url = browser.find_element_by_xpath(path_video_src_2).get_attribute('src')
                            list_img_and_video_urls.append(video_src_url)
                            get_video = requests.get(video_src_url)
                            with open(f"{user_name}/{user_name}_{post_name}_video.mp4", "wb") as video_file:
                                video_file.write(get_video.content)
                            print(f'Video downloaded  at post: {url}')
                        except Exception as ex:
                            print(ex)
                    else:
                        print(f"Sorry.Having problems with the content on this link {url}")
                        list_img_and_video_urls.append(f'Having problems with the content on this link: {url}')
                except Exception as ex:
                    print(ex)
            self.close_browser()
        with open(f'Img and video urls for download.txt', 'a') as file:
            for i in list_img_and_video_urls:
                file.write(i + '\n')

    def get_all_followers(self, user_page):
        """This method allows you to go to the page you specified, copy all the person's subscribers to a file,
         go to each page and subscribe to it.For correct operation, the number of subscribers to the page you
         specified should not exceed 1000."""
        browser = self.browser
        browser.get(user_page)
        time.sleep(3)
        page_not_found = '/html/body/div[1]/section/main/div/h2'
        user_name = user_page.split('/')[-2]
        if os.path.exists(f"{user_name}"):
            print(f"A folder{user_name} with the same name already exists")
        else:
            print(f'Create new dir user: {user_name}')
            os.mkdir(user_name)
        if self.xpath_find_element(page_not_found):
            print(f'No such user {user_page} exist. Check the correctness of the entered url')
            self.close_browser()
        else:
            print(f'User page is find. Create him new dir {user_name}')
        followers_button = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/'
                                                         'header/section/ul/li[2]/a/span')
        followers_count = int(followers_button.text)
        time.sleep(3)
        print(f'Count followers user {user_name} is {followers_count}')
        scrolls = int(math.ceil(followers_count/12))
        print(f'Count scrolls follower list is {scrolls}')
        time.sleep(3)
        followers_button.click()
        time.sleep(3)
        followers_url = browser.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        try:
            for i in range(1, scrolls):
                browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_url)
                time.sleep(random.randrange(2, 4))
                print(f"Scroll #{i}")
            all_urls_div = browser.find_elements_by_tag_name("a")
            followers_list_raw = []
            followers_set = set()
            for url in all_urls_div:
                try:
                    url = url.get_attribute("href")
                    url_split = url.split('/')
                    if len(url_split) != 5:
                        continue
                    else:
                        followers_list_raw.append(url)
                except Exception as ex:
                    print(ex)
            followers_list = followers_list_raw[4:]
            for follower in followers_list:
                followers_set.add(follower)
            with open(f"{user_name}/{user_name}_followers_list.txt", "a") as text_file:
                for link in followers_set:
                    text_file.write(link+'\n')
            with open(f"{user_name}/{user_name}_followers_list.txt") as text_file:
                users_urls = text_file.readlines()
                for user in users_urls:
                    browser.get(user)
                    time.sleep(3)
                    try:
                        already_subscribed = '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/' \
                                             'div/div[2]/div/span/span[1]/button/div/span'
                        follow_btn = '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/' \
                                     'span/span[1]/button'
                        follow_btn2 = '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button'
                        if self.xpath_find_element(already_subscribed):
                            print(f'We already subscribed at {user}')
                            continue
                        elif self.xpath_find_element(follow_btn):
                            follow = browser.find_element_by_xpath(follow_btn)
                            time.sleep(2)
                            print(f'We subscribed at {user}')
                            follow.click()
                            with open('People_we_subscribed_to .txt', 'a') as file:
                                file.write(user)
                            time.sleep(3)
                        elif self.xpath_find_element(follow_btn2):
                            follow = browser.find_element_by_xpath(follow_btn2)
                            time.sleep(2)
                            print(f'We subscribed at {user}')
                            follow.click()
                            with open('People_we_subscribed_to .txt', 'a') as file:
                                file.write(user)
                            time.sleep(3)
                        else:
                            print(f'Something went wrong with this link {user} ')
                    except Exception as ex:
                        print(ex)
        except Exception as ex:
            print(ex)
            self.close_browser()



serg = InstaBot('parsing_to_order', 'parsing')
# serg.login()
# serg.download_user_content('https://www.instagram.com/mashka192/')
# serg.download_user_content('https://www.instagram.com/mashkerya/')
# serg.get_all_followers('https://www.instagram.com/marta196/')

