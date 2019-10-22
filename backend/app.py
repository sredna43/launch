from flask import Flask, request
from pymongo import MongoClient, errors
import os
from deployment import clone_repo, create_image, find_dockerfiles

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
        images = []     
        if clone_repo(user, repo):
            dockerfiles = find_dockerfiles(user, repo)            
            for path_to_dockerfile in dockerfiles:
                images.append(create_image(repo, path_to_dockerfile))
            print(images)

        #MongoDB stuff
        if repo is not None and user is not None:
            user = {
                'username': user,
                'git-repo': [repo]
            }
            # Attempt to connect to the db
            try:
                result = db.collection_users.insert_one(user)
            except errors.ServerSelectionTimeoutError:
                print("MongoDB could not be found")
            
        
if __name__ == '__main__':
    app.debug = True
    app.run(use_reloader=True, debug=True, host='0.0.0.0', port=5001)