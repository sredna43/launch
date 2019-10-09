from flask import Flask, request
import subprocess, sys
import docker
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "SUPER SECRET KEY"
app.config["MONGO_URI"] = "mongodb://localhost:27017/Launch"
mongo = PyMongo(app)
@app.route('/')
def home():
    return ("<h1>Hello, World!</h1>")

@app.route('/api/<query>')
def api(query):
    return("Placeholder")

# Responds to POST requests that contain JSON data
@app.route('/deploy', methods=['POST'])
def deploy():
    json_data = request.get_json()
    if request.method == "POST":
        repo = json_data['repo']
        user = json_data['user']
        if repo is not None and user is not None:
            mongo.db.
        github_string = 'git@github.com:{}/{}.git'.format(user,repo)
        if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            subprocess.call(['mkdir', '/home/{}/{}'.format(user,repo)])
            subprocess.call(['git','init'])
            subprocess.call(['git', 'clone', github_string])
            # create_image(user, repo)
            return("cloning {}".format(github_string))
        else:
            print('Running on windows, most likely dev...')
            print('Right now would be setting up ' + repo + ' from user: ' + user)


if __name__ == '__main__':
    app.debug = True
    app.run(use_reloader=True, debug=True, host='0.0.0.0', port=5001)