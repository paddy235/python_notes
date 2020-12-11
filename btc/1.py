"""
根据UTC时间统计6号爆块信息， 2020-12-06 08:00:00- 2020-12-07 08:00:00


"""
import re
import csv
import pymysql

db = pymysql.connect("10.193.208.159", "root", "Django12", "btc")
cursor = db.cursor()

logs = []
headers = ['时间', '块hash']

with open('7.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        l = l.strip()
        if '000000' not in l:
            continue
        # if 'ltc-blkmaker' in l:
        #     continue
        logs.append(l)
        # searchObj = re.search(r'(.*) client connect, ip: (.*?)\t(.*)', l, re.M | re.I)
        # if searchObj:
        #     ip = searchObj.group(2)
        #     if ip not in d.keys():
        #         d[ip] = 1
        #     else:
        #         d[ip] += 1


# with open('6_btc.log', 'a+') as f:
#     for log in logs:
#         f.write(log+'\n')
rows = []

for log in logs:
    # print('-' * 75)
    L = log.split(',')
    hash = L[16].strip('"')
    hash_time = L[22].split('"')[1]
    # sql = "SELECT * FROM btccom where hash='%s'" % hash
    # try:
    #     cursor.execute(sql)
    #     results = cursor.fetchall()
    #     if results:
    #         # print('existed')
    #         print(L)
    #     else:
    #         pass
    # except Exception as e:
    #     print(e)
    if 'btc-blkmaker' in log:
        rows.append((hash_time, hash))

print(rows)
with open('btc7.csv','w', newline='') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
