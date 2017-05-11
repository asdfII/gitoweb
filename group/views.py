# -*- coding: utf-8 -*-

import os

from flask import (
    request,
    render_template, redirect, url_for
)
from manage import app, BASE_DIR
from utils.traversal import item_traversal


@app.route('/group', methods=['GET', 'POST'])
def group():
    grouplist = {}
    groupfile = item_traversal('conf/groups')
    groupfile = groupfile['conf/groups']
    for _ in groupfile:
        filepath = BASE_DIR + '/conf/groups/' + _
        with open(filepath, 'rb') as f:
            content = f.readlines()
            for _ in content:
                group_name = (((_.strip('\n')).split('='))[0]).strip().lstrip('@')
                group_member = ((_.strip('\n')).split('='))[1]
                grouplist[group_name] = group_member
    #~ if request.method == 'POST':
        #~ group_add('new_group')
    group_add('new_group')
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
