import requests
import urllib3

urllib3.disable_warnings()

headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        }

urls = []
with open('webapps.txt', 'r') as f:
    lines = f.readlines()
    for l in lines:
        l = l.strip().strip('"')
        urls.append(l)

for url in urls:
    url2 = url + "/'"
    try:
        r2 = requests.get(url2, headers=headers, timeout=10, verify=False, allow_redirects=False)
        if r2.status_code in [404, 301, 302]:
            continue
        else:


            rl2 = len(r2.text)
            try:
                r = requests.get(url, headers=headers, timeout=10, verify=False, allow_redirects=False)
                rl = len(r.text)
            except:
                rl = 0
            if rl == rl2:
                continue
            print('-' * 75)
            print(url2)
            print(r2.status_code)
    except:
        pass
