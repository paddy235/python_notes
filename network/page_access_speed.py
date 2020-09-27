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