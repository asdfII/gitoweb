# -*- coding: utf-8 -*-

from flask import render_template
from manage import app


@app.route('/repo')
def repo():
    return render_template('repo.html')
