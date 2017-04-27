# -*- coding: utf-8 -*-

import sys

from flask import (
    Flask, request, session,
    url_for, redirect, render_template,
    make_response,
    )
from werkzeug.utils import secure_filename
from db.database import sessionmaker, engine, db_session
from models import *

new_user = GitUser(name='alphaz')
db_session.add(new_user)
try:
    db_session.commit()
except:
    db_session.rollback()

app = Flask(__name__)


@app.route('/')
def login(name=None):
    #~ return render_template('hello.html', name=name)
    return "Please log in."


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('upload/uploaded_file.txt')

if __name__ == '__main__':
    app.run()