from datetime import datetime, timedelta

now_time = datetime.strftime('2020-12-06 00:08:00', "%Y-%m-%d %H:%M:%SZ")

utc_time = now_time - timedelta(hours=8)  # UTC只是比北京时间提前了8个小时

utc_time = utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")  # 转换成Aliyun要求的传参格式...

print(utc_time)