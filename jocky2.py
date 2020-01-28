import json
from flask import Flask, request 
import requests
import time
import urllib

f_open = open('token.txt','r')
TOKEN = f_open.read()
print (TOKEN)

MAIN_URL = "https://api.telegram.org/bot{}/".format(TOKEN)
url = MAIN_URL

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json(url):
    js = json.loads(get_url(url))
    return js


def get_updates(offset = None):
    url = MAIN_URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json(url)
    return js

def get_last_updateid(update):
    update_ids = []
    for i in update:
        update_ids.append(i['update_id'])
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id):
    # print (chat_id)
    # print (text)
    text = urllib.parse.quote_plus(text)        # this allows you to enter special characters
    url = MAIN_URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

# while True:
#     jsf = get_updates(url)
#     update = jsf['result']
#     last_update = get_last_updateid(update)
#     update = get_updates(last_update)
#     msg, chatid = get_last_chat_id_and_text(update)
#     print (msg)
#     send_message(msg, chatid)

def main():
    jsf = get_updates(url)
    update = jsf['result']
    last_update = None
    while True:
        update = get_updates(last_update)
        if len(update["result"]) > 0:
            last_update_id = get_last_updateid(update) + 1
            msg, chatid = get_last_chat_id_and_text(update)
            print (msg)
            send_message(msg, chatid)
        time.sleep(0.5)


if __name__ == '__main__':
    main()

# print (url)
# update = js.update_id()
# print (update_ids)
