# -*- coding: utf-8 -*-

import sys

from flask import (
    Flask,
    request,
    session,
    url_for,
    redirect,
    render_template,
    )

from models import GitUser, GitGroup, GitRepo
#~ init_db('gitolite', 'gitolite', 'gitolite')

app = Flask(__name__)


@app.route('/')
def index():
    pass


@app.route('/login')
def login():
    pass


@app.route('/user/')
@app.route('/user/<username>')
def profile(username=None):
    return render_template('user.html', username=username)


with app.test_request_context():
    print url_for('index')
    print url_for('login', user='admin')
    print url_for('profile', username='test')
    print url_for('static', filename='./react/react.min.js')

if __name__ == '__main__':
    app.run()