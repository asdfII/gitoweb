# -*- coding: utf-8 -*-

import os
try:
    import simplejson as json
except:
    import json

from flask import (
    request,
    render_template, redirect, url_for, abort,
)
from manage import app, BASE_DIR
from utils.widgets import item_traversal, allowed_file
from index.models import GitUser, GitGroup, GitRepo
from db.database import db_session

allowed_ext = ['conf']


@app.route('/repo', methods=['GET', 'POST'])
def repo():
    repodict = {}
    repofile = item_traversal('conf/repos')
    try:
        repofile = repofile['conf/repos']
    except:
        repofile = {}
    for _ in repofile:
        if allowed_file(_, allowed_ext):
            filepath = BASE_DIR + '/conf/repos/' + _
            with open(filepath, 'rb') as f:
                content = f.readlines()
                for _ in content:
                    if '=' in _:
                        repo_name = (((_.strip('\n')).split('='))[0]).strip().lstrip('@')
                        repo_member = ((_.strip('\n')).split('='))[1]
                        repodict[repo_name] = repo_member
    print repodict
    if request.method == 'POST':
        new_repo_name = request.form.get('addRepoName', '')
        if new_repo_name:
            try:
                new_repo = GitRepo(name=new_repo_name)
                db_session.add(new_repo)
                db_session.commit()
                repo_init(new_repo_name)
            except:
                db_session.rollback()
                os.remove(os.path.join(filepath, new_repo_name))
            db_session.close()
        return redirect(url_for('repo'))
    return render_template(
        'repo.html',
        #~ repofile=repofile,
        repodict=repodict,
    )


@app.route('/repo/<repo_name>')
def repo_add(repo_name):
    f = open(BASE_DIR + '/conf/repos/' + repo_name + '.conf', 'wb+')
    f.truncate()
    f.write('@' + repo_name + ' = ')
    f.close()
    return redirect(
        url_for('repo')
    )

