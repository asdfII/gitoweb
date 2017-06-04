# -*- coding: utf-8 -*-

import os
import re
try:
    import simplejson as json
except:
    import json
from pprint import pprint

from flask import (
    request, send_from_directory,
    render_template, redirect, url_for, abort,
)
from werkzeug.utils import secure_filename
from manage import app, BASE_DIR, KEY_DIR
from utils.widgets import item_traversal, allowed_file, Pagination
from index.models import (
    GitUser, GitGroup, GitRepo, GitSubRepo,
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
        3: 'Please choose a pub key file.',
        4: 'Error while writing into db.',
        5: 'Please check if `keydir` exists.',
    }
    #~ keydict = item_traversal('keydir')
    userdict = {}
    grouptouserdict = {}
    assignedlist = []
    assignedgroup = {}
    upload_status = {'status': '-1'}
    
    for gituser in db_session.query(GitUser).all():
        userdict[gituser.id] = gituser.name
    for gitgroup in db_session.query(GitGroup).all():
        grouptouserdict[gitgroup.id] = gitgroup.name
    for i in userdict.keys():
        queries = GitGroup.query.filter(
            GitGroup.git_user.any(id=i)
        ).all()
        for query in queries:
            assignedlist.append(query.name)
        assignedgroup[i] = assignedlist
        assignedlist = []
    
    f = open('log.log', 'ab+')
    if request.method == 'POST' and request.files:
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
                file.save(filepath)
                db_session.commit()
                upload_status['status'] = 0
                print >>f, filename + ' has been saved locally.'
                return render_template(
                    'upload.html',
                    upload_status=upload_status,
                )
            except IOError:
                db_session.rollback()
                upload_status['status'] = 5
                return render_template(
                    'upload.html',
                    upload_status=upload_status,
                )
            except:
                db_session.rollback()
                upload_status['status'] = 4
                return render_template(
                    'upload.html',
                    upload_status=upload_status,
                )
            finally:
                db_session.close()
        else:
            upload_status['status'] = 3
            return render_template(
                'upload.html',
                upload_status=upload_status,
            )
    f.close()
    return render_template(
        'user.html',
        status_dict=status_dict,
        userdict=userdict,
        grouptouserdict=grouptouserdict,
        assignedgroup=assignedgroup,
    )


@app.route('/user/<filename>')
def uploaded_file(filename):
    return send_from_directory(KEY_DIR, filename)


@app.route('/user/remove', methods=['POST'])
def user_remove():
    if request.method == 'POST':
        try:
            remove_user_name = request.form.keys()[0]
        except IndexError:
            remove_user_name = ''
        assouser = db_session.query(
            GitUser
        ).filter_by(name=remove_user_name).first()
        assogroup_relation = db_session.query(
            asso_group_user
        ).filter_by(git_user_id=assouser.id).all()
        
        assogroup_list = []
        for _ in assogroup_relation:
            assogroup = db_session.query(
                GitGroup
            ).filter_by(id=_.git_group_id).first()
            assogroup_list.append(assogroup)
        if not assogroup_list:
            for assogroup in assogroup_list:
                assouser.git_group.remove(assogroup)
                db_session.delete(assouser)
        db_session.delete(assouser)
        db_session.commit()
        
        deleteuser_assogroup = []
        for _ in assogroup_list:
            deleteuser_assogroup_file = BASE_DIR \
                + '/conf/groups/' + _.name + '.conf'
            deleteuser_assogroup.append(
                deleteuser_assogroup_file
            )
        
        gconf_dict = {}
        for i in deleteuser_assogroup:
            with open(i, 'rb') as f:
                lines = f.readlines()
                for line in lines:
                    gconf_group = line.split('=')[0].lstrip('@').strip()
                    gconf_user = line.split('=')[1].split()
                    gconf_dict[gconf_group] = gconf_user
        
        assouser.name = '.'.join(assouser.name.split('.')[:-1])
        assouser_name = str(assouser.name)
        for each_group in gconf_dict:
            if assouser_name in gconf_dict[each_group]:
                gconf_dict[each_group].remove(assouser_name)
                assogroup_file = BASE_DIR + '/conf/groups/' + each_group \
                    + '.conf'
                f = open(assogroup_file, 'wb')
                f.truncate()
                f.write('@' + each_group + ' = ' + ' '.join(gconf_dict[each_group]))
                f.close()
        db_session.close()
        user_name_file = os.path.join(KEY_DIR, remove_user_name)
        os.remove(user_name_file)
        return redirect(url_for('user'))


