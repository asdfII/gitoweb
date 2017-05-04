# -*- coding: utf-8 -*-

from flask import (
    request, session, g,
    redirect, url_for, abort,
    render_template, flash, make_response,
)
from werkzeug.utils import secure_filename
from manage import app
from .models import GitUser, GitGroup, GitRepo
from db.database import sessionmaker, engine, db_session


@app.route('/', methods=['Get'])
def index():
    try:
        #~ new_user = GitUser(name='alphaz')
        #~ db_session.add(new_user)
        db_session.commit()
    except:
        db_session.rollback()
    return render_template('index.html')


#~ @app.route('/index')
#~ def index_self():
    #~ response = make_response(redirect(url_for('index')))
    #~ return response
    #~ return render_template('index.html')


@app.route('/show')
def show():
    return redirect(url_for('group'))


@app.route('/error')
def error():
    return render_template('error.html')
