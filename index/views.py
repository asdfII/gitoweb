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


#~ Session = sessionmaker(bind=engine)
#~ session = Session()

#~ new_user = GitUser(name='alphaz')
#~ session.add(new_user)


@app.route('/', methods=['Get'])
def login():
    new_user = GitUser(name='alphaz')
    db_session.add(new_user)
    try:
        db_session.commit()
    except:
        db_session.rollback()
    return render_template('index.html')
