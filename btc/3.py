a = []
with open('ips.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        l = l.strip()
        _l = l.split('.')
        ip = _l[0] + '.' + _l[1] + '.' + _l[2]
        if ip not in a:
            a.append(ip)

for i in a:
    print(i)