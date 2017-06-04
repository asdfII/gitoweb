# -*- coding: utf-8 -*-

import os
try:
    import simplejson as json
except:
    import json

from flask import (
    request,
    render_template, redirect, url_for, abort,
    jsonify,
)
from manage import app, BASE_DIR
from utils.widgets import (
    item_traversal, allowed_file,
    Pagination,
)
from index.models import GitUser, GitGroup, GitRepo
from db.database import db_session


@app.route('/ceshi/', defaults={'page':1})
@app.route('/ceshi/page/<int:page>')
def ceshi(page):
    #~ abort(404)
    ceshidict = {
        'alphaz': ['admin', 'superuser'],
        'user01': ['superuser'],
        'user02': [],
    }
    ceshistring = json.dumps(ceshidict)
    #~ pagination = Pagination(page, PER_PAGE, count)
    pagination = Pagination(page, 1, 3)
    return render_template(
        'ceshi.html',
        ceshidict=ceshidict,
        ceshistring=ceshistring,
    )


@app.route('/ceshi-ajax', methods=['GET', 'POST'])
def ceshi_ajax():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        error = None
        if len(username) < 5:
            error = 'Password must be at least 5 characters.'
        if len(password) < 6:
            error = 'Password must be at least 6 characters.'
        elif not any(c.isupper() for c in password):
            error = 'Your password needs at least 1 capital.'
        if error is not None:
            return jsonify({'r': 1, 'error': error})
        return jsonify({'r': 0, 'rs': 'ok'})
    return render_template('ceshi-ajax.html')
