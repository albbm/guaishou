import requests
import re
import time
import pymysql

def kaoyan51(page):
    Header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    url="http://www.chinakaoyan.com/tiaoji/schoollist/pagenum/"+str(page)+".shtml"
    response=requests.get(url=url,headers=Header)
    html=response.text
    pattern=re.compile('\s*<span class="school">(.*?)</span>\s*<span class="name">(.*?)</span>\s*<span\s*class="title"><a href="(.*?)" title=.*? target="_blank">.*?</a></span>\s*<span class="time">(.*?)</span>')
    items=re.findall(pattern,html)
    for item in items:
        print(item)
        bool=isexisturl("http://www.chinakaoyan.com/"+item[2])
        if bool==False:
            print("准备入库")
            sava_to_mysql("http://www.chinakaoyan.com/"+item[2], item[0],item[1],item[3])
        else:
             print('信息已存在')
def sava_to_mysql(url,school,title,time):
    sql = 'insert into Chinakaoyan(url,school,title,time) values ("%s","%s","%s","%s")' %(url,school,title,time)
    count = cursor.execute(sql)
    db.commit()
def isexisturl(url):
    sql = 'select * from Chinakaoyan where url = "%s"'%(url)
    print(sql)
    count = cursor.execute(sql)
    db.commit()
    count=cursor.rowcount
    print(count)
    if count!=0:
        return True
    else:
        return False

while  True:

    db = pymysql.connect(host="", port=3306, user='', password='', database='',charset='utf8')
    cursor = db.cursor()
    for x in range(1, 20):
       kaoyan51(x)
    cursor.close()
    db.close()
    print('延迟一小时....')
    time.sleep(600)














