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
    status_dict = {
        0: 'Upload successfully.',
        1: 'Not a pub key file.',
        2: 'The pub key already exists.',
        3: 'Error while writing into db.',
    }
    upload_status = {}
    
    f = open('log.log', 'ab+')
    if request.method == 'POST':
        file = request.files['file']
        if file:
            if not allowed_file(file.filename):
                upload_status['status'] = 1
                return render_template(
                    'upload.html',
                    upload_status=upload_status,
                )
            filename = secure_filename(file.filename)
            filepath = os.path.join(KEY_DIRS, filename)
            if os.path.isfile(filepath):
                upload_status['status'] = 2
                return render_template(
                    'upload.html',
                    upload_status=upload_status,
                )
            file.save(filepath)
            print >>f, filename + " has been saved locally."
            try:
                new_user = GitUser(name=filename)
                db_session.add(new_user)
                db_session.commit()
                upload_status['status'] = 0
                return render_template(
                    'upload.html',
                    upload_status=upload_status,
                )
            except:
                db_session.rollback()
                os.remove(filepath)
                upload_status['status'] = 3
                return render_template(
                    'upload.html',
                    upload_status=upload_status,
                )
    f.close()
    keylist = item_traversal('keydir')
    return render_template(
        'user.html',
        keylist=keylist,
        data=status_dict,
    )
