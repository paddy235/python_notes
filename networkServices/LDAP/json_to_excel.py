"""
标题：利用python提取json文件的关键字段，写入excel中
需求分析：由于json文件的可读性比较差，因此利用python处理json文件，提取文件中关心的几个字段，并写入excel表格中。
运行环境：python3 + Windows或者Linux
依赖库第三方库： xlwt
GitHub链接：https://github.com/dandh811/python_notes/blob/master/networkServices/LDAP/json_to_excel.py
备注：脚本中的字段名称或者其他参数需要根据自己的场景做相应修改。
"""

import json
import xlwt


def read_json_file(file):
    with open(file, 'r', encoding='utf8') as fr:
        data = json.load(fr)                                    # 用json中的load方法，将json串转换成字典
    return data


def write_to_excel():
    a = read_json_file('users.json')
    title = ["序号", "姓名", "部门", "邮箱", "手机"]
    book = xlwt.Workbook()                                      # 创建一个excel对象
    sheet = book.add_sheet('Sheet1',cell_overwrite_ok=True)     # 添加一个sheet页
    for i in range(len(title)):                                 # 循环列
        sheet.write(0,i,title[i])                               # 将title数组中的字段写入到0行i列中
    count = 0
    for line in a:                                              # 循环字典
        if 'name' in line['attributes']:
            name = line["attributes"]["name"]
        else:
            continue
        if 'telephoneNumber' in line['attributes']:
            phone = line["attributes"]["telephoneNumber"]
        else:
            phone = "NA"
        if 'mail' in line['attributes']:
            email = line["attributes"]["mail"]
        else:
            email = "NA"
        if 'department' in line['attributes']:
            dep = line["attributes"]["department"]
        else:
            dep = "NA"
        if 'sAMAccountName' in line['attributes']:
            domainname = line["attributes"]["sAMAccountName"]
        else:
            domainname = "NA"
        count = count + 1
        sheet.write(count,1,name)                               # 将line写入到第int(line)行，第0列中
        sheet.write(count, 2, domainname)
        sheet.write(count, 3, phone)
        sheet.write(count, 4, email)
        sheet.write(count, 5, dep)

    book.save('demo2.xls')


if __name__ == '__main__':
    write_to_excel()
