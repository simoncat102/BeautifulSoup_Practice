import requests as req
from bs4 import BeautifulSoup

url_base = "http://books.toscrape.com/catalogue/"
url_link = 'page-1.html'
url = url_base + url_link
headers = {'simoncat102': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
# request = req.get(url, headers=headers)
# html_text = request.text  # request.content 所有的html標籤
# soup = BeautifulSoup(request.text, "html.parser")

file = open("bookname.txt", "w")  # 開啟要輸出的檔案 x = create_file / w = create if not exist


def get_category():
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


def next_page():
    soup = BeautifulSoup(req.get(url, headers=headers).text, "html.parser")
    tags = soup.select('li.next a')
    for link in tags:
        url_link = link.get('href')
    return url_link


def get_bookname(url):
    soup = BeautifulSoup(req.get(url, headers=headers).text, "html.parser")
    tags = soup.select('article.product_pod a')
    for name in tags:
        bookname = name.get('title')
        if (bookname != None):
            print(bookname)
            file.write(bookname)
            file.write("\n")
# 找到書名為A開頭的書名 與 其詳細資訊
def get_moreinfo():
    soup = BeautifulSoup(req.get(url, headers = headers).text, "html.parser")
    tags = soup.select("") #看有什麼選擇

# 把找到的資訊存成csv

for i in range(2):
    get_bookname(url)
    url = url_base + next_page()

