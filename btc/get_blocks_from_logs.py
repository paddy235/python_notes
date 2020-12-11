import requests
from urllib.parse import quote
import re
import urllib3
import pymysql

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

db = pymysql.connect("10.193.208.159", "root", "Django12", "btc")
cursor = db.cursor()

keyword = 'BlockMakerBitcoin'
# keyword = 'bpool-btc-blkmaker* and submit*'

f = open(r'cookies.txt', 'r')
cookies = {}
for line in f.read().split(';'):
    name,value = line.strip().split('=',1)
    cookies[name] = value

headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    }

def get_report_pool_name(hash):
    try:
        res = requests.get('https://chain.api.btc.com/v3/block/' + hash, timeout=10, headers=headers, verify=False).json()
        report = res['data']['extras']['pool_name']
    except:
        report = 'error'

    return report


def save_info(time, hash, report, container, url):
    sql = "SELECT hash FROM btc_blocks where hash='%s'" % hash
    try:
       cursor.execute(sql)
       results = cursor.fetchall()
       if results:
           # print('existed')
            pass
       else:
           sql = "INSERT INTO btc_blocks(time, hash, report, container, success, log_url)" \
                 "VALUES ('%s', '%s',  '%s',  '%s',  '%s',  '%s')" % \
                    (time, hash, report, container, 'yes', url)
           try:
               cursor.execute(sql)
               db.commit()
           except Exception as e:
               print(e)

    except Exception as e:
       print (e)


def start(urls):
    for url in urls:
        try:
            res = requests.get(url, headers=headers, cookies=cookies).json()
            if res['rows']:
                for log in res['rows']:
                    if 'btc-blkmaker' not in log['content']:
                        continue
                    if '000000' not in log['content']:
                        continue

                    searchObj = re.search(r'_container_name_:(.*?)<br>(.*)', log['content'], re.M | re.I)
                    if searchObj:
                        container = searchObj.group(1)
                    else:
                        container = ''
                    content = log['content'].split(',')
                    hash = content[16].strip('"')
                    report = get_report_pool_name(hash)
                    time = content[22].split('"')[1]
                    print(time + ' ' + hash + ' ' + report + ' ' + container)
                    save_info(time, hash, report, container, url)
        except Exception as e:
            pass


for i in range(1, 31):
    start_time = '2020-12-%d 08:00:00' % i
    end_time = '2020-12-%d 08:00:00' % (i + 1)
    cycle = quote(start_time + '->' + end_time, 'utf-8')
    urls = [
        'https://cmis.bitmain.vip/get_logs/?rows=2000&page=1&logstore=config-operation-log&project=bpool-gymainland-bj-cluster&region=cn-beijing&account_id=1959593592593463&keyword=%s&cycle=%s' % (
        keyword, cycle),
        'https://cmis.bitmain.vip/get_logs/?rows=2000&page=1&logstore=config-operation-log&project=bpool-cloudpool-bj-cluster&region=cn-beijing&account_id=1959593592593463&keyword=%s&cycle=%s' % (
        keyword, cycle),
        'https://cmis.bitmain.vip/get_logs/?rows=2000&page=1&logstore=config-operation-log&project=k8s-log-bpool-bj-cluster&region=cn-beijing&account_id=1581108693131087&keyword=%s&cycle=%s' % (
        keyword, cycle),
        'https://cmis.bitmain.vip/get_logs/?rows=2000&page=1&logstore=config-operation-log&project=bpool-gymainland-hk-cluster&region=cn-hongkong&account_id=1959593592593463&keyword=%s&cycle=%s' % (
        keyword, cycle),
        'https://cmis.bitmain.vip/get_logs/?rows=2000&page=1&logstore=config-operation-log&project=k8s-log-custom-bpool-1902-va-aws-eks&region=us-east-1&account_id=1959593592593463&keyword=%s&cycle=%s' % (
        keyword, cycle),
        'https://cmis.bitmain.vip/get_logs/?rows=2000&page=1&logstore=container-stdout&project=k8s-log-custom-bpool-1902-va-aws-eks&region=us-east-1&account_id=1959593592593463&keyword=%s&cycle=%s' % (
        keyword, cycle),
        'https://cmis.bitmain.vip/get_logs/?rows=2000&page=1&logstore=config-operation-log&project=k8s-log-bpool-us-cluster&region=us-east-1&account_id=1581108693131087&keyword=%s&cycle=%s' % (
        keyword, cycle),
        'https://cmis.bitmain.vip/get_logs/?rows=2000&page=1&logstore=config-operation-log&project=bpool-gymainland-sz-cluster&region=cn-shenzhen&account_id=1959593592593463&keyword=%s&cycle=%s' % (
        keyword, cycle),
        'https://cmis.bitmain.vip/get_logs/?rows=2000&page=1&logstore=config-operation-log&project=bpool-cloudpool-sz-cluster&region=cn-shenzhen&account_id=1959593592593463&keyword=%s&cycle=%s' % (
        keyword, cycle),
        'https://cmis.bitmain.vip/get_logs/?rows=2000&page=1&logstore=config-operation-log&project=k8s-log-bpool-sz-cluster&region=cn-shenzhen&account_id=1581108693131087&keyword=%s&cycle=%s' % (
        keyword, cycle),
        'https://cmis.bitmain.vip/get_logs/?rows=2000&page=1&logstore=config-operation-log&project=k8s-log-custom-bpool-1902-eu-aws-eks&region=eu-central-1&account_id=1959593592593463&keyword=%s&cycle=%s' % (
        keyword, cycle),
        'https://cmis.bitmain.vip/get_logs/?rows=2000&page=1&logstore=container-stdout&project=k8s-log-custom-bpool-1902-eu-aws-eks&region=eu-central-1&account_id=1959593592593463&keyword=%s&cycle=%s' % (
        keyword, cycle),
        'https://cmis.bitmain.vip/get_logs/?rows=2000&page=1&logstore=config-operation-log&project=k8s-log-bpool-fra-cluster&region=eu-central-1&account_id=1581108693131087&keyword=%s&cycle=%s' % (
        keyword, cycle),
    ]

    start(urls)