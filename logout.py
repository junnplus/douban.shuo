# -*- coding: utf-8 -*-
import sys

from workflow import Workflow3
from workflow.notify import notify


def main(wf):
    wf.clear_cache(lambda f: f.startswith('access_token'))
    notify('Douban Logout', 'Please login again')


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