@app.route('/user/group/add', methods=['POST'])
def add_asso_group():
    if request.method == 'POST':
        try:
            request_key = request.form.keys()[0]
            get_user_id = int(request_key.split('-')[1])
            get_group_id = int(request.form.get(request_key, ''))
            assouser = db_session.query(
                GitUser
            ).filter_by(id=get_user_id).first()
            assogroup = db_session.query(
                GitGroup
            ).filter_by(id=get_group_id).first()
            if assogroup not in assouser.git_group:
                assouser.git_group.append(assogroup)
            
            assos = db_session.query(asso_group_user).all()
            if (get_group_id, get_user_id) not in assos:
                try:
                    db_session.add(assouser)
                    db_session.commit()
                    print '====>  Store (%s) to DB successfully.' % assouser.name
                    
                    assogroup_file = BASE_DIR + '/conf/groups/' \
                        + assogroup.name + '.conf'
                    gconf_dict = {}
                    with open(assogroup_file, 'rb') as f:
                        lines = f.readlines()
                        for line in lines:
                            gconf_group = line.split('=')[0].lstrip('@').strip()
                            gconf_user = line.split('=')[1].split()
                            gconf_dict[gconf_group] = gconf_user
                    allowed_ext_user = []
                    for _ in allowed_ext:
                        allowed_ext_user.append(
                            '.'.join(assouser.name.split('.')[:-1])
                        )
                    for _ in set(allowed_ext_user):
                        if gconf_dict.has_key(
                            assogroup.name
                        ) and _ not in gconf_dict[assogroup.name]:
                            gconf_dict[assogroup.name].append(str(_))
                            f = open(assogroup_file, 'wb')
                            f.truncate()
                            for _ in gconf_dict:
                                f.write('@' + _ + ' = ' + ' '.join(gconf_dict[_]))
                            f.close()
                except TypeError:
                    db_session.rollback()
                    print '====>  TypeError Need string or buffer, list found.'
                finally:
                    db_session.close()
            else:
                print '====>  The record(%s) already exists.' % assouser.name
        except IndexError:
            print '====>  IndexError because of out of range.'
        return redirect(url_for('user'))


@app.route('/user/group/remove', methods=['POST'])
def remove_asso_group():
    if request.method == 'POST':
        try:
            request_key = request.form.keys()[0]
            get_user_id = int(request_key.split('-')[1])
            get_group_id = request.form.get(request_key, '')
            assouser = db_session.query(
                GitUser
            ).filter_by(id=get_user_id).first()
            assogroup = db_session.query(
                GitGroup
            ).filter_by(id=get_group_id).first()
            assouser.git_group.remove(assogroup)
            db_session.add(assouser)
            db_session.commit()
            print '====>  Sponge (%s) from DB successfully.' % assouser.name
            
            assogroup_file = BASE_DIR + '/conf/groups/' \
                + assogroup.name + '.conf'
            gconf_dict = {}
            with open(assogroup_file, 'rb') as f:
                lines = f.readlines()
                for line in lines:
                    gconf_group = line.split('=')[0].lstrip('@').strip()
                    gconf_user = line.split('=')[1].split()
                    gconf_dict[gconf_group] = gconf_user
            allowed_ext_user = []
            for _ in allowed_ext:
                allowed_ext_user.append(
                    '.'.join(assouser.name.split('.')[:-1])
                )
            for _ in set(allowed_ext_user):
                if gconf_dict.has_key(
                    assogroup.name
                ) and _ in gconf_dict[assogroup.name]:
                    gconf_dict[assogroup.name].remove(str(_))
                    f = open(assogroup_file, 'wb')
                    f.truncate()
                    for _ in gconf_dict:
                        f.write('@' + _ + ' = ' + ' '.join(gconf_dict[_]))
                    f.close()
        except IndexError:
            db_session.rollback()
            print '====>  IndexError Out of range.'
        except ValueError:
            db_session.rollback()
            print '====>  ValueError Not in list.'
        finally:
            db_session.close()
        return redirect(url_for('user'))
