# ***********************************************
# @Time    : 2019/8/27 11:50
# @Author  : dandh811
# @Blog    ：https://www.xiuxing128.top
# ***********************************************

import requests
import datetime
import ssl
import json
from kafka import KafkaConsumer

# sasl_mechanism = 'PLAIN'
#security_protocol = 'SSL'
#
context = ssl.create_default_context()
context.options &= ssl.OPENSSL_VERSION_NUMBER


ssl_certfile = "kafka_client_ssl/certificate.pem"
ssl_cafile = "kafka_client_ssl/CARoot.pem"
ssl_keyfile = "kafka_client_ssl/key.pem"

consumer = KafkaConsumer('kbunting',
                         group_id='test-consumer-group',
                         bootstrap_servers=['ip-10-10-0-210:8000'],
                         api_version=(0, 10),
                         ssl_check_hostname=False,
                         ssl_certfile=ssl_certfile,
                         security_protocol="SSL",
                         ssl_cafile=ssl_cafile,
                         ssl_keyfile=ssl_keyfile)

for message in consumer:
    print('[+] ' + str(datetime.datetime.now()) + 'get message:')
    print()
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    asset_data = message.value.decode('utf-8')
    asset_data = json.loads(asset_data)
    print(asset_data)
    user_token = asset_data.get("user_token")
    if user_token is None:
        print("Cannot get the user_token")
        continue

    data = json.dumps(asset_data)
    headers = {"Authorization": "TOKEN " + user_token, "Content-Type": "application/json"}
    report_target = "https://%s%s" % ('sec..com/', '/api/v1/report/')

    try:
        response = requests.post(report_target, data=data, headers=headers, verify=False)
        if response.status_code == requests.codes.ok:
            print("Report response: %s" % response)
        else:
            print('Report response error: %s' % response)
    except Exception as e:
        print("Failed to report data:")
        print(e)


def test():
    pass


test()