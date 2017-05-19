# -*- coding: utf-8 -*-

import os
try:
    import simplejson as json
except:
    import json

from flask import (
    request,
    render_template, redirect, url_for
)
from manage import app, BASE_DIR
from utils.widgets import item_traversal, allowed_file
from index.models import GitUser, GitGroup, GitRepo
from db.database import db_session


@app.route('/ceshi')
def ceshi():
    ceshidict = {'x': 1, 'y': 2, 'z': 3}
    context = {
        'ceshistring': json.dumps(ceshidict),
    }
    return render_template(
        'ceshi.html',
        ceshidict=ceshidict,
        context=context,
    )
