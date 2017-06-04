# -*- coding: utf-8 -*-

import socket

from flask import Flask
from gitoweb.settings import *


app = Flask(__name__)


if __name__ == '__main__':
    from index.views import *
    from repo.views import *
    from group.views import *
    from user.views import *
    from ceshi.views import *
    try:
        app.run(
            '0.0.0.0',
            5000,
            threaded=True,
            debug=True,
        )
    except socket.error:
        print 'Massive requests and socket error.'
