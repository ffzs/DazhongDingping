#-*-coding:utf-8-*-
import datetime
import re
import random
import threading
import time
import socket
import sys
from config import *
from YunDun import YunDun
import requests
from bs4 import BeautifulSoup
import pymongo
import json

client = pymongo.MongoClient(DIANPING_URL,connect=False)
db=client[DIANPING_DB]

def save_to_mongo(result):
    if db[DIANPING_TABLE].insert(result):
        print('存储到MongoDB成功', result)
        return True
    return False

def get_cookie():
    global headers
    test_url ="http://www.kuaidaili.com/free/intr/"
    html = requests.get(test_url,headers=headers).text
    oo = re.findall('no="", oo = (.*?);qo = "qo=', html)[0]
    ri = ''.join(re.findall('setTimeout\(\"\D+\((\d+)\)\"', html))
    a = html.split(";",2)[-1]
    b = re.sub("0xff", "", a)
    s = re.findall("\d+", b)
    cookie = {'_ydclearance':YunDun.get_cookie(0,ri,oo,s)}
    return cookie

def get_ip_kuai(page):
    headers = {
        'Referer': 'http://www.kuaidaili.com/free/intr/',
        'User-Agent': random.choice(USER_AGENTS)
    }
    cookies = get_cookie()
    ip_list=[]
    for page in range(1,page):
        print("-------获取第"+str(page)+"页ip--------")
        url = "http://www.kuaidaili.com/free/intr/"+str(page)+"/"
        response = requests.get(url,headers=headers,cookies=cookies).text
        # print(response)
        soup = BeautifulSoup(response,'lxml')
        all_tr = soup.find_all("tr")
        for tr in all_tr[1:]:
            ip = tr.find_all("td")[0].get_text()
            post = tr.find_all("td")[1].get_text()
            full_ip = {"http": ip+":"+post}
            # print(full_ip)
            ip_list.append(full_ip)
        time.sleep(random.choice(range(1, 3)))
    return ip_list

def get_ip_xila(page):
    headers3 = {
        'Referer': 'http://www.xicidaili.com/nt',
        'User-Agent': random.choice(USER_AGENTS)
    }
    ip_list=[]
    for page in range(1, page):
        print("-------获取第" + str(page) + "页ip--------")
        url = "http://www.xicidaili.com/nt/" + str(page)
        requset = requests.get(url=url, headers=headers3)  # ,proxies=json.loads(random.choice(ip_list))
        result_a = requset.text
        all_tr = BeautifulSoup(result_a, 'lxml').find_all('tr')[1:]
        for tr in all_tr:
            all_td = tr.find_all('td')
            ip = all_td[1].get_text()
            port = all_td[2].get_text()
            ip_type = all_td[5].get_text().lower()
            full_ip = {ip_type:(ip + ":" + port)}
            ip_list.append(full_ip)
        time.sleep(random.choice(range(2, 4)))
    return ip_list

