import json
import random
import pymongo
import sys
import threading
import time
from bs4 import BeautifulSoup
from config import *
import requests

client = pymongo.MongoClient(DIANPING_URL,connect=False)
db=client[DIANPING_DB]

def save_to_mongo(result):
    if db[DIANPING_TABLE].insert(result):
        print('存储到MongoDB成功', result)
        return True
    return False


def get_type_list(file):
    file = open(file,encoding="utf-8")
    type_list =[]
    for line in file:
        type_list.append(line.strip())
    return type_list

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
        response = requests.get(url, headers=headers2,proxies = proxies, timeout=7)
        soup = BeautifulSoup(response.text, 'lxml')
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
                if txt.find("span", class_='comment-list'):
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
        if soup.find("div", class_="page"):
            page = soup.find("div", class_="page").find_all("a", class_="PageLink")[-1].get_text()
            lock.acquire()
            with open("page.txt", "a",encoding="utf-8") as file:
                print(url+"获取page成功，page数为："+page)
                file.write(url+","+page+ "\n")
                file.close()
            lock.release()

    except Exception as e:
        print(e)
        print(str(ip) + "不可用,剩余ip数：" + str(len(ip_list)))
        if ip_list == []:
            sys.exit()
        if ip in ip_list:
            ip_list.remove(ip)
        crawl(url, ip_list)
    else:
        print(str(ip) + "可用###剩余ip数：" + str(len(ip_list)) + "###网络状态：" + str(response.status_code))
        if response.status_code != 200:
            crawl(url, ip_list)

def get_ip_text(file):
    file = open(file)
    ip_list =[]
    for line in file:
        try:
            ip_list.append(json.loads(line.strip()))
        except:
            pass
    return ip_list

if __name__ == '__main__':
    lock = threading.Lock()
    IP_LIST = get_ip_text("ip_kuai.txt")
    url_list = get_type_list("url.txt")
    for url in url_list:
        t1 =threading.Thread(target=crawl,args=(url,IP_LIST))
        t1.start()
        time.sleep(1)
    # print(url_list)


