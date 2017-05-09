# -*- coding: utf-8 -*-

import os

from flask import (
    request, send_from_directory,
    render_template, redirect, url_for
)
from werkzeug.utils import secure_filename

from gitoweb.settings import KEY_DIRS
from utils.traversal import item_traversal
from manage import app


ALLOWED_EXTENSIONS = set(['pub'])


@app.route('/user')
def user():
    userdata = item_traversal('keydir')
    return render_template('user.html', userdata=userdata)


def allowed_file(filename):
    return '.' in filename \
        and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(KEY_DIRS, filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(KEY_DIRS, filename))
            #~ return redirect(
            print (
                url_for(
                    'uploaded_file',
                    filename=filename
                )
            )
    #~ return redirect(url_for('user'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
