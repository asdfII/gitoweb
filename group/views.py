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


@app.route('/group', methods=['GET', 'POST'])
def group():
    grouplist = {}
    groupfile = item_traversal('conf/groups')
    try:
        groupfile = groupfile['conf/groups']
    except:
        groupfile = {}
    for _ in groupfile:
        if allowed_file(_, allowed_ext):
            filepath = BASE_DIR + '/conf/groups/' + _
            with open(filepath, 'rb') as f:
                content = f.readlines()
                for _ in content:
                    group_name = (((_.strip('\n')).split('='))[0]).strip().lstrip('@')
                    group_member = ((_.strip('\n')).split('='))[1]
                    grouplist[group_name] = group_member
    if request.method == 'POST':
        new_group_name = request.form.get('addGroupName', '')
        if new_group_name:
            try:
                new_group = GitGroup(name=new_group_name)
                db_session.add(new_group)
                db_session.commit()
                db_session.close()
                group_add(new_group_name)
            except:
                db_session.rollback()
                db_session.close()
                os.remove(os.path.join(filepath, new_group_name))
        return redirect(url_for('group'))
    return render_template(
        'group.html',
        #~ grouplist=groupfile,
        grouplist=grouplist,
    )


@app.route('/group/<group_name>')
def group_add(group_name):
    f = open(BASE_DIR + '/conf/groups/' + group_name + '.conf', 'wb+')
    f.truncate()
    f.write('@' + group_name + ' = ')
    f.close()
    return redirect(
        url_for('group')
    )
