from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import unicodedata as uni
import re
import time


def init():
    global driver

    # Chrome 실행 및 instagram 접속
    driver = webdriver.Chrome()
    url = 'https://www.instagram.com'
    driver.get(url)
    driver.implicitly_wait(5)

    # Login
    username_input = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.NAME, 'username')))
    password_input = driver.find_element(By.NAME, 'password')
    username_input.send_keys('adigau1234')
    password_input.send_keys('djelrkdb')
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    driver.implicitly_wait(5)


def move_to_target(user_tag: str):
    driver.get('https://www.instagram.com/' + user_tag + '/')

    first_posts = {
        "jjoo_kite": "a[href='/p/C6N8u-FBIIv/']",
        "daejeon_people": "a[href='/reel/C4xQmmRLNc3/']",
        "hungry_dj": "a[href='/p/C68VKIQPKct/']"
    }

    first = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, first_posts[user_tag])))
    first.click()


def get_content():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        content = soup.select('div._a9zs')[0].text
        content = uni.normalize('NFC', content)
    except:
        content = ' '
    tags = re.findall(r'#[^\s#,\\]+', content)
    try:
        date = soup.select("time._a9ze._a9zf")[0]['datetime'][:10]
    except IndexError:
        date = None
    content = content.split("#")[0]
    data = [content, tags, date]
    return data


def move_next():
    right = driver.find_element(By.CSS_SELECTOR, "svg[aria-label='다음']")
    right.click()
    driver.implicitly_wait(1)


def get_data(user_tag: str):
    move_to_target(user_tag)

    total_data = []
    while True:
        try:
            data = get_content()
            total_data.append(data)
            move_next()
        except NoSuchElementException:
            break

    return total_data


if __name__ == '__main__':
    init()
    time.sleep(5)
    daejeon_people_data = get_data("jjoo_kite")
    print(daejeon_people_data)
