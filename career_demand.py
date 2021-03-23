from logging import info
from time import sleep
import random
from bs4 import BeautifulSoup
import requests
from urllib import request, error
import threading
import os
from fake_useragent import UserAgent
import utils

# ip pool
# ip_pool = []
# with open("verified.txt", "r") as f:
#     while True:
#         ll = f.readline()
#         if not ll: break
#         line = ll.strip().split('|')
#         ip = line[1]
#         port = line[2]
#         realip = ip + ':' + port
#         ip_pool.append(realip)
ip_pool = utils.get_ips()

hrefs = []
with open("href.txt", "r", encoding='utf-8') as f:
    while True:
        ll = f.readline()
        if not ll: break
        line = ll.strip()
        hrefs.append(line)

# 伪装
ua = UserAgent()
# page是我们需要获取多少页的ip，这里我们获取到第x页
# 打开我们创建的txt文件
demand = open('demand.txt', 'w', encoding='utf-8')
error = 0
for url in hrefs:
    sleep(1)
    # 伪装
    # 通过requests来获取网页源码
    proxy = {'http': random.choice(ip_pool)}
    rsp = requests.get(url, proxies = proxy, headers = { 'User-Agent': ua.random })
    html = rsp.text
    # 通过BeautifulSoup，来解析html页面
    soup = BeautifulSoup(html,'html.parser')
    # 通过分析我们发现数据在　id为ip_list的table标签中的tr标签中
    try:
        trs = soup.find(class_="job-item main-message job-description").find_all(class_='content content-word')
            # 我们循环这个列表
        for item in trs:
            # 并至少出每个tr中的所有td标签
            # print(item)
            # item.replace('<br>','').replace('<br/>','')
            info = item.text.strip()
            print(info)
            demand.write('%s\n' % (info))
            # proxyFile.write('%s|%s|%s|%s|%s\n' % (locate, ip, port, anony, time))
        demand.flush()
    except:
        error += 1
demand.close()
print(error)    