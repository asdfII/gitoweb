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
repodict = {}
subrepodict = {}


@app.route('/repo', methods=['GET', 'POST'])
def repo():
    repodict = {}
    repofile = item_traversal('conf/repos')
    try:
        repofile = repofile['conf/repos']
    except:
        repofile = []
    for _ in repofile:
        if allowed_file(_, allowed_ext):
            filepath = BASE_DIR + '/conf/repos/' + _
            with open(filepath, 'rb') as f:
                content = f.readlines()
                for _ in content:
                    if '=' in _:
                        repo_name = (
                            ((_.strip('\n')).split('='))[0]
                        ).strip().lstrip('@')
                        repo_member = (
                            (_.strip('\n')).split('=')
                        )[1]
                        repodict[repo_name] = repo_member
    
    subrepodict = {}
    subrepoitem = {}
    subrepofile = item_traversal('conf/subrepos')
    try:
        subrepofile = subrepofile['conf/subrepos']
    except:
        subrepofile = []
    for _ in subrepofile:
        if allowed_file(_, allowed_ext):
            filepath = BASE_DIR + '/conf/subrepos/' + _
            with open(filepath, 'rb') as f:
                first_line = f.readline().strip('\n')
                subrepo_name = first_line[4:].strip()
                content = f.readlines()
                for _ in content:
                    if '=' in _:
                        subrepo_item = (
                            ((_.strip('\n')).split('='))[0]
                        ).strip().lstrip('@')
                        subrepo_member = (
                            (_.strip('\n')).split('=')
                        )[1]
                        subrepoitem[subrepo_item] = subrepo_member
            subrepodict[subrepo_name] = subrepoitem.copy()
    subrepotorepodict = {}
    assignedlist = []
    assignedgroup = {}
    
    for gitsubrepo in GitSubRepo.query.filter_by(
        main_repo_id=None
    ).all():
        subrepotorepodict[gitsubrepo.id] = gitsubrepo.name
    for i in repodict.keys():
        queries = GitSubRepo.query.join(GitRepo).filter(
            GitRepo.name==i
        ).all()
        for query in queries:
            assignedlist.append(query.name)
        assignedgroup[i] = assignedlist
        assignedlist = []
    
    if request.args:
        tab_page = request.args.get('tab_page', '')
        subRepoName = request.args.get('subRepoName', '')
    else:
        tab_page = 0
        subRepoName = ''
    subitemdict = {}
    select_subrepo = ''
    grouptosubrepodict = {}
    for gitgroup in db_session.query(GitGroup).all():
        grouptosubrepodict[gitgroup.id] = gitgroup.name
    grouptosubrepodict[0] = u'all'
    
    if request.method == 'GET':
        if 'subRepoName' in request.args.keys() and 'tab_page' in request.args.keys():
            select_subrepo = str(request.args.get('subRepoName', ''))
            subitemdict = subrepodict[select_subrepo]
    
    if request.method == 'POST':
        if 'addMainRepoName' in request.form.keys():
            get_repo_name = request.form.get('addMainRepoName', '')
            new_repo_name = ''
            if get_repo_name[0] == '%' and get_repo_name[-1] == '%':
                new_repo_name = get_repo_name.strip('%')
            elif not (
                get_repo_name[0] == '%' and get_repo_name[-1] == '%'
            ):
                if not get_repo_name.endswith('_repo'):
                    get_repo_name = get_repo_name + '_repo'
                new_repo_name = get_repo_name
            query_repo = db_session.query(
                GitRepo
            ).filter_by(name=new_repo_name)
            if not db_session.query(
                query_repo.exists()
            ).scalar() and new_repo_name.strip() != '':
                try:
                    new_repo = GitRepo(name=new_repo_name)
                    db_session.add(new_repo)
                    db_session.commit()
                    repo_init(new_repo_name)
                except:
                    db_session.rollback()
                finally:
                    db_session.close()
            return redirect(url_for('repo'))
        elif 'addSubRepoName' in request.form.keys():
            new_sub_repo_name = request.form.get('addSubRepoName', '')
            if '/' in new_sub_repo_name:
                new_sub_repo_name = '~'.join(
                    new_sub_repo_name.split('/')
                )
            query_repo = db_session.query(
                GitSubRepo
            ).filter_by(name=new_sub_repo_name)
            if not db_session.query(
                query_repo.exists()
            ).scalar() and new_sub_repo_name.strip() != '':
                try:
                    new_sub_repo = GitSubRepo(name=new_sub_repo_name)
                    db_session.add(new_sub_repo)
                    db_session.commit()
                    sub_repo_init(new_sub_repo_name)
                except:
                    db_session.rollback()
                finally:
                    db_session.close()
            return redirect(url_for('repo'))
        elif 'subRepoName' in request.form.keys():
            tab_page = 1
            select_subrepo = str(request.form.get('subRepoName', ''))
            subitemdict = subrepodict[select_subrepo]
    return render_template(
        'repo.html',
        #~ repofile=repofile,
        repodict=repodict,
        subrepodict=subrepodict,
        subrepotorepodict=subrepotorepodict,
        assignedgroup=assignedgroup,
        tab_page=tab_page,
        select_subrepo=select_subrepo,
        subitemdict = subitemdict,
        grouptosubrepodict=grouptosubrepodict,
        subRepoName=subRepoName,
    )


