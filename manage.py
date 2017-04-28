# -*- coding: utf-8 -*-

from flask import Flask


app = Flask(__name__)


if __name__ == '__main__':
    from index.views import *
    from group.views import *
    from repo.views import *
    app.run()
