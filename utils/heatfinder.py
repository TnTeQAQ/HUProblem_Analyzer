# 用于获取题目在搜索引擎中的搜索词条数,以及搜索引擎返回结果的第一页
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import re
from time import sleep

headers = {
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

def bing(q):
    results = {}
    url_bing = f'https://www.bing.com/search?q="{quote(q)}"'
    # print(url_bing)
    res = requests.get(url=url_bing, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    a_labels = soup.select('#b_results > li > h2 > a')
    for a in a_labels:
        results[a.text] = a.get('href')
    count = soup.select('.sb_count')[0].text
    return int(count[2:-4].replace(',', '')), results

def google(q):
    results = {}
    url_google = f'https://www.google.com/search?q="{quote(q)}"'
    # print(url_google)
    res = requests.get(url=url_google, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    a_labels = soup.select('#rso > div > div > div > div.kb0PBd.cvP2Ce.jGGQ5e > div > div > span > a')
    for a in a_labels:
        results[a.select('a > h3')[0].text] = a.get('href')
    count = soup.select('#result-stats')[0].text
    res = re.findall(r' [0-9,]* ', count)
    return int(res[0][1:-1].replace(',', '')), results

def google_scholar(q):
    results = {}
    url_google_scholar = f'https://scholar.google.com/scholar?q={quote(q)}'
    # print(url_google_scholar)
    res = requests.get(url=url_google_scholar, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    a_labels = soup.select('.gs_rt > a')
    for a in a_labels:
        results[a.text] = a.get('href')
    count = soup.select('.gs_ab_mdw')[1].text
    res = re.findall(r' [0-9,]* ', count)
    return int(res[0][1:-1].replace(',', '')), results

get_heat_functions = [google, bing, google_scholar]

def get_heat(q):
    results_count = {}
    first_page_results = {}
    for func in get_heat_functions:
        err_n = 0
        while True:
            try:
                if err_n == 3:
                    results_count[func.__name__] = 'error!'
                    first_page_results[func.__name__] = 'error!'
                    print(f'{func.__name__}查询出错!!!')
                    break
                results_count[func.__name__], first_page_results[func.__name__] = func(q)
                break
            except:
                err_n += 1
                print(f'{func.__name__}查询出错，正在重新查询')
                sleep(1)
    return results_count, first_page_results

if __name__ == '__main__':
    func = google_scholar
    results_count = {}
    first_page_results = {}
    results_count[func.__name__], first_page_results[func.__name__] = func('Understanding Used Sailboat Prices')
    # print(bing('Understanding Used Sailboat Prices'))
    print(results_count, '\n', first_page_results)