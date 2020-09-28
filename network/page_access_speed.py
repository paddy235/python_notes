"""
需求分析：业务部门反馈某个站点有时访问比较慢，因此写个简单脚本监测一段时间，监测结果记录在日志文件中。
运行环境：python3
依赖库第三方库： request
GitHub链接：https://github.com/dandh811/python_notes/blob/master/network/page_access_speed.py
"""

import requests
import logging
import time

url = 'https://www.xxx.com'  # 监测域名
logging.basicConfig(level=logging.INFO, filename='access.log', filemode='a')  # 配置日志

while True:
    r = requests.get(url)
    ct = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    t = r.elapsed.total_seconds()
    if t > 1:
        mes = str(ct) + " --- " + str(t)
        print(mes)
        logging.info(mes)
        time.sleep(10)