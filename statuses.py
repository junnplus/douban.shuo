# -*- coding: utf-8 -*-
import sys

from workflow import Workflow3
from workflow import web
from base import avatar_url_to_path
from base import DOUBAN_API
from base import COMMENTS_URL


def main(wf):
    res = web.get(DOUBAN_API + COMMENTS_URL.format(wf.args[0]))
    if res.error:
        wf.send_feedback()
        return

    comments = res.json()
    for comment in comments:
        text = comment['text']
        avatar_path = avatar_url_to_path(comment['user']['small_avatar'])
        user_status = comment['user']['screen_name']
        wf.add_item(text, user_status, largetext=text, icon=avatar_path)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
