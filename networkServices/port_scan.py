import socket
import time
from multiprocessing.dummy import Pool as ThreadPool


def start(i):
    ips = ['10.192.28.2', '172.16.1.135', '10.193.210.100', '10.40.24.1', '10.40.25.2', '10.40.0.31', '10.40.3.32',
           '10.211.0.126', '10.211.0.11', '10.211.1.11']
    for ip in ips:
        try:
            # print(ip, i)
            sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sk.settimeout(3)
            sk.connect((ip, i))
            print(ip, i, " port is ok")
            sk.close()
        except Exception as e:
            # print(e)
            pass
try:

    pool = ThreadPool(30)
    ips2 = pool.map(start, list(range(1, 65536)))

    pool.close()
    pool.join()
except Exception as e:
    print(e)