@app.route('/repo/<repo_name>')
def repo_init(repo_name):
    repo_init_file = BASE_DIR + '/conf/repos/' + repo_name + '.conf'
    f = open(repo_init_file, 'wb+')
    f.truncate()
    f.write('@' + repo_name + ' = '.rstrip('\r'))
    f.close()
    return redirect(
        url_for('repo')
    )


@app.route('/repo/sub/<sub_repo_name>')
def sub_repo_init(sub_repo_name):
    sub_repo_init_file = BASE_DIR + '/conf/subrepos/' \
        + sub_repo_name + '.conf'
    if '~' in sub_repo_name:
        sub_repo_name = '/'.join(sub_repo_name.split('~'))
    f = open(sub_repo_init_file, 'wb+')
    f.truncate()
    f.write('repo ' + sub_repo_name)
    f.write('\n')
    f.write('RW+C                    = ')
    f.write('\n')
    f.write('-   VREF/comments       = ')
    f.write('\n')
    f.write('RW                      = ')
    f.write('\n')
    f.write('-   release             = ')
    f.write('\n')
    f.write('RWC release-v[0-9\.]+   = ')
    f.write('\n')
    f.write('RW                      = ')
    f.write('\n')
    f.write('RWC dbg_[\w]+_[\w]+     = ')
    f.close()
    return redirect(
        url_for('repo')
    )


@app.route('/repo/remove', methods=['POST'])
def repo_remove():
    if request.method == 'POST':
        try:
            remove_repo_name = request.form.keys()[0]
        except IndexError:
            remove_repo_name = ''
        repo_name_file = BASE_DIR + '/conf/repos/' \
            + remove_repo_name + '.conf'
        deleterepo = db_session.query(
            GitRepo
        ).filter_by(name=remove_repo_name).first()
        db_session.delete(deleterepo)
        db_session.commit()
        db_session.close()
        os.remove(repo_name_file)
        #~ groupdict.pop(remove_group_name)
        return redirect(url_for('repo'))


@app.route('/repo/sub/remove', methods=['POST'])
def sub_repo_remove():
    if request.method == 'POST':
        try:
            remove_sub_repo_name = request.form.get('subRepoName', '')
        except IndexError:
            remove_sub_repo_name = ''
        if remove_sub_repo_name and '/' in remove_sub_repo_name:
            remove_sub_repo_name = '~'.join(
                remove_sub_repo_name.split('/')
            )
        sub_repo_name_file = BASE_DIR + '/conf/subrepos/' \
            + remove_sub_repo_name + '.conf'
        deletesubrepo = db_session.query(
            GitSubRepo
        ).filter_by(name=remove_sub_repo_name).first()
        if deletesubrepo:
            db_session.delete(deletesubrepo)
            db_session.commit()
            db_session.close()
            os.remove(sub_repo_name_file)
        tab_page = 1
        return redirect(url_for('repo', tab_page=tab_page))


@app.route('/repo/rename', methods=['POST'])
def repo_rename():
    if request.method == 'POST':
        try:
            old_reponame = request.form.keys()[0]
        except IndexError:
            old_reponame = ''
        new_reponame = request.form.get(old_reponame, '')
        old_name_file = BASE_DIR + '/conf/repos/' \
            + old_reponame + '.conf'
        new_name_file = BASE_DIR + '/conf/repos/' \
            + new_reponame + '.conf'
        if new_reponame.strip(
        ) != '' and new_reponame != old_reponame:
            renamerepo = db_session.query(
                GitRepo
            ).filter_by(name=old_reponame).first()
            renamerepo.name = new_reponame
            db_session.commit()
            db_session.close()
            #~ repodict.pop(old_reponame)
            new_lines = []
            with open(old_name_file, 'rb') as f:
                while True:
                    lines = f.readlines(8192)
                    if not lines:
                        break
                    for line in lines:
                        line = line.rstrip('\n')
                        line = re.sub('@'+old_reponame,
                            '@'+new_reponame, line
                        )
                        new_lines.append(line)
            with open(old_name_file, 'wb') as f:
                f.truncate()
                for _ in new_lines:
                    print >>f, _
            os.rename(old_name_file, new_name_file)
        return redirect(url_for('repo'))


@app.route('/repo/sub/rename', methods=['POST'])
def sub_repo_rename():
    if request.method == 'POST':
        try:
            old_subreponame = request.form.keys()[0]
        except IndexError:
            old_subreponame = ''
        new_subreponame = request.form.get(old_subreponame, '')
        
        if '/' in old_subreponame:
            old_subreponame = '~'.join(old_subreponame.split('/'))
        if '/' in new_subreponame:
            new_subreponame = '~'.join(new_subreponame.split('/'))
        old_name_file = BASE_DIR + '/conf/subrepos/' \
            + old_subreponame + '.conf'
        new_name_file = BASE_DIR + '/conf/subrepos/' \
            + new_subreponame + '.conf'
        
        if new_subreponame.strip(
        ) != '' and new_subreponame != old_subreponame:
            renamesubrepo = db_session.query(
                GitSubRepo
            ).filter_by(name=old_subreponame).first()
            renamesubrepo.name = new_subreponame
            db_session.commit()
            db_session.close()
            #~ subrepodict.pop(old_subreponame)
            new_lines = []
        if '~' in old_subreponame:
            old_subreponame = '/'.join(old_subreponame.split('~'))
        if '~' in new_subreponame:
            new_subreponame = '/'.join(new_subreponame.split('~'))
            with open(old_name_file, 'rb') as f:
                while True:
                    lines = f.readlines(8192)
                    if not lines:
                        break
                    for line in lines:
                        line = line.rstrip('\n')
                        line = re.sub('@'+old_subreponame,
                            '@'+new_subreponame, line
                        )
                        new_lines.append(line)
            with open(old_name_file, 'wb') as f:
                f.truncate()
                for _ in new_lines:
                    print >>f, _
            os.rename(old_name_file, new_name_file)
        return redirect(url_for('repo'))


@app.route('/repo/subrepo/add', methods=['POST'])
def add_asso_subrepo():
    if request.method == 'POST':
        try:
            request_key = request.form.keys()[0]
            get_repo_name = request_key.split('-')[1]
            get_subrepo_name = request.form.get(request_key, '')
            assosubrepo = db_session.query(
                GitSubRepo
            ).filter_by(name=get_subrepo_name).first()
            assorepo = db_session.query(
                GitRepo
            ).filter_by(name=get_repo_name).first()
            if assosubrepo.main_repo_id != assorepo.id:
                try:
                    assosubrepo.main_repo_id = assorepo.id
                    db_session.commit()
                    
                    assorepo_file = BASE_DIR + '/conf/repos/' \
                        + assorepo.name + '.conf'
                    rconf_dict = {}
                    with open(assorepo_file, 'rb') as f:
                        lines = f.readlines()
                        for line in lines:
                            rconf_repo = line.split('=')[0].lstrip('@').strip()
                            rconf_subrepo = line.split('=')[1].split()
                            rconf_dict[rconf_repo] = rconf_subrepo
                    
                    if rconf_dict.has_key(
                        assorepo.name
                    ) and get_subrepo_name not in rconf_dict[assorepo.name]:
                        rconf_dict[assorepo.name].append(
                            str(re.sub('~', '/', get_subrepo_name))
                        )
                        f = open(assorepo_file, 'wb')
                        f.truncate()
                        for _ in rconf_dict:
                            f.write('@' + _ + ' = ' + ' '.join(rconf_dict[_]))
                        f.close()
                except TypeError:
                    db_session.rollback()
                    print '====>  TypeError Need string or buffer, list found.'
                finally:
                    db_session.close()
        except IndexError:
            db_session.rollback()
            print '====>  IndexError Out of range.'
    return redirect(url_for('repo'))


