# -*- coding: utf-8 -*-

import sys

from flask import (
    Flask,
    request,
    session,
    url_for,
    redirect,
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


@app.route('/user/<username>')
def profile(username):
    pass


with app.test_request_context():
    print url_for('index')
    print url_for('login', user='admin')
    print url_for('profile', username='test')


#~ if __name__ == '__main__':
    #~ app.run()