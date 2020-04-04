# coding=utf-8
from bs4 import BeautifulSoup
import requests
import re
import random
from fake_useragent import UserAgent
import time
import os
import shutil


#链接课程网站
url = "https://mooc1-2.chaoxing.com/course/206199750.html"#这个课程是温铁军教授的十次危机，每个章节还有下级节点，不点开就不加载，用通用版本会落下很多视频


#伪装ua
fake_ua = UserAgent()
headers = {'User-Agent':fake_ua.random}
r = requests.get(url,headers = headers)

url_list1 = []
url_list2 = []
url_list = []

#搜索所有章节链接，并添加到列表中
soup = BeautifulSoup(r.text, 'html.parser')
for link in soup.find_all(href=re.compile("nodedetailcontroller")):
    course = link.get('href')
    url_list1.append('http://mooc1-2.chaoxing.com' + course)

for i in url_list1:
    headers = {'User-Agent': fake_ua.random}
    r = requests.get(i, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    for link in soup.find_all(href=re.compile("courseId")):
        course = link.get('href')
        url_list2.append('http://mooc1-2.chaoxing.com/nodedetailcontroller/visitnodedetail' + course)
    url_list = list(dict.fromkeys(url_list2))


data1 = []
for i in url_list:
    v_r = requests.get(i, headers=headers)
    v_soup = BeautifulSoup(v_r.text, 'html.parser')
    for dict in v_soup.find_all('iframe'):
        data = eval(dict.get('data'))
        if data.has_key('objectid') == True:
            data1.append(data['objectid'])
        else:
            continue

# 去重
data2 = list(set(data1))
data2.sort(key=data1.index)

# 创建保存视频的文件夹
save_dir = u'D:/十次危机'#保存路径
if os.path.exists(save_dir):
    shutil.rmtree(save_dir)#清空文件夹
os.mkdir(save_dir)

#开始下载
num = 1
for i in data2:
    print('正在下载第' + str(num) + '个视频')
    req = requests.get('http://d0.ananas.chaoxing.com/download/' + i, headers=headers)
    with open(save_dir + '/' + str(num) + '.' + '.mp4', "wb") as f:
        f.write(req.content)
    print('第' + str(num) + '个视频下载完成')
    time.sleep(5 + random.randint(1, 5))
    num = num + 1
