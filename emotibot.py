import logging
import json
import requests
import re
import os
import sys
import opencc

from slackbot import settings
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot_utils import *

appid = os.getenv('EMOTIBOT_APPID', None)
if not appid:
    logging.CRITICAL('no Emotibot AppId is found. Make sure EMOTIBOT_APPID is set')
    sys.exit(1)

url = 'http://idc.emotibot.com/api/ApiKey/openapi.php'

userid_db = {}
userid_db_file = 'emotibot_userid_db.json'
userid_db_loaded = False


def emotibot_register():
    register_data = {"cmd": "register", "appid": appid}
    r = requests.post(url, params=register_data)
    response = json.dumps(r.json(), ensure_ascii=False)
    jsondata = json.loads(response)
    datas = jsondata.get('data')
    return datas[0].get('value')


def emotibot_chat(userid, msg):
    register_data = {"cmd": "chat", "appid": appid, "userid": userid, "text": msg, "location": ""}
    r = requests.post(url, params=register_data)
    response = json.dumps(r.json(), ensure_ascii=False)
    jsondata = json.loads(response)
    datas = jsondata.get("data")
    if len(datas) == 0:
        return ''
    return datas[0].get('value', '')


def emotibot_initialize_db():
    global userid_db, userid_db_loaded
    logging.info('loading userid db from %s', userid_db_file)
    with open(userid_db_file, 'r') as f:
        userid_db = json.load(f)
        userid_db_loaded = True


def get_userid(user):
    global userid_db
    if not userid_db_loaded:
        emotibot_initialize_db()
    if not userid_db.get(user, None):
        userid = emotibot_register()
        userid_db[user] = userid
        logging.info('registered a new user %s as %s', user, userid)
        with open(userid_db_file, 'w') as f:
            json.dump(userid_db, f)
        return userid
    else:
        return userid_db.get(user, None)


def chat(user, msg):
    logging.info('chat (%s)-> %s', user, msg)
    msg = emotibot_chat(get_userid(user), msg)
    msg = opencc.convert(msg, config='s2tw.json')
    logging.info('chat (%s)<- %s', user, msg)
    return msg


@respond_to('.*', re.IGNORECASE)
def slack_chat(msg):
    body = msg.body
    # print body
    if body.get('text', ''):
        msg.reply(chat(body.get('user', ''), body.get('text', '')))
