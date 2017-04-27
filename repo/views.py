# -*- coding: utf-8 -*-

from flask import Flask
from index.views import app


@app.route('/repo')
def repo():
    return "RRRRRRRRRRRRRRRRRRRepoooo"
