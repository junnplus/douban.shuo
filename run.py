# -*- coding: utf-8 -*-
import sys

from workflow import Workflow3
from base import start_http_server
from base import stop_http_server


def main(wf):
    access_token = wf.cached_data('access_token', max_age=0)
    if not access_token:
        wf.add_item('Login', 'Douban Login', arg='login', valid=True)
        start_http_server()
    else:
        wf.add_item('Logout', 'Douban Logout', arg='logout', valid=True)
        stop_http_server()
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
