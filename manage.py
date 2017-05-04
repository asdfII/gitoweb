# -*- coding: utf-8 -*-

import socket

from flask import Flask


app = Flask(__name__)


if __name__ == '__main__':
    from index.views import *
    from repo.views import *
    from group.views import *
    from user.views import *
    try:
        app.run()
    except socket.error:
        print 'Massive requests and socket error.'
