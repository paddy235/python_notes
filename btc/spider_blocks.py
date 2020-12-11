import requests
import urllib3
from bs4 import BeautifulSoup
import pymysql

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    }


db = pymysql.connect("10.193.208.159", "root", "Django12", "btc")
cursor = db.cursor()


def get_report_pool_name(hash):
    try:
        res = requests.get('https://chain.api.btc.com/v3/block/' + hash, timeout=10, headers=headers, verify=False).json()
        report = res['data']['extras']['pool_name']
    except:
        report = 'error'

    return report


def save_info(height, number, size, earnings, time, hash, difficulty, report):
    sql = "SELECT height FROM btccom where height=%s" % height
    try:
       cursor.execute(sql)
       results = cursor.fetchall()
       if results:
           # print('existed')
            pass
       else:
           sql = "INSERT INTO btccom(height, number, size, earnings, time, hash, difficulty, report)" \
                 "VALUES ('%s', '%s',  '%s',  '%s',  '%s',  '%s',  '%s', '%s')" % \
                    (height, number, size, earnings, time, hash, difficulty, report)
           try:
               cursor.execute(sql)
               db.commit()
           except Exception as e:
               print(e)

    except Exception as e:
       print (e)


def get_info(i):
    url = 'https://btc.com/stats/pool/BTC.com?page=' + str(i)
    # print(url)
    res = requests.get(url, timeout=10, headers=headers, verify=False).content
    soup = BeautifulSoup(res, "html5lib")
    div = soup.find('div', class_="pool-blockList")
    for tr in div.find_all('tr'):
        try:
            tds = tr.find_all('td')
            height = tds[0].text.replace(',', '')
            # print('高度:', height)

            number = tds[1].text.replace(',', '')
            # print('数量:', number)

            size = tds[2].text.replace(',', '')
            # print('大小:', size)

            earnings = tds[3].text.strip()
            # print('块收益:', earnings)

            time = tds[4].text.strip()
            # print('时间:', time)

            hash = tds[5].text.strip()
            print('块哈希:', hash)
            report = get_report_pool_name(hash)

            difficulty = tds[6].text.strip().replace('\n', '').replace(' ', '')
            # print('难度:', difficulty)

            save_info(height, number, size, earnings, time, hash, difficulty, report)
            # print('-' * 75)

        except:
            pass




for i in range(1, 100):
    try:
        get_info(i)
    except Exception as e:
        print(e)

db.close()