def crawl(url, ip_list):
    global lock
    # socket.setdefaulttimeout(5)
    try:
        ip = random.choice(ip_list)
    except:
        return False
    else:
        proxies = ip
        usa = random.choice(USER_AGENTS)
        headers2 = {"Accept": "text/html,application/xhtml+xml,application/xml;",
                    'Cookie': '_lxsdk_cuid=1605e0182a1c8-0dcddc996964e2-5b452a1d-144000-1605e0182a1c8; _lxsdk=1605e0182a1c8-0dcddc996964e2-5b452a1d-144000-1605e0182a1c8; _hc.v=4fcafd03-8373-d150-6954-d7986b392b47.1513405645; s_ViewType=10; cy=2; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=16064b2eea8-a3f-e63-0fe%7C%7C30',
                    "Accept-Encoding": "gzip, deflate, sdch",
                    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
                    "Referer": "http://www.dianping.com/beijing/food",
                    "User-Agent": usa,
                    }
    try:
        response = requests.get(url, headers=headers2,proxies=proxies,timeout=5)
        html = response.text
        soup = BeautifulSoup(html, "lxml")
        all_txt = soup.find_all("div", class_="txt")
        for txt in all_txt:
            try:
                title = txt.find("h4").get_text()
                shop_url = txt.find("div", class_="tit").find("a")["href"]
                star = txt.find("div", class_="comment").find("span")["class"][1][7:]
                if txt.find("a", class_="review-num"):
                    review_num = txt.find("a", class_="review-num").find("b").get_text()
                else:
                    review_num = ""
                if txt.find("a", class_="mean-price").find("b"):
                    mean_price = txt.find("a", class_="mean-price").find("b").get_text()[1:]
                else:
                    mean_price = ""
                food_type = txt.find_all("span", class_="tag")[0].get_text()
                location = txt.find_all("span", class_="tag")[1].get_text()
                address = txt.find("span", class_="addr").get_text()
                if star != "0":
                    taste = txt.find("span", class_='comment-list').find_all("b")[0].get_text()
                    environment = txt.find("span", class_='comment-list').find_all("b")[1].get_text()
                    service = txt.find("span", class_='comment-list').find_all("b")[2].get_text()
                else:
                    taste, environment, service = "", "", ""
                total = {
                    "标题": title,
                    "网址": shop_url,
                    "星级": star,
                    "评论人数": review_num,
                    "人均消费": mean_price,
                    "品类": food_type,
                    "区位": location,
                    "地址": address,
                    "口味": taste,
                    "环境": environment,
                    "服务": service,
                }
                lock.acquire()
                save_to_mongo(total)
                with open("dz_.txt", "a") as file:
                    file.write(json.dumps(ip) + "\n")
                    file.close()
                lock.release()
            except Exception as e:
                print(e)
                pass

    except Exception:
        print(str(ip)+"不可用,剩余ip数："+str(len(ip_list)))
        if ip_list == []:
            sys.exit()
        if ip in ip_list:
            ip_list.remove(ip)
        # if len(ip_list) <= 10 :
        #     ip_list = get_ip_text("dz_ip.txt")
        crawl(url, ip_list)
    else:
        print(str(ip) + "可用###剩余ip数：" + str(len(ip_list)) + "###网络状态：" + str(response.status_code))
        print(usa)
        if response.status_code==403:
            crawl(url, ip_list)
            # pass
            # if ip in ip_list:
            #     ip_list.remove(ip)


def get_type_list(file):
    file = open(file,encoding="utf-8")
    type_list =[]
    for line in file:
        type_list.append(line.strip().split(":")[-1])
    return type_list

def get_ip_text(file):
    file = open(file)
    ip_list =[]
    for line in file:
        try:
            ip_list.append(json.loads(line.strip()))
        except:
            pass
    return ip_list

def get_page(url):
    headers = {
                'Cookie': '_lxsdk_cuid=1605e0182a1c8-0dcddc996964e2-5b452a1d-144000-1605e0182a1c8; _lxsdk=1605e0182a1c8-0dcddc996964e2-5b452a1d-144000-1605e0182a1c8; _hc.v=4fcafd03-8373-d150-6954-d7986b392b47.1513405645; s_ViewType=10; cy=2; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=16064b2eea8-a3f-e63-0fe%7C%7C30',
                "Referer": "http://www.dianping.com/beijing/food",
                "User-Agent":'Opera/9.25 (Windows NT 6.0; U; en)' ,
                }
    time.sleep(2)
    try:
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, 'lxml')
        page = soup.find("div", class_="page").find_all("a", class_="PageLink")[-1].get_text()
        return page
    except:
        return False

if __name__ == '__main__':
    lock = threading.Lock()
    IP_LIST =get_ip_text("dz_dianping.txt")
    type_list = get_type_list("dianping_meishi.txt")
    local_list = get_type_list("meishi.txt")
    # type_list = list(reversed(type_list))
    # print(local_list)
    for type in type_list:
        for local in local_list:
            url_a = "http:" + type +"r"+local
            page = get_page(url_a)
            if page:
                print(page)
                for page in range(1, int(page)+1):
                    url = "http:" + type +"r"+local+"o2p" + str(page)
                    crawl(url,IP_LIST)
                    # t1 = threading.Thread(target=crawl, args=(url, IP_LIST))
                    # t1.start()
                    # time.sleep(0.1)
    # for i in range(1,1000):
    #     t1 = threading.Thread(target=test_ip, args=(i, IP_LIST))
    #     t1.start()
    #     time.sleep(1)




