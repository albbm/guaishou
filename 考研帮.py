import requests
import re
import time
import pymysql

def kaoyan51(page):
    Header={
        "User-Agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    }
    url="https://www.51kywang.com/51kaoyanwang/wap_doc/14654849_0_0_0.html?&style=1&pageNum="+str(page)
    response=requests.get(url)
    html=response.text
    pattern=re.compile('<a class="urlfont" href="(.*?)" >(.*?)</a>')
    items=re.findall(pattern,html)
    for item in items:
        print(item)
        bool=isexisturl(item[0])
        if bool==False:
            print("准备入库")
            sava_to_mysql("https://www.51kywang.com"+item[0], item[1])
            time.sleep(1)
        else:
             print('信息已存在')


def sava_to_mysql(url,title):
    inserttime=time.strftime("%Y-%m-%d %H:%M:%S")
    sql = 'insert into kaoyan51(url,title,time) values ("%s","%s","%s")' %(url,title,inserttime)
    count = cursor.execute(sql)
    db.commit()
def isexisturl(url):
    sql = 'select * from kaoyan51 where url = "%s"'%("https://www.51kywang.com"+url)
    count = cursor.execute(sql)
    db.commit()
    count=cursor.rowcount
    if count!=0:
        return True
    else:
        return False


while(True):
    db = pymysql.connect(host="", port=, user='', password='', database='',
                         charset='utf8')
    cursor = db.cursor()
    print('正在爬取考研屋....')
    for x in range(1, 20):
        kaoyan51(x)
    cursor.close()
    db.close()
    print('延迟一小时....')
    time.sleep(600)














