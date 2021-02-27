import datetime

import requests
import  json
import re
import time
import pymysql



def xiaomuchong(page):
    Header={
        "User-Agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    }
    url="http://muchong.com/bbs/kaoyan.php?&page="+str(page)
    response=requests.get(url)
    html=response.text
    pattern=re.compile('<tr>\s*<td class=".*?">\s*<a href="(.*?)" target="_blank" class=".*?">(.*?)</a>\s*</td>\s*<td>.*?</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>')
    '''<li><span class="span-time">(.*?)</span>\s*<a target="_blank" href="(.*?)">(.*?)</a>'''
    items=re.findall(pattern,html)
    for item in items:
        print(item)
        bool=isexistmysql(item[4])
        if bool==False:
            print("准备入库")
            sava_to_mysql(item[0], item[1], item[2], item[3], item[4])
            time.sleep(1)
        else:
             print('信息已存在')

def kaoyanwu():
    Header={
        "User-Agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    }
    url="http://tiaoji.kaoyan.com/xinxi/"
    response=requests.get(url)
    response.encoding = 'utf-8'
    html=response.text
    pattern=re.compile('<li><em>(.*?)</em><a href="(.*?)" title="(.*?) target="_blank">.*?</a></li>')
    items=re.findall(pattern,html)
    for item in items:
        print(item)
        bool=isexisttitle(item[1])
        if bool==False:
            print("准备入库")
            sql = 'insert into tiaoji(url,title,time) values ("%s","%s","%s")'
            dt = "2020-02-17 18:51:29"
            print(dt)
            count = cursor.execute(sql, (item[1], item[2], dt))
            db.commit()
            time.sleep(1)
        else:
             print('信息已存在')
def sava_to_mysql(url,title,type,mums,time):
    sql = 'insert into tiaoji(url,title,type,nums,time) values ("%s","%s","%s","%s","%s")' %(url,title,type,mums,time)
    count = cursor.execute(sql)
    db.commit()

def isexistmysql(time):
    sql = 'select * from tiaoji where time = "%s"'%(time)
    count = cursor.execute(sql)
    db.commit()
    count=cursor.rowcount
    if count!=0:
        return True
    else:
        return False
def isexisttitle(url):
    sql = 'select * from tiaoji where url = "%s"'%(url)
    count = cursor.execute(sql)
    db.commit()
    count=cursor.rowcount
    if count!=0:
        return True
    else:
        return False

while(True):
    db = pymysql.connect(host="", port=3306, user='', password='', database='',
                         charset='utf8')
    cursor = db.cursor()
    for i in range(1,20):
        xiaomuchong(i)
    cursor.close()
    db.close()
    print('延迟一小时....')












