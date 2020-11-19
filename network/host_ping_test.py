import subprocess as p
from multiprocessing.dummy import Pool as ThreadPool


def check_ip(ip):
    ip = ip.strip()
    w=p.Popen('ping -c 2 '+ip, shell=True, stdout=p.PIPE, stderr=p.PIPE)
    out, err = w.communicate()
    other_info = out.decode('utf-8')
    if 'ttl' in other_info or 'TTL' in other_info:
        pass
    else:
        print(ip,'is down')


with open('aliyun_ips_private.txt', 'r') as f:
    ips = f.readlines()
    try:
        pool = ThreadPool(30)
        pool.map(check_ip, ips)
        pool.close()
        pool.join()
    except Exception as e:
        print(e)
