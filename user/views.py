# -*- coding: utf-8 -*-

import os
import re
try:
    import simplejson as json
except:
    import json

from flask import (
    request, send_from_directory,
    render_template, redirect, url_for, abort,
)
from werkzeug.utils import secure_filename
from manage import app, KEY_DIR
from utils.widgets import item_traversal, allowed_file, Pagination
from index.models import (
    GitUser, GitGroup, GitRepo,
    asso_group_user
)
from db.database import db_session

allowed_ext = ['pub']


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
    assignedlist = []
    assignedgroup = {}
    upload_status = {'status': '-1'}

    for gituser in db_session.query(GitUser).all():
        userdict[gituser.id] = gituser.name
    for gitgroup in db_session.query(GitGroup).all():
        groupdict[gitgroup.id] = gitgroup.name
    for i in userdict.keys():
        queries = GitGroup.query.filter(
            GitGroup.git_user.any(id=i)
        ).all()
        for query in queries:
            assignedlist.append(query.name)
        assignedgroup[i] = assignedlist
        assignedlist = []
    
    f = open('log.log', 'ab+')
    if request.method == 'POST':
        for request_key in request.form.keys():
            if 'addIntoGroupName' in request_key:
                get_user_id = int(request_key.split('-')[1])
                get_group_id = request.form.get(request_key, '')
                try:
                    assouser = db_session.query(
                        GitUser
                    ).filter_by(id=get_user_id).first()
                    assogroup = db_session.query(
                        GitGroup
                    ).filter_by(id=get_group_id).first()
                    assouser.git_group.append(assogroup)
                    db_session.add(assouser)
                    db_session.commit()
                except:
                    db_session.rollback()
                db_session.close()
                return redirect(url_for('user'))
        if request.files:
            file = request.files.get('keyFile', '')
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
    
    db_session.close() 
    return render_template(
        'user.html',
        status_dict=status_dict,
        userdict=userdict,
        groupdict=groupdict,
        assignedgroup=assignedgroup,
    )


@app.route('/user/<filename>')
def uploaded_file(filename):
    return send_from_directory(KEY_DIR, filename)


@app.route('/user/int:<user_id>/group')
def assign_group(user_id):
    return redirect(
        url_for('user')
    )
