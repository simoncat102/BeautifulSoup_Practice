import requests as req
import pandas as pd
from bs4 import BeautifulSoup

url_base = "http://books.toscrape.com/catalogue/"
url_link = 'page-1.html'
url = url_base + url_link
headers = {'simoncat102': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
# request = req.get(url, headers=headers)
# html_text = request.text  # request.content 所有的html標籤
# soup = BeautifulSoup(request.text, "html.parser")

file = open("bookname.txt", "w")  # 開啟要輸出的檔案 x = create_file / w = create if not exist


def get_category():  # 找出有多少種類 + 練習把text的空格去除
    soup = BeautifulSoup(req.get(url, headers=headers).text, "html.parser")
    tags = soup.select('ul.nav ul li a')
    cate_list = []

    for t in tags:
        category = t.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in category.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        cate_list.append(text)
    return cate_list


def next_page():  # 跳轉至下一頁
    soup = BeautifulSoup(req.get(url, headers=headers).text, "html.parser")
    tags = soup.select('li.next a')
    for link in tags:
        url_link = link.get('href')  # get link in this tags
    return url_link


def get_bookname(url):  # 找出網站頁面的書名 (easy way)
    soup = BeautifulSoup(req.get(url, headers=headers).text, "html.parser")
    tags = soup.select('article.product_pod a')
    for name in tags:
        bookname = name.get('title')
        if (bookname != None):
            print(bookname)
            file.write(bookname)
            file.write("\n")


# 找到書名為A開頭的書名 與 其詳細資訊(Bookname, Price, Availiable)
def get_moreinfo():
    global status_text
    soup = BeautifulSoup(req.get(url, headers=headers).text, "html.parser")
    tags = soup.select("div.image_container a")  # 看有什麼選擇

    # pandas的預設表格
    data = {'Bookname': [],
            'Price': [],
            'Status': [],
            }
    dataFrame = pd.DataFrame(data)  # 設定為df
    pd.set_option('display.width', 600)

    for info_link in tags:
        info_url_link = info_link.get("href")  # find the link
        pages_url = url_base + info_url_link  # 書頁連結

        soup_info = BeautifulSoup(req.get(pages_url, headers=headers).text, "html.parser")
        tags_price = soup_info.select("p.price_color")
        tags_bookname = soup_info.select("div.product_main h1")
        tags_status = soup_info.select("div.product_main p.availability")
        price = tags_price[0].get_text()[1:]  # 陣列中的第一個選項 抓價格
        bookname = tags_bookname[0].get_text()  # 抓書名

        for status in tags_status:
            status_text = status.get_text()
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in status_text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            status_text = '\n'.join(chunk for chunk in chunks if chunk)  # 抓狀態
            # dataFrame.at[index, 'Status'] = status_text
        pd.set_option("display.colheader_justify", "center")  # header靠左
        dataFrame = dataFrame.append({
            'Bookname': bookname,
            'Price': price,
            'Status': status_text
        }, ignore_index=True)
    print(dataFrame)


# main running area
get_moreinfo()

