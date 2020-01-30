import json
import requests
import time
import urllib
from settings import RULES, BOT_INTRO

f_open = open('token.txt','r')
TOKEN = f_open.read()
print (TOKEN)
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        group_title = None
        text = None
        new_member = None
        chat_id = None
        rep_msg_id = None
        rep_chat_id = None
        # print (update["message"])
        for i in update["message"]:
            if (i == "text"):
                text = update["message"]["text"]
            if (i == "chat"):
                if (update["message"]["chat"]["type"] == "supergroup" ): #| update["message"]["chat"]["type"] == "supergroup"):
                    group_title = update["message"]["chat"]["title"]
                chat_id = update["message"]["chat"]["id"]
            if (i == "reply_to_message"):
                rep_msg_id = update["message"]["reply_to_message"]["message_id"]
                rep_chat_id = update["message"]["reply_to_message"]["chat"]["id"]
            if (i == "new_chat_participant"):
                new_member = update["message"]["new_chat_member"]
            elif (i == "new_chat_member"):
                new_member = update["message"]["new_chat_member"]
            elif (i == "new_chat_members"):
                new_member = update["message"]["new_chat_member"]
        user_id = update["message"]["from"]["id"]
        msg_id = update["message"]["message_id"]
        username = update["message"]["from"]["username"]
        # reply = "wrong entry"
        if (text == "/hello"):
            reply = "Hi @" + username
            send_message(reply, chat_id)
        elif (text == "/start"):
            reply = BOT_INTRO
            chat_id = user_id
            send_message(reply, chat_id)
        elif (text == "/rules"):
            reply = RULES
            chat_id = user_id
            send_message(reply, chat_id)
        elif (new_member != None):
            reply = "Welcome "+new_member["first_name"]+" to "+group_title
            send_message(reply,chat_id)
        elif (text == "/delete"):
            if (rep_msg_id != None):
                delete_message(rep_chat_id,rep_msg_id)            
                delete_message(chat_id,msg_id)
            else:
                delete_message(chat_id,msg_id)
        elif (text.split(" ")[0] == "/kick"):
            print ("kicking")
            x = text.split(" ")
            kick_user(chat_id,x[1])     #is not working
            send_message("kicked "+x[1],chat_id)
            


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    # print (chat_id)
    # print (text)
    # text = urllib.parse.quote_plus(text)        # this allows you to enter special characters
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def delete_message(chat_id,message_id):
    url = URL + "deleteMessage?chat_id={}&message_id={}".format(chat_id,message_id)
    get_url(url)

def kick_user(chat_id,user_id):
    url = URL + "kickChatMember?chat_id={}&user_id={}".format(chat_id,user_id)
    get_url(url)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()