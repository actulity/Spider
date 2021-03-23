from sys import path
from threading import main_thread
import requests
from bs4 import BeautifulSoup
import random
import requests
from fake_useragent import UserAgent
from time import sleep
from utils import get_ips


# # fake userAgent
# ua = UserAgent()
# # ip pool
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
# #=============== test the ip =================
# # response = requests.get("http://httpbin.org/ip", proxies=proxy, headers={ "User-Agent":ua.random})
# # # response = requests.get("http://httpbin.org/ip", headers={ "User-Agent":ua.random})
# # print(response.text)


# job = ['数据挖掘', '图像算法工程师', 'java 后端', '互联网产品经理']
# dqs = {'北京':'101', '上海':'020', '广州':'050020', '深圳':'050090', '杭州':'070020', '武汉':'170020'}


# for page in range(1, 10):
#     sleep(1)
#     # 搜索关键字为“数据挖掘”，工作地区为北京的url，dps 为工作地区的参数，010 为猎聘网为北京地区指定的区域号
#     url="https://www.liepin.com/zhaopin/?key=数据挖掘&dqs=010&curPage=%s"%(str(page))
#     # 发起访问请求
#     proxy = {'http': random.choice(ip_pool)}
#     html = requests.get(url = url, proxies=proxy, headers={ "User-Agent":ua.random})
#     # 输出返回信息
#     print(html.url)
#     # 初始化soup 对象,page.text 为爬取到的带有html 标签页面
#     soup = BeautifulSoup(html.text,"html.parser")
#     # 找到<h3>标签，实质是获取所有包含职位名称及链接的标签内容
#     soup = soup.find_all("h3")
#     #在每个<h3>中进行抽取链接信息
#     with open('href.txt', 'a', encoding='utf-8') as f:
#         for i in soup:
#             #有些<h3>标签不包含求职信息，做简要判断
#             if i.has_attr("title"):
#                 #抽取链接内容
#                 href=i.find_all("a")[0]["href"]
#                 if('https://www.liepin.com' in href):
#                     f.write(href + '\n')
#                 else:
#                     f.write('https://www.liepin.com' + href + '\n')
#                 print(href)
#         f.flush()
        

def spider_href(job, citys, num_page):
    # fake userAgent
    ua = UserAgent()
    #ip pool
    ip_pool = get_ips()
    # save path
    out_path = './data/hrefs/href_%s.txt' % (job)
    # open file
    fp = open(out_path, 'w', encoding='utf-8')
    # spider the href
    for city in citys:
        for page in range(1, int(num_page / len(city))):
            # sleep(1)
            # 搜索关键字为“数据挖掘”，工作地区为北京的url，dps 为工作地区的参数，010 为猎聘网为北京地区指定的区域号
            url="https://www.liepin.com/zhaopin/?key=%s&dqs=%s&curPage=%s" % (job, citys[city], str(page))
            # 发起访问请求
            proxy = {'http': random.choice(ip_pool)}
            html = requests.get(url = url, proxies=proxy, headers={ "User-Agent":ua.random})
            # 输出返回信息
            print(html.url)
            # 初始化soup 对象,page.text 为爬取到的带有html 标签页面
            soup = BeautifulSoup(html.text,"html.parser")
            # 找到<h3>标签，实质是获取所有包含职位名称及链接的标签内容
            soup = soup.find_all("h3")
            #在每个<h3>中进行抽取链接信息
            # with open('href.txt', 'a', encoding='utf-8') as f:
            for i in soup:
                #有些<h3>标签不包含求职信息，做简要判断
                if i.has_attr("title"):
                    #抽取链接内容
                    href=i.find_all("a")[0]["href"]
                    if('https://www.liepin.com' in href):
                        fp.write(href + '\n')
                    else:
                        fp.write('https://www.liepin.com' + href + '\n')
                    print(href)
        fp.flush()
    fp.close()
    

if __name__ == "__main__":
    jobs = ['数据挖掘', '图像算法工程师', 'java后端', '互联网产品经理']
    dqs = {'北京':'101', '上海':'020', '广州':'050020', '深圳':'050090', '杭州':'070020', '武汉':'170020'}
    num_page = 10
    for job in jobs:
        spider_href(job, dqs, num_page)