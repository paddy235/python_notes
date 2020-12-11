import pymysql
import numpy as np
# import matplotlib.pyplot as plt
import csv

db = pymysql.connect("10.193.208.159", "root", "Django12", "btc")
cursor = db.cursor()
dict = {}
dates = []

sql = "SELECT time FROM btccom"
cursor.execute(sql)
results = cursor.fetchall()
for t in results:
    t = str(t[0]).split(' ')[0]
    if t not in dates:
        dates.append(t)

dates.reverse()

for d in dates:
    sql = "SELECT time FROM btccom where time like '%s%%'" % (d)
    cursor.execute(sql)
    results = cursor.fetchall()
    # print(d + ': ' + str(len(results)))
    dict[d] = len(results)

# dict = {"a": 1, "b": 5, "c": 3}
with open('btc.csv', 'a+', newline='') as f:
    for k, v in dict.items():
        csv_write = csv.writer(f)
        data_row = [k, v]
        csv_write.writerow(data_row)

# colors = list("rgbcmyk")
#
# x = dict.keys()
# y = dict.values()
# plt.plot(x, y, color=colors.pop())
#
# # plt.legend(d.keys())
# plt.show()