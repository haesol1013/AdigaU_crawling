from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import res.info as info


def init() -> None:
    global driver

    # ChromeOptions 설정
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

    # Chrome 실행 및 instagram 접속
    driver = webdriver.Chrome(options=options)
    url = 'https://www.instagram.com'
    driver.get(url)
    driver.implicitly_wait(5)

    # Login
    username_input = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.NAME, 'username')))
    password_input = driver.find_element(By.NAME, 'password')
    username_input.send_keys(info.insta_id)
    password_input.send_keys(info.insta_pw)
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(1)
    driver.implicitly_wait(5)


def get_photos(user_tag: str):
    driver.get('https://www.instagram.com/' + user_tag + '/')

    photos = []
    last_height = driver.execute_script("return document.body.scrollHeight")  # 초기 페이지 높이 저장
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for div in soup.find_all('div', class_='_aagv'):
            img = div.find('img')
            if img and img.get('src'):
                photo_url = img['src']
                if photo_url not in photos:
                    photos.append(photo_url.replace("https", "http"))

        if len(photos) >= info.valid_posts[user_tag]:
            break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height

    return {user_tag: photos[:info.valid_posts[user_tag]]}


def write_json(new_data, user_tag) -> None:
    path = r"../res/img_url.json"
    with open(path, "r", encoding="utf-8") as json_file:
        load_data = json.load(json_file)
    load_data[user_tag] = new_data[user_tag]
    with open(path, "w", encoding="utf-8") as json_file:
        json.dump(load_data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    init()
    time.sleep(5)
    user = "daejeon_people"
    img_urls = get_photos(user)
    write_json(img_urls, user)
