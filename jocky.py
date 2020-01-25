import json
import requests
import time

TOKEN = "830873928:AAE5u4XF95Lc0LwKRV0HFYMcvM5Jty3ITMA"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

# in below function we get url of message from where we will download content of the message
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content
 
#  below here we download contents from site
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

# here we will get updates of message
def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js

# to get text and chatid from last update 
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

# to send message 
def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    

def main():
    last_textchat = (None, None)
    while True:         #to continuously read the message
        text, chat = get_last_chat_id_and_text(get_updates())
        if (text, chat) != last_textchat:
            send_message(text, chat)
            # last_textchat = (text, chat)
        time.sleep(0.5)         


if __name__ == '__main__':
    main()