from flask import Flask, request
from pymongo import MongoClient, errors
import os, sys
from docker_helper import clone_repo, create_image, find_dockerfiles
from kubernetes_helper import create_deployment_object, create_deployment, delete_deployment, update_deployment


app = Flask(__name__)
app.secret_key = "SUPER SECRET KEY"
client = MongoClient("mongodb://datastore:27017/Launch")
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
        db = json_data['db']
        print("User selected database: " + db)
        images = []     
        if clone_repo(user, repo):
            dockerfiles = find_dockerfiles(user, repo)            
            for path_to_dockerfile in dockerfiles:
                images.append(create_image(repo, user, path_to_dockerfile))
        else:
            return("Something got messed up!")
        deployment_name = repo + "-deployment"
        try:
            config_location = sys.argv[1]
        except:
            config_location = None
        try:
            delete_deployment(deployment_name, config_location)
        except:
            print("Delete didn't work... unsure why")
            pass
        try:
            create_deployment(create_deployment_object(images, deployment_name, config_location=config_location), config_location=config_location)
        except:
            update_deployment(create_deployment_object(images, deployment_name, config_location=config_location), deployment_name, config_location=config_location)

        #MongoDB stuff
        try:
            if repo is not None and user is not None:
                user_param = collection_users.find({'username': {"$in" :[user]}})
                if user_param:
                    collection_users.update({'username':user},{"$push" :{'git-repo':{"$each" :[repo]}}})
                else:
                    user = {
                        'username': user,
                        'git-repo': [repo]
                    }
                # Attempt to connect to the db
                result = db.collection_users.insert_one(user)
        except errors.ServerSelectionTimeoutError:
            print("MongoDB could not be found")
    return("Done!")
            
        
if __name__ == '__main__':
    app.debug = True
    app.run(use_reloader=True, debug=True, host='0.0.0.0', port=5001)