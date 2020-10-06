import json
import requests
import urllib3

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

corpid = 'xxx'
secret = 'xxx'


class WeChatPub:
    s = requests.session()
    token = None

    def __init__(self):
        self.token = self.get_token(corpid, secret)

    def get_token(self, corpid, secret):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}".format(corpid, secret)
        rep = self.s.get(url, timeout=10, verify=False)
        if rep.status_code == 200:
            try:
                access_token = json.loads(rep.content.decode('utf-8'))['access_token']
                return access_token
            except Exception as e:
                print(e)
        else:
            print("request failed.")
            return None

    def send_msg(self, title, content):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser": "@all",
            "toparty": " PartyID1 | PartyID2 ",
            "totag": " TagID1 | TagID2 ",
            "msgtype": "textcard",
            "agentid": 1000002,
            "textcard": {
                "title": title,
                "description": content,
                "url": url,
            },
            "safe": 0
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        if rep.status_code == 200:
            return json.loads(rep.content.decode('utf-8'))
        else:
            print("request failed.")
            return None


wechat = WeChatPub()


if __name__ == '__main__':
    wechat = WeChatPub()
    try:
        wechat.send_msg(title="test", content="hello world!")
    except Exception as e:
        print(e)
