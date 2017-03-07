# -*- coding: utf-8 -*-
import re
import sys

from workflow import Workflow3
from workflow import web
from base import SHUO_URL
from base import DOUBAN_API
from base import avatar_url_to_path
from base import format_reshared_status
from base import format_text
from base import start_http_server
from base import stop_http_server


def main(wf):
    access_token = wf.cached_data('access_token', max_age=0)
    if not access_token:
        wf.add_item('Login', 'Douban login', arg='login', valid=True)
        wf.send_feedback()
        start_http_server()
    else:
        stop_http_server()
        headers = {'Authorization': 'Bearer ' + access_token}
        datas = web.get(DOUBAN_API + SHUO_URL + '?count=50', headers=headers).json()
        for data in datas:
            avatar_path = avatar_url_to_path(data['user']['small_avatar'])
            user_status = '@' + data['user']['screen_name']
            text = format_text(data['text'])
            if data['title'] and not data.get('reshared_status'):
                stars = re.findall(r'\d', data['title'])
                if stars:
                    stars = int(stars[0])
                    text = u'★' * stars + u'☆' * (5 - stars) + ' ' + text
                    user_status += ' ' + data['title'][:2]
                else:
                    user_status += ' ' + data['title']

            if data.get('reshared_status'):
                original = data['reshared_status']
                if not text:
                    text = format_text(original['text'])
                    attachments = original['attachments']
                    if attachments:
                        attachment = attachments[0]
                        if attachment['type'] == 'image' and attachment['media']:
                            text += u'[图片]'

                avatar_path = avatar_url_to_path(original['user']['small_avatar'])
                user_status = format_reshared_status('@' + original['user']['screen_name'] + ' ' + original['title'], user_status)

            attachments = data['attachments']
            if attachments:
                attachment = attachments[0]
                attachment_type = attachment['type']
                if attachment_type == 'image' and attachment['media']:
                    text += u'[图片]'
                if text:
                    user_status += ' ' + attachment['title']
                else:
                    text = attachment['title']
            wf.add_item(text, user_status, largetext=text, icon=avatar_path, arg=data['id'], valid=True)
        wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
