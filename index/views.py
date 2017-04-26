# -*- coding: utf-8 -*-

import sys

from flask import (
    Flask,
    request, session,
    url_for, redirect, render_template,
    make_response,
    )
from werkzeug.utils import secure_filename
from .models import *

Session = sessionmaker(bind=engine)
session = Session()

new_user = GitUser(id=1, name='alphaz')
session.add(new_user)
try:
    session.commit()
except:
    session.rollback()

app = Flask(__name__)


@app.route('/')
def index():
    username = request.cookies.get('username')
    #request.cookies['username']
    # Storing cookies
    #resp = make_response(render_template(...))
    #resp.set_cookie('username', 'the username')
    #return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(
            request.form['username'],
            request.form['password']
            ):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('upload/uploaded_file.txt')


with app.test_request_context():
    print url_for('login')
    print url_for('hello', name='test')
    print url_for('static', filename='./react/react.min.js')

with app.test_request_context('/hello', method='POST'):
    assert request.path == '/hello'
    assert request.method == 'POST'

if __name__ == '__main__':
    app.run()