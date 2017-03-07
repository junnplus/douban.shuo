# -*- coding: utf-8 -*-
import os
import re
import subprocess
from collections import defaultdict

from workflow import web

SHUO_URL = 'shuo/v2/statuses/home_timeline'
USER_URL = 'v2/user/'
STATUSES_URL = 'shuo/v2/statuses/'
COMMENTS_URL = 'shuo/v2/statuses/{}/comments'
DOUBAN_API = 'https://api.douban.com/'


def avatar_url_to_path(url):
    avatar_path = 'icons/' + url.split('/')[-1]
    if not os.path.exists(avatar_path):
        web.get(url).save_to_path(avatar_path)
    return avatar_path


def format_reshared_status(user, reshared_user):
    totle = 120
    reshared = reshared_user + u' 转播'
    spaces = totle - len(user.encode('utf-8')) - len(reshared.encode('utf-8'))
    return user + ' ' * spaces + reshared


def get_user_name(user_id):
    data = web.get(DOUBAN_API + USER_URL + user_id).json()
    return data['name']


def format_text(text):
    uids = re.findall(r'@(?P<uid>\d+)', text)
    uids_map = {}
    uids_count = defaultdict(int)
    for uid in uids:
        uids_count[uid] += 1
        try:
            name = get_user_name(uid)
        except Exception:
            uids_map[uid] = uid
        else:
            uids_map[uid] = name
    for k, v in uids_map.items():
        text = text.replace(k, v, uids_count[k])
    return text


def start_http_server():
    try:
        subprocess.Popen('python ./server.py', shell=True)
    except Exception:
        pass


def stop_http_server():
    subprocess.Popen("ps aux|grep 'python ./server.p[y]'|awk '{print $2}'|xargs kill -9", shell=True)
