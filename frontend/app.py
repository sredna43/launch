from flask import Flask, flash, url_for, render_template, request, Response, redirect
from flask_static_compress import FlaskStaticCompress
from flask_bootstrap import Bootstrap
from markupsafe import escape

from forms import GithubRepo
import sys
import json

app = Flask(__name__, template_folder='templates', static_folder="static")
Bootstrap(app)

@app.route('/', methods=('GET', 'POST'))
def homepage():
    form = GithubRepo()
    if request.method == 'POST':
        if form.validate():
            flash('Cloning {}'.format(escape('repo')))
    return render_template('form.html', form=form, title="Launch UI")

if __name__ == '__main__':
    app.secret_key = 'secret key'
    app.debug = True
    app.run(use_reloader=True)