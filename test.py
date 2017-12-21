from config import *
import random
import requests
from bs4 import BeautifulSoup
import time

usa1= [
"Mozilla/5.0 (Linux; U; Android 4.1.1; ja-jp; Galaxy Nexus Build/JRO03H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 ,",
'Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9A334 Safari/7534.48.3 ',
'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9A405 Safari/7534.48.3 ',
'Mozilla/5.0 (iPod; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3 ',
'Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; da-dk) AppleWebKit/534.46.0 (KHTML, like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3'
]
usa_list=[]
with open("number.txt") as f:
    for line in f:
        usa_list.append(line.strip())
print(usa_list)

usa_list.extend(usa1)


user_agent =[]
for u in usa1:
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
                "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
                "Referer": "http://www.dianping.com/beijing/food",
                "User-Agent":u
                }
    cookies ={
        "_hc.v":"55a41e93-74c2-42ac-54db-244bcc764832.1513404921"
    }

    url = "http://www.dianping.com/search/category/2/10/g508r9157"
    # proxy = {"http":"http://10,119,134,15:80"}
    try:
        response = requests.get(url,headers=headers)
        print(response.text)

        time.sleep(2)
    except Exception as e:
        print(e)

    else:
        if response.status_code == 200:
            user_agent.append(u)
print(user_agent)
# soup = BeautifulSoup(response,'lxml')
# page =soup.find("div",class_="page").find_all("a",class_="PageLink")[-1].get_text()
# print(page)


usa =[
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14 ',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre ',
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729) ",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5 ",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/527 (KHTML, like Gecko, Safari/419.3) Arora/0.6 (Change: ) ",
    "Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 Firefox/14.0.1 ",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1 ",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) ",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0) ",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0) "]



usa1= [
'Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9A334 Safari/7534.48.3 ',
'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9A405 Safari/7534.48.3 ',
'Mozilla/5.0 (iPod; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3 ',
'Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; da-dk) AppleWebKit/534.46.0 (KHTML, like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3'
]



