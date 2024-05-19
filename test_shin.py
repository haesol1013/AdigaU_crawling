from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import unicodedata as uni
import re


class Crawler:
    def __init__(self, profile: str, first_post: str) -> None:
        self.profile = profile
        self.first_post = first_post

        # open web_driver
        self.driver = webdriver.Chrome()
        url = "https://www.instagram.com"
        self.driver.get(url)
        self.driver.implicitly_wait(2)

        # login to instagram
        username_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
        password_input = self.driver.find_element(By.NAME, "password")
        username_input.send_keys("adigau1234")
        password_input.send_keys("djelrkdb")
        login = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login.click()

    def get_target_url(self) -> str:
        return "https://www.instagram.com/" + self.profile + "/"

    def get_content(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            content = soup.select('div._a9zs')[0].text
            content = uni.normalize('NFC', content)
        except:
            content = ' '

        tags = re.findall(r'#[^Ws#,\\]+', content)

        try:
            date = soup.select("time._a9ze._a9zf")[0]['datetime'][:10]
        except IndexError:
            date = None

        content = content.split("#")[0]
        data = [content, tags, date]
        return data

    def move_next(self):
        right = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='다음']")))
        right.click()
        self.driver.implicitly_wait(2)

    def get_data(self):
        # open profile
        self.driver.get(self.get_target_url())
        self.driver.implicitly_wait(2)

        # click
        first = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href = '/p/C6N8u-FBIIv/']")))
        first.click()

        total_data = []

        while True:
            try:
                total_data.append(self.get_content())
                self.move_next()
            except NoSuchElementException:
                break
            except:
                self.move_next()
        return total_data


if __name__ == "__main__":
    page1 = Crawler("jjoo_kite", '/p/C6N8u-FBIIv/')
    data = page1.get_data()
