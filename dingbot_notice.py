# -*- coding: utf-8 -*-
import sys
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json
import time

# --------------------- #
# 日期：2023/8/29
# 作者：陈某
# 功能：钉钉告警通知
# --------------------- #

###
# 钉钉机器人信息
# access_token
api_url = ''
# 加签
api_secret = ''

###
# 获取当前时间戳，sign值
def get_timestamp_sign():
    timestamp = str(round(time.time() * 1000))
    secret = api_secret
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign

###
# 获取加签后的链接
def get_signed_url():
    timestamp, sign = get_timestamp_sign()
    webhook = api_url + "&timestamp=" + timestamp + "&sign=" + sign
    return webhook

###
# 定义消息模式
def get_webhook(mode):
    if mode == 0:  # only 关键字
        webhook = api_url
    elif mode == 1 or mode == 2:  # 关键字和加签 或 # 关键字+加签+ip
        webhook = get_signed_url()
    else:
        webhook = ""
        print("error! mode:   ", mode, "  webhook :  ", webhook)
    return webhook

### 获取信息内容
def get_message(text, user_info):
    # 和类型相对应，具体可以看文档 ：https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
    message = {
        "msgtype": "text",
        "text": {
            "content": text
        },
        "at": {
            "atMobiles": [
                user_info,
            ],
            "isAtAll": False
        }
    }
    return message

def send_ding_message(text, user_info):
    # 请求的URL，WebHook地址
    # 主要模式有 0 ： 关键字 1：# 关键字 +加签 3：关键字+加签+IP
    webhook = get_webhook(1)
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    message = get_message(text, user_info)
    message_json = json.dumps(message)
    info = requests.post(url=webhook, data=message_json, headers=header).json()
    code = info["errcode"]
    errmsg = info["errmsg"]

if __name__ == "__main__":
    text = sys.argv[1]	# 通过命令行传递参数
	# text = '测试'
    user_info = '手机号码'
    send_ding_message(text, user_info)
