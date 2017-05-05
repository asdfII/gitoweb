# -*- coding: utf-8 -*-

from flask import render_template
from manage import app


@app.route('/user')
def user():
    userdata = {
        'name': 'gitoweb',
        'project': 'gitowebproj',
    }
    return render_template('user.html', userdata=userdata)
