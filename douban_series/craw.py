import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import openpyxl
import pandas as pd

url = "https://movie.douban.com/tv/"
# r = requests.get(url)
# if r.status_code !=200:
#     raise Exception("status_code wrong")
# print(r.text)

driver = webdriver.Edge()
driver.get(url)
time.sleep(1)
driver.find_element(By.XPATH,"//span[text()='排序']").click()
time.sleep(1)
button = driver.find_element(By.XPATH,"//span[text()='高分优先']").click()
time.sleep(1)

while True:
    try:
     driver.find_element(By.XPATH,"//button[text()='加载更多']").click()
     time.sleep(1)
    except NoSuchElementException:
        break

html = driver.page_source
driver.quit()
# soup = BeautifulSoup(html,"html.parser")
# series = soup.find("ul",class_="explore_list").find_all("li")
# print(html)

def parse_the_whole_html(html):
    datas = []
    soup = BeautifulSoup(html, "html.parser")
    article_items = (
        soup.find("ul",class_="explore-list").find_all("li")
    )
    i = 1
    for article_item in article_items:
        rank = i
        i += 1
        info = article_item.find("div", class_="drc-subject-info")
        title = info.find("span", class_="drc-subject-info-title-text").get_text()
        print("titile is",title)
        detail = info.find("div",class_="drc-subject-info-subtitle").get_text()
        print(detail)
        stars = info.find("span", class_="drc-rating-stars")
        star = stars["data-rating"]
        print(star,"stars")
        # rating = stars.attrs['data-rating']
        rating_num = article_item.find("span",class_="drc-rating-num").get_text()
        # comment = stars[3].get_text()

        datas.append({
            "rank": rank,
            "stars": star,
            "title": title,
            "detail": detail,
            # "rating": rating.replace("rating", "").replace("-t", ""),
            "rating_num": rating_num,
            # "comments": comment.replace("人评价", "")
        })
    return datas

# for sery in series:
#     name = sery.find("div",class_= "drc-subject-info-subtitle").

datas = parse_the_whole_html(html)

print(len(datas),"dataset")

df = pd.DataFrame(datas)
df.to_excel("douban_topseries.xlsx")






