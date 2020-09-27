import sys
import subprocess


char_set = ['\\', '|', '/', '-']
count = 0


def print_msg(msg=None, left_align=True, line_feed=False):
    if left_align:
        sys.stdout.write('\r' + msg)
    else:
        # 右对齐
        sys.stdout.write('\r' + ' ' * (78 - len(msg)) + msg)
    if line_feed:
        sys.stdout.write('\n')

    sys.stdout.flush()


def check_alive(city, domain):
    print_msg('[%s] 测试 %s' % (char_set[count % 4], city))
    ping = subprocess.Popen('ping -c 4' + ' ' + domain,
                            shell=True,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)  # 执行命令
    res, err = ping.communicate()
    if err:
        print(err)
        # sys.exit(err.decode().strip('\n'))

    pres = list(res.decode().split('\n'))
    try:
        loss = pres[-3].split()[5]  # 获取丢包率
    except Exception as e:
        print(e)
    try:
        rtt = pres[-2].split('/')[4]  # 获取rtt avg值
        return rtt
    except Exception as e:
        print(e)

cities = [
    {'(Asia)Tokyo, Japan[日本 东京]': 'hnd-jp-ping.vultr.com'},
    {'Singapore[新加坡]': 'sgp-ping.vultr.com'},
    {'(AU) Sydney, Australia[悉尼]': 'syd-au-ping.vultr.com'},
    {'(EU) Frankfurt, DE[德国 法兰克福]': 'fra-de-ping.vultr.com'},
    {'(EU) Amsterdam, NL[荷兰 阿姆斯特丹]': 'ams-nl-ping.vultr.com'},
    {'(EU) London, UK[英国 伦敦]': 'lon-gb-ping.vultr.com'},
    {'(EU) Paris, France[法国 巴黎]': 'par-fr-ping.vultr.com'},
    {'Seattle, Washington[美东 华盛顿州 西雅图]': 'wa-us-ping.vultr.com'},
    {'Silicon Valley, Ca[美西 加州 硅谷]': 'sjo-ca-us-ping.vultr.com'},
    {'Los Angeles, Ca[美西 加州 洛杉矶]': 'lax-ca-us-ping.vultr.com'},
    {'Chicago, Illinois[美东 芝加哥]': 'il-us-ping.vultr.com'},
    {'Dallas, Texas[美中 德克萨斯州 达拉斯]': 'tx-us-ping.vultr.com'},
    {'New York / New Jersey[美东 新泽西]': 'nj-us-ping.vultr.com'},
    {'Atlanta, Georgiaa[美东 乔治亚州 亚特兰大]': 'ga-us-ping.vultr.com'},
    {'Miami, Florida[美东 佛罗里达州 迈阿密]': 'fl-us-ping.vultr.com'},
]


D = {'city': 'city', 'rtt': '9999999'}
for city in cities:

    for k, v in city.items():
        rtt = check_alive(k, v)
        count += 1
        if rtt < D['rtt']:
            D['city'] = k
            D['rtt'] = rtt

print('[+] 测试完毕，最优选择城市：%s，延时 %s ms' % (D['city'], D['rtt']))

def test():  # "><img src=1 onerror=alert(9)>
    pass


test()