@app.route('/user/sub/remove', methods=['POST'])
def remove_asso_subrepo():
    if request.method == 'POST':
        try:
            request_key = request.form.keys()[0]
            get_repo_name = request_key.split('-')[1]
            get_subrepo_name = request.form.get(request_key, '')
            assorepo = db_session.query(
                GitRepo
            ).filter_by(name=get_repo_name).first()
            assosubrepo = db_session.query(
                GitSubRepo
            ).filter_by(name=get_subrepo_name).first()
            assosubrepo.main_repo_id = None
            db_session.add(assosubrepo)
            db_session.commit()
            print '====>  Sponge (%s) from DB successfully.' % assosubrepo.name
            
            assorepo_file = BASE_DIR + '/conf/repos/' \
                + assorepo.name + '.conf'
            rconf_dict = {}
            with open(assorepo_file, 'rb') as f:
                lines = f.readlines()
                for line in lines:
                    rconf_repo = line.split('=')[0].lstrip('@').strip()
                    rconf_subrepo = line.split('=')[1].split()
                    rconf_dict[rconf_repo] = rconf_subrepo
            
            if rconf_dict.has_key(
                assorepo.name
            ) and '/'.join(
                get_subrepo_name.split('~')
            ) in rconf_dict[assorepo.name]:
                rconf_dict[assorepo.name].remove(
                    str(re.sub('~', '/', get_subrepo_name))
                )
                f = open(assorepo_file, 'wb')
                f.truncate()
                for _ in rconf_dict:
                    f.write('@' + _ + ' = ' + ' '.join(rconf_dict[_]))
                f.close()            
        except IndexError:
            db_session.rollback()
            print '====>  IndexError Out of range.'
        except ValueError:
            db_session.rollback()
            print '====>  ValueError Not in list.'
        finally:
            db_session.close()
        return redirect(url_for('repo'))


@app.route('/repo/subrepogroup/add', methods=['POST'])
def add_asso_subrepo_group():
    if request.method == 'POST':
        try:
            request_key = request.form.keys()[0]
            get_subrepo_name = request_key.split(':')[1]
            get_item_name = request_key.split(':')[2]
            get_group_name = request.form.get(request_key, '')
            get_group_name = '@' + get_group_name
            
            assosubrepo_file = BASE_DIR + '/conf/subrepos/' \
                + re.sub('/', '~', get_subrepo_name) + '.conf'
            iconf_dict = {}
            subrepo_name = ''
            with open(assosubrepo_file, 'rb') as f:
                first_line = f.readline().strip('\n')
                subrepo_name = first_line[4:].strip()
                content = f.readlines()
                for _ in content:
                    if '=' in _:
                        iconf_key = (
                            (_.strip('\n').split('='))[0]
                        ).strip()
                        iconf_value = (
                            (_.strip('\n').split('='))[1]
                        ).split()
                        iconf_dict[iconf_key] = iconf_value
            
            if iconf_dict.has_key(
                get_item_name
            ) and get_group_name not in iconf_dict[get_item_name]:
                iconf_dict[get_item_name].append(
                    str(get_group_name)
                )
                f = open(assosubrepo_file, 'wb')
                f.truncate()
                f.write('repo ' + subrepo_name + '\n')
                for _ in iconf_dict:
                    f.write(_ + ' = ' + ' '.join(iconf_dict[_]) + '\n')
                f.close()
        except IndexError:
            print '====>  IndexError Out of range.'
        tab_page = 1
        subRepoName = get_subrepo_name
    return redirect(url_for(
        'repo',
        tab_page=tab_page,
        subRepoName=subRepoName,
    ))


@app.route('/user/subrepogroup/remove', methods=['POST'])
def remove_asso_subrepo_group():
    if request.method == 'POST':
        try:
            request_key = request.form.keys()[0]
            get_subrepo_name = request_key.split(':')[1]
            get_item_name = request_key.split(':')[2]
            get_group_name = request.form.get(request_key, '')
            get_group_name = '@' + get_group_name
            
            assosubrepo_file = BASE_DIR + '/conf/subrepos/' \
                + re.sub('/', '~', get_subrepo_name) + '.conf'
            iconf_dict = {}
            subrepo_name = ''
            with open(assosubrepo_file, 'rb') as f:
                first_line = f.readline().strip('\n')
                subrepo_name = first_line[4:].strip()
                content = f.readlines()
                for _ in content:
                    if '=' in _:
                        iconf_key = (
                            (_.strip('\n').split('='))[0]
                        ).strip()
                        iconf_value = (
                            (_.strip('\n').split('='))[1]
                        ).split()
                        iconf_dict[iconf_key] = iconf_value
            
            if iconf_dict.has_key(
                get_item_name
            ) and get_group_name in iconf_dict[get_item_name]:
                iconf_dict[get_item_name].remove(
                    str(get_group_name)
                )
                f = open(assosubrepo_file, 'wb')
                f.truncate()
                f.write('repo ' + subrepo_name + '\n')
                for _ in iconf_dict:
                    f.write(_ + ' = ' + ' '.join(iconf_dict[_]) + '\n')
                f.close()
        except IndexError:
            print '====>  IndexError Out of range.'
        tab_page = 1
        subRepoName = get_subrepo_name
    return redirect(url_for(
        'repo',
        tab_page=tab_page,
        subRepoName=subRepoName,
    ))
