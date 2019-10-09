from flask import Flask, request
from pymongo import MongoClient
import os
from deployment import *

app = Flask(__name__)
app.secret_key = "SUPER SECRET KEY"
client = MongoClient("mongodb://localhost:27017/Launch")
db = client.Launch
collection_users = db.users
@app.route('/')
def home():
    return ("<h1>Hello, World!</h1>")

@app.route('/api/<query>')
def api(query):
    return("Placeholder")

# Responds to POST requests that contain JSON data
@app.route('/deploy', methods=['POST'])
def deploy():
    if request.method == "POST":
        json_data = request.get_json()
        user = json_data['user']
        repo = json_data['repo']        
        clone_repo(user, repo)
        if repo is not None and user is not None:
            user = {
                'username': user,
                'git-repo': [repo]
            }
            result = db.collection_users.insert_one(user)
            dockerfiles = 
        create_image(user, repo, path_to_dockerfile)
if __name__ == '__main__':
    app.debug = True
    app.run(use_reloader=True, debug=True, host='0.0.0.0', port=5001)