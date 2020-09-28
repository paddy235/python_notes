
urls = []
with open('webapps.txt', 'r') as f:
    lines = f.readlines()
    for l in lines:
        l = l.strip('"')
        urls.append(l)

print(urls)