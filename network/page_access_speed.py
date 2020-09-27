"""
需求分析：与LDAP服务器建立连接，查询公司所有的员工信息和部门信息，并将结果保存在2个json文件中。
运行环境：python3 + Windows或者Linux
依赖库第三方库： ldap3
GitHub链接：https://github.com/dandh811/python_notes/blob/master/networkServices/LDAP/ldap_tool.py
"""
import requests
import logging
import time

url = 'https://songjing.vip'
logging.basicConfig(level=logging.INFO,
                    filename='access.log',
                    filemode='a',
                    )


while True:
    r = requests.get(url)
    ct = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    t = r.elapsed.total_seconds()
    if t > 1:
        mes = str(ct) + " --- " + str(t)
        print(mes)
        logging.info(mes)
        time.sleep(10)