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

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


with app.test_request_context():
    print url_for('index')
    print url_for('hello', name='test')
    print url_for('static', filename='./react/react.min.js')

if __name__ == '__main__':
    app.run()