# -*- coding: utf-8 -*-

import sys
from gitoweb.settings import BASE_DIR
sys.path.append(BASE_DIR)

from repo.views import app


#~ app = Flask(__name__)

if __name__ == '__main__':
    app.run()