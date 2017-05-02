# -*- coding: utf-8 -*-

from flask import (
    Flask,
    request, session,
    url_for, redirect, render_template,
    make_response,
    )
from werkzeug.utils import secure_filename

from manage import app
from .models import GitUser, GitGroup, GitRepo
from db.database import sessionmaker, engine


#~ Session = sessionmaker(bind=engine)
#~ session = Session()

#~ new_user = GitUser(name='alphaz')
#~ session.add(new_user)
#~ try:
    #~ session.commit()
#~ except:
    #~ session.rollback()


@app.route('/')
def login():
    return "Please log in."
