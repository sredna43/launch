from flask import Flask, flash, url_for, render_template, request, Response, redirect, session
from flask_bootstrap import Bootstrap
from markupsafe import escape

from forms import GithubRepo
import sys
import json

backend = '127.0.0.1'

app = Flask(__name__, template_folder='templates', static_folder="static")
Bootstrap(app)
app.secret_key = 'devkey'

@app.route('/', methods=('GET', 'POST'))
def RepoForm():
    form = GithubRepo()
    if request.method == 'POST':
        print(form.user.data)
        session['user'] = form.user.data
        session['repo'] = form.repo.data
        return redirect('/submit')
    return render_template('form.html', form=form, title="Launch UI")

@app.route('/submit')
def Submit():
    # This is where we can reach out to the tool and start spinning up a container!
    return render_template('index.html', title="Launch UI - Spinning Up", user=session.get('user'), repo=session.get('repo'))

if __name__ == '__main__':
    app.debug = True
    app.run(use_reloader=True, host='0.0.0.0')