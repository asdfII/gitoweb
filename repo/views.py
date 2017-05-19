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

allowed_ext = ['conf']


@app.route('/repo', methods=['GET', 'POST'])
def repo():
    return render_template('repo.html')


'''
# -*- coding: utf-8 -*-

import os

from flask import (
    request,
    render_template, redirect, url_for
)
from manage import app, BASE_DIR
from utils.widgets import item_traversal, allowed_file
from index.models import GitUser, GitGroup, GitRepo
from db.database import db_session

allowed_ext = ['conf']


@app.route('/repo', methods=['GET', 'POST'])
def repo():
    repolist = {}
    repofile = item_traversal('conf/repos')
    repofile = repofile['conf/repos']
    print repofile
    for _ in repofile:
        if allowed_file(_, allowed_ext):
            filepath = BASE_DIR + '/conf/repos/' + _
            with open(filepath, 'rb') as f:
                content = f.readlines()
                for _ in content:
                    repo_name = (((_.strip('\n')).split('='))[0]).strip().lstrip('@')
                    repo_member = ((_.strip('\n')).split('='))[1]
                    repolist[repo_name] = repo_member
    if request.method == 'POST':
        new_repo_name = request.form.get('addRepoName', '')
        if new_repo_name:
            repo_add(new_repo_name)
            return redirect(url_for('repo'))
    return render_template(
        'repo.html',
        #~ repolist=repofile,
        repolist=repolist,
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
'''