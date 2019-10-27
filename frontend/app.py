from flask import Flask, flash, url_for, render_template, request, Response, redirect, session
from flask_bootstrap import Bootstrap
from markupsafe import escape
import requests

from forms import GithubRepo, User
import sys
import json

''' 
Current idea is to have something like this set up for each project that we take in.
Basically, force the user to include some way of handling a backend_ip file being
placed in their main code folder so that we can dynamically update ip addresses.

Better ideas for this will be gladly accepted.
'''
try:
    f = open('backend_ip', 'r')
    backend_host = f.readline().replace('\n', '').replace(' ', '').replace('"', '').replace("'", "")
    backend_port = f.readline().replace('\n', '').replace(' ', '').replace('"', '').replace("'", "")
except:
    backend_host = '127.0.0.1'
    backend_port = '27017'

print("Backend IP is: " + backend_host + ":" + backend_port)

# Create our global variable 'app'
app = Flask(__name__, template_folder='templates', static_folder="static")
Bootstrap(app) # Bootstraps the entire project, very useful for neat CSS
app.secret_key = 'devkey' # There are better ways to generate a random string

# App routes are used to handle browser requests at different endpoints in our project
@app.route('/', methods = ('GET', 'POST'))
def UserForm():
    form = User()
    if request.method == 'POST':
        session['user'] = form.user.data
        return redirect('/repo')
    return render_template('form.html', form=form, title="Launch UI")

@app.route('/repo', methods=('GET', 'POST'))
def RepoForm():
    URL = 'https://api.github.com/users/' + session['user'] + '/repos'
    try:
        r = requests.get(URL)        
    except:
        return render_template('index.html', message='We had some trouble getting to Github...', title='Launch UI - Connection Error', btn="Try again")
    repo_json = r.json()
    try:
        select_field_repos = [(repo['name'], repo['name']) for repo in repo_json]
        select_field_repos.insert(0,('','Select a Repository'))
    except:
        return render_template('index.html', message='We had some trouble getting to Github, try checking your username.', title='Launch UI - Username Error', btn="Try again")

    form = GithubRepo()
    form.repo.choices = select_field_repos
    if request.method == 'POST': # Once the user has hit 'submit'
        # Set the Session variables 'user' and 'repo' so that we can use them later
        session['repo'] = form.repo.data
        session['db'] = form.db.data
        return redirect('/submit')
    return render_template('form.html', form=form, title="Launch UI")

@app.route('/submit')
def Submit():
    # This is where we can reach out to the tool and start spinning up a container!
    send_data = {'user': session.get('user'), 'repo': session.get('repo'), 'db': session.get('db')}
    try:
        res = requests.post('http://{}:{}/deploy'.format(backend_host, backend_port), json=send_data)
    except requests.exceptions.ConnectionError:
        print("Connection error to backend at {}:{}".format(backend_host, backend_port))
        return render_template('index.html', title="Launch UI - Error", message="Oops, looks like someone stepped on a crack and broke our back(end)...", btn="Home")
    return render_template('index.html', title="Launch UI - Spinning Up", message="Thanks {}, {} is now live!".format(session['user'], session['repo']), btn="Start Over", spinner="loading")

if __name__ == '__main__':
    app.debug = True
    app.run(use_reloader=True, host='0.0.0.0', port=5000)