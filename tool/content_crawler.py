from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import parser
import json
import unicodedata as uni
import time
import re
import numpy as np
import res.info as info


def init() -> None:
    global driver

    # ChromeOptions 설정
    options = Options()
    #options.add_argument("--headless")
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
    driver.implicitly_wait(5)


def move_next() -> None:
    right = driver.find_element(By.CSS_SELECTOR, "svg[aria-label='다음']")
    right.click()
    driver.implicitly_wait(2)


def get_content(soup) -> str | None:
    try:
        content = soup.select('div._a9zs')[0].text
        content = uni.normalize('NFC', content)
    except:
        content = None
    return content


def choose_parser(user_tag: str):
    match user_tag:
        case "daejeon_people":
            return parser.parse_daejeon_people
        case "matdongyeop":
            return parser.parse_matdongyeop


def get_like(soup) -> int | None:
    try:
        like = soup.select(
            '.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.xt0psk2.x1i0vuye.xvs91rp.x1s688f.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')[0].text
        like = int(re.findall(r'[\d]+', like)[0])
    except:
        like = None
    return like


def check_video(soup):
    video = soup.find('video')
    is_video = True if video else False
    return is_video


def get_data(user_tag: str) -> tuple[list[dict], list[int]]:
    parsing_func = choose_parser(user_tag)
    total_data = []
    total_like = []

    driver.get('https://www.instagram.com/' + user_tag + '/')
    first = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, info.first_posts[user_tag])))
    first.click()
    driver.implicitly_wait(2)

    for _ in range(info.valid_posts[user_tag]):
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        content = get_content(soup)
        is_video = check_video(soup)

        total_data.append(parsing_func(content, is_video))
        total_like.append(get_like(soup))

        move_next()
        driver.implicitly_wait(2)
    return total_data, total_like


def append_extra_info(total_data: list[dict], likes: list[int], user_tag: str) -> list[dict]:
    likes = np.array(likes)
    after_likes = likes / np.mean(likes)

    path = r"../res/img_url.json"
    with open(path, "r", encoding="utf-8") as json_file:
        img_urls = json.load(json_file)

    intact_data = []
    for idx, value in enumerate(total_data):
        total_data[idx]["like"] = after_likes[idx]
        total_data[idx]["img_url"] = img_urls[user_tag][idx]
        if (total_data[idx]["name"] and
                total_data[idx]["location"] and
                total_data[idx]["tags"] and
                total_data[idx]["time"]):
            intact_data.append(total_data[idx])

    return intact_data


def write_json(new_data: list[dict]) -> None:
    path = r"../res/data.json"
    with open(path, "r", encoding="utf-8") as json_file:
        load_data = json.load(json_file)
    load_data += new_data
    with open(path, "w", encoding="utf-8") as json_file:
        json.dump(load_data, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    init()
    time.sleep(5)
    user = "matdongyeop"
    content_data, like_data = get_data(user)
    final_data = append_extra_info(content_data, like_data, user)
    write_json(final_data)
