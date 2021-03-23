#@Readme : IP代理==模拟一个ip地址去访问某个网站（爬的次数太多，ip被屏蔽）

# 多线程的方式构造ip代理池。
from time import sleep
from bs4 import BeautifulSoup
import requests
from urllib import request, error
import threading
import os
from fake_useragent import UserAgent

inPath = "./data/proxies/proxy.txt"
inPath = "./data/proxies/verified.txt"
inFile = open('proxy.txt')           # 存放爬虫下来的ip
verifiedtxt = open('verified.txt')   # 存放已证实的可用的ip

lock = threading.Lock()

def getProxy_89free():
    # 打开我们创建的txt文件
    proxyFile = open('proxy.txt', 'a', encodign='utf-8')
    # 伪装
    ua = UserAgent()
    # page是我们需要获取多少页的ip，这里我们获取到第x页
    for page in range(1, 35):
        sleep(2)
        # 通过观察URL，我们发现原网址+页码就是我们需要的网址了，这里的page需要转换成str类型
        # urls = url + str(page)
        urls = 'https://www.89ip.cn/index_'+ str(page) + '/1.html'
        # 伪装
        headers = {
            'User-Agent': ua.random
        }
        # 通过requests来获取网页源码
        rsp = requests.get(urls, headers=headers)
        html = rsp.text
        # 通过BeautifulSoup，来解析html页面
        soup = BeautifulSoup(html,'html.parser')
        # 通过分析我们发现数据在　id为ip_list的table标签中的tr标签中
        trs = soup.find('table', class_="layui-table").find("tbody").find_all('tr')   # 这里获得的是一个list列表
        
        # trs = soup.find('table').find_all('tr')  # 这里获得的是一个list列表
        # 我们循环这个列表
        for item in trs:
            # 并至少出每个tr中的所有td标签
            tds = item.find_all('td')
            # 我们会发现有些img标签里面是空的，所以这里我们需要加一个判断
            # locate = '未知'
            if tds[2] is None:
                locate = '未知'
            else:
                locate = tds[2].text.strip()
            # 通过td列表里面的数据，我们分别把它们提取出来
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            coorperation = tds[3].text.strip()
            # protocol = tds[4].text.strip()
            # speed = tds[5].text.strip()
            time = tds[4].text.strip()
            # 将获取到的数据按照规定格式写入txt文本中，这样方便我们获取
            proxyFile.write('%s|%s|%s|%s|%s\n' % (locate, ip, port, coorperation, time))
    proxyFile.flush()


def getProxy_66ip(url):
    # 打开我们创建的txt文件
    proxyFile = open('proxy.txt', 'a',encodign='utf-8')
    # 伪装
    ua = UserAgent()
    # page是我们需要获取多少页的ip，这里我们获取到第x页
    for page in range(1, 35):
        sleep(2)
        # 通过观察URL，我们发现原网址+页码就是我们需要的网址了，这里的page需要转换成str类型
        # urls = url + str(page)
        urls = 'http://www.66ip.cn/areaindex_'+ str(page) + '/1.html'
        # 伪装
        headers = {
            'User-Agent': ua.random
        }
        # 通过requests来获取网页源码
        rsp = requests.get(urls, headers=headers)
        html = rsp.text
        # 通过BeautifulSoup，来解析html页面
        soup = BeautifulSoup(html,'html.parser')
        # 通过分析我们发现数据在　id为ip_list的table标签中的tr标签中
        trs = soup.find(id='main', class_='container').find("table").find_all('tr')   # 这里获得的是一个list列表
        # trs = soup.find('table').find_all('tr')  # 这里获得的是一个list列表
        # 我们循环这个列表
        for item in trs[2:]:
            # 并至少出每个tr中的所有td标签
            tds = item.find_all('td')
            # 我们会发现有些img标签里面是空的，所以这里我们需要加一个判断
            locate = '未知'
            # if tds[2] is None:
                # locate = '未知'
            # else:
                # locate = tds[4].text.strip()
            # 通过td列表里面的数据，我们分别把它们提取出来
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            anony = tds[3].text.strip()
            # protocol = tds[4].text.strip()
            # speed = tds[5].text.strip()
            time = tds[4].text.strip()
            # 将获取到的数据按照规定格式写入txt文本中，这样方便我们获取
            proxyFile.write('%s|%s|%s\n' % (locate, ip, port))
            # proxyFile.write('%s|%s|%s|%s|%s\n' % (locate, ip, port, anony, time))
            proxyFile.flush()

def verifyProxyList():
    verifiedFile = open('verified.txt', 'a')
    while True:
        lock.acquire()
        ll = inFile.readline().strip()
        lock.release()
        if len(ll) == 0: break
        line = ll.strip().split('|')
        ip = line[1]
        port = line[2]
        realip = ip + ':' + port
        code = verifyProxy(realip)
        if code == 200:
            lock.acquire()
            print("---Success成功:" + ip + ":" + port)
            verifiedFile.write(ll + "\n")
            verifiedFile.flush()
            lock.release()
        else:
            print("---Failure失败:" + ip + ":" + port)


def verifyProxy(ip):
    '''
    验证代理的有效性
    '''
    ua = UserAgent()
    requestHeader = {
        'User-Agent': ua.random
    }
    url = "http://www.baidu.com"
    # 填写代理地址
    proxy = {'http': ip}
    # 创建proxyHandler
    proxy_handler = request.ProxyHandler(proxy)
    # 创建opener
    proxy_opener = request.build_opener(proxy_handler)
    # 安装opener
    request.install_opener(proxy_opener)

    try:
        req = request.Request(url, headers=requestHeader)
        rsq = request.urlopen(req, timeout=5.0)
        code = rsq.getcode()
        rsq.close()
        return code
    except :
        return 0


if __name__ == '__main__':
    # 手动新建两个文件
    filename = 'proxy.txt'
    filename2 = 'verified.txt'
    if not os.path.isfile(filename):
        inFile = open(filename, mode="w", encoding="utf-8")
    if not os.path.isfile(filename2):
        verifiedtxt = open(filename2, mode="w", encoding="utf-8")
    tmp = open('proxy.txt', 'w')
    tmp.write("")
    tmp.close()
    tmp1 = open('verified.txt', 'w')
    tmp1.write("")
    tmp1.close()
    # 多线程爬虫西刺代理网，找可用ip
    # getProxy_66ip()
    getProxy_89free()
    # getProxy("http://www.66ip.cn/areaindex_2/1.html")
    # getProxy("http://www.66ip.cn/areaindex_3/1.html")
    # getProxy("http://www.66ip.cn/areaindex_4/1.html")

    all_thread = []
    for i in range(30):
        t = threading.Thread(target=verifyProxyList)
        all_thread.append(t)
        t.start()

    for t in all_thread:
        t.join()

    inFile.close()
    verifiedtxt.close()  
    
    # ============== 对ip去重 ===============
    ips = set()
    with open('verified.txt', 'r', encoding='utf=8') as f:
        while True:
            line = f.readline().strip()
            if not line: break
            ips.add(line)
            
    with open('verified.txt', 'w', encoding='utf=8') as f:
        for ip in ips:
            f.write(ip + '\n')
        f.flush()
