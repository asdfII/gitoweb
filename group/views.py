# -*- coding: utf-8 -*-

import os
import re
try:
    import simplejson as json
except:
    import json
from pprint import pprint

from flask import (
    request,
    render_template, redirect, url_for, abort,
)
from manage import app, BASE_DIR
from utils.widgets import item_traversal, allowed_file, Pagination
from index.models import GitUser, GitGroup, GitRepo, GitSubRepo
from db.database import db_session

allowed_ext = ['conf']
groupdict = {}


@app.route('/group', methods=['GET', 'POST'])
def group():
    groupdict = {}
    groupfile = item_traversal('conf/groups')
    try:
        groupfile = groupfile['conf/groups']
        if groupfile:
            for _ in groupfile:
                if allowed_file(_, allowed_ext):
                    filepath = BASE_DIR + '/conf/groups/' + _
                    with open(filepath, 'rb') as f:
                        content = f.readlines()
                        for _ in content:
                            group_name = (
                                ((_.strip('\n')).split('='))[0]
                            ).strip().lstrip('@')
                            group_member = (
                                (_.strip('\n')).split('=')
                            )[1]
                            groupdict[group_name] = group_member
    except:
        groupfile = []
    if request.method == 'POST':
        new_group_name = request.form.get('addGroupName', '')
        query_group = db_session.query(
            GitGroup
        ).filter_by(name=new_group_name)
        if not db_session.query(
            query_group.exists()
        ).scalar() and new_group_name.strip() != '':
            try:
                new_group = GitGroup(name=new_group_name)
                db_session.add(new_group)
                db_session.commit()
                group_init(new_group_name)
            except:
                db_session.rollback()
            finally:
                db_session.close()
            return redirect(url_for('group'))
    return render_template(
        'group.html',
        groupdict=groupdict,
    )


@app.route('/group/<group_name>')
def group_init(group_name):
    group_init_file = BASE_DIR + '/conf/groups/' + group_name + '.conf'
    if not os.path.exists(group_init_file):
        f = open(group_init_file, 'wb+')
        f.truncate()
        f.write('@' + group_name + ' = '.rstrip('\r'))
        f.close()
    return redirect(url_for('group'))


@app.route('/group/remove', methods=['POST'])
def group_remove():
    if request.method == 'POST':
        try:
            remove_group_name = request.form.keys()[0]
        except IndexError:
            remove_group_name = ''
        group_name_file = BASE_DIR + '/conf/groups/' \
            + remove_group_name + '.conf'
        deletegroup = db_session.query(
                    GitGroup
                ).filter_by(name=remove_group_name).first()
        db_session.delete(deletegroup)
        db_session.commit()
        db_session.close()
        os.remove(group_name_file)
        #~ groupdict.pop(remove_group_name)
        return redirect(url_for('group'))


@app.route('/group/rename', methods=['POST'])
def group_rename():
    if request.method == 'POST':
        try:
            old_groupname = request.form.keys()[0]
        except IndexError:
            old_groupname = ''
        new_groupname = request.form.get(old_groupname, '')
        old_name_file = BASE_DIR + '/conf/groups/' \
            + old_groupname + '.conf'
        new_name_file = BASE_DIR + '/conf/groups/' \
            + new_groupname + '.conf'
        if new_groupname.strip(
        ) != '' and new_groupname != old_groupname:
            renamegroup = db_session.query(
                GitGroup
            ).filter_by(name=old_groupname).first()
            renamegroup.name = new_groupname
            db_session.commit()
            db_session.close()
            #~ groupdict.pop(old_groupname)
            new_lines = []
            with open(old_name_file, 'r') as f:
                while True:
                    lines = f.readlines(8192)        
                    if not lines:
                        break
                    for line in lines:
                        line = line.rstrip('\n')
                        line = re.sub('@'+old_groupname, '@'+new_groupname, line)
                        new_lines.append(line)
            with open(old_name_file, 'w') as f:
                f.truncate()
                for _ in new_lines:
                    print >>f, _
            os.rename(old_name_file, new_name_file)
        return redirect(url_for('group'))
