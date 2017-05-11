# -*- coding: utf-8 -*-

import os

from flask import render_template, redirect, url_for
from manage import app, BASE_DIR
from utils.traversal import item_traversal


@app.route('/group')
def group():
    grouplist = item_traversal('conf/groups')
    for _ in grouplist['conf/groups']:
        filepath = BASE_DIR + '/conf/groups/' + _
        with open(filepath, 'rb') as f:
            content = f.readlines()
            for _ in content:
                print _.strip('\n')
    group_add('new_group')
    return render_template(
        'group.html',
        grouplist=grouplist,
    )


@app.route('/group/<group_name>')
def group_add(group_name):
    f = open(BASE_DIR + '/conf/groups/' + group_name + '.conf', 'wb+')
    f.close()
    return redirect(
        url_for('group')
    )
