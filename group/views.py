# -*- coding: utf-8 -*-

from flask import render_template
from manage import app


@app.route('/group')
def group():
    return render_template('group.html')
