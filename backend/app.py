from flask import Flask, request
from pymongo import MongoClient, errors
import os
from deployment import clone_repo, create_image, find_dockerfiles

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
# finds all objects in database, then makes jsonfile with all objects
@app.route('/api/getAll',methods=['GET'])
def getAllObj():
    json_data = collection_users.find()
    writeTOJSONFile(json_data)
def writeTOJSONFile(json_data):
    file = open("all_objects.json", "w")
    json_docs = []
    file.write('[')
    for document in json_data:
        json_docs = json.dumps(document, default=json_util.default)
        json_docs.append(json_docs)
        file.write(json.dumps(document))
        file.write(',')
    file.write(']')
    return json_docs
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
                images.append(create_image(repo, path_to_dockerfile))
            print(images)
        else:
            return("Something got messed up!")

        #MongoDB stuff
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
                try:
                    result = db.collection_users.insert_one(user)
                except errors.ServerSelectionTimeoutError:
                    print("MongoDB could not be found")
    return(str(image for image in images))
            
        
if __name__ == '__main__':
    app.debug = True
    app.run(use_reloader=True, debug=True, host='0.0.0.0', port=5001)