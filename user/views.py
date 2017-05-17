# -*- coding: utf-8 -*-

import os

from flask import (
    request, send_from_directory,
    render_template, redirect, url_for
)
from werkzeug.utils import secure_filename
from manage import app, KEY_DIR
from utils.widgets import item_traversal, allowed_file
from index.models import GitUser, GitGroup, GitRepo
from db.database import db_session

allowed_ext = ['pub']


@app.route('/user/<filename>')
def uploaded_file(filename):
    return send_from_directory(KEY_DIR, filename)


@app.route('/user', methods=['GET', 'POST'])
def user():
    status_dict = {
        0: 'Upload successfully.',
        1: 'Not a pub key file.',
        2: 'The pub key already exists.',
        3: 'Error while writing into db.',
        4: 'Please choose a pub key file.'
    }
    #~ keydict = item_traversal('keydir')
    userdict = {}
    groupdict = {}
    upload_status = {'status': '-1'}
    
    f = open('log.log', 'ab+')
    if request.method == 'POST':
        file = request.files['keyFile']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(KEY_DIR, filename)
            if not allowed_file(filename, allowed_ext):
                upload_status['status'] = 1
                print >>f, filename + ' is not a pub key.'
                return render_template(
                    'upload.html',
                    upload_status=upload_status,
                )
            if os.path.exists(filepath):
                upload_status['status'] = 2
                return render_template(
                    'upload.html',
                    upload_status=upload_status,
                )
            try:
                new_user = GitUser(name=filename)
                db_session.add(new_user)
                db_session.commit()
                db_session.close()
                file.save(filepath)
                print >>f, filename + ' has been saved locally.'
                upload_status['status'] = 0
                return render_template(
                    'upload.html',
                    upload_status=upload_status,
                )
            except:
                db_session.rollback()
                db_session.close()
                upload_status['status'] = 3
                return render_template(
                    'upload.html',
                    upload_status=upload_status,
                )
        else:
            upload_status['status'] = 4
            return render_template(
                'upload.html',
                upload_status=upload_status,
            )
    f.close()
    for _ in db_session.query(GitUser).all():
        userdict[_.id] = _.name.rstrip('.pub')
    for _ in db_session.query(GitGroup).all():
        groupdict[_.id] = _.name.rstrip('.pub')
    db_session.close()
    return render_template(
        'user.html',
        userdict=userdict,
        groupdict=groupdict,
        data=status_dict,
    )
