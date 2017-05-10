# -*- coding: utf-8 -*-

import os

from flask import (
    request, send_from_directory,
    render_template, redirect, url_for
)
from werkzeug.utils import secure_filename
from manage import app
from gitoweb.settings import KEY_DIRS
from utils.traversal import item_traversal
from index.models import GitUser, GitGroup, GitRepo
from db.database import db_session

ALLOWED_EXTENSIONS = set(['pub'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/user/<filename>')
def uploaded_file(filename):
    return send_from_directory(KEY_DIRS, filename)


@app.route('/user', methods=['GET', 'POST'])
def user():
    f = open('log.log', 'ab+')
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(KEY_DIRS, filename))
            print >>f, filename + " has been saved."
            try:
                new_user = GitUser(name=filename)
                db_session.add(new_user)
                db_session.commit()
                print >>f, "Write DB successfully"
            except:
                db_session.rollback()
            return render_template('upload.html')
        if file and not allowed_file(file.filename):
            return render_template('error.html')
    f.close()
    keylist = item_traversal('keydir')
    return render_template('user.html', keylist=keylist)
