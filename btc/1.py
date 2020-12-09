import re

d = {}

with open('log-connect-2020-12-05 13 00 00- 2020-12-05 14 00 00.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        l = l.strip()
        searchObj = re.search(r'(.*) client connect, ip: (.*?)\t(.*)', l, re.M | re.I)
        if searchObj:
            ip = searchObj.group(2)
            if ip not in d.keys():
                d[ip] = 1
            else:
                d[ip] += 1


res = sorted(d.items(), key=lambda item:item[1])
for i in res:

    print(i[0] + ': ' + str(i[1]))

