# -*- coding: utf-8 -*-

import os
import time
import subprocess
try:
    import simplejson as json
except:
    import json
import platform
if platform.system() == 'Windows':
    proc_shell = True
elif platform.system() == 'Linux':
    proc_shell = False

from flask import (
    request, session, g,
    redirect, url_for, abort,
    render_template, flash, make_response,
)
from werkzeug.utils import secure_filename
from manage import app
from index.models import GitUser, GitGroup, GitRepo
from db.database import db_session


@app.route('/', methods=['GET', 'POST'])
def index():
    proc = subprocess.Popen(['git', 'status'],
        stdout=subprocess.PIPE,
        shell=proc_shell,
    )
    (results, errors) = proc.communicate()
    return render_template(
        'index.html',
        results = results,
    )


@app.route('/git/status', methods=['POST'])
def git_status():
    if request.method == 'POST':
        key = request.form
        if key.has_key('gitStatus'):
            proc1 = subprocess.Popen(['git', 'status'],
                stdout=subprocess.PIPE,
                shell=proc_shell,
            )
            (results1, errors1) = proc1.communicate()
        elif key.has_key('gitConfirm') and key.has_key('gitComment'):
            comments = key.get('gitComment')
            if comments == '':
                comments = 'Default Web Commit at ' + time.strftime(
                    "%Y%m%d%H%M%S", time.localtime()
                )
            #~ os.system("git add .")
            #~ os.system("git add -A")
            #~ os.system("git commit -m " + comments)
            #~ os.system("git push origin dev")
            proc0 = subprocess.Popen(['git', 'add', '.'],
                stdout=subprocess.PIPE,
                shell=proc_shell,
            )
            proc1 = subprocess.Popen(['git', 'add', '-A'],
                stdout=subprocess.PIPE,
                shell=proc_shell,
            )
            proc2 = subprocess.Popen(['git', 'commit', '-m', comments],
                stdout=subprocess.PIPE,
                shell=proc_shell,
            )
            proc3 = subprocess.Popen(['git', 'push'],
                stdout=subprocess.PIPE,
                shell=proc_shell,
            )
            (results0, errors0) = proc0.communicate()
            (results1, errors1) = proc1.communicate()
            (results2, errors2) = proc2.communicate()
            (results3, errors3) = proc3.communicate()
    return redirect(url_for('index'))


@app.route('/error')
def error():
    return render_template('error.html')
