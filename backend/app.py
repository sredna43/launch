from flask import Flask, request
from pymongo import MongoClient, errors
from flask_pymongo  import PyMongo
from flask.ext.bcrypt import Bcrypt
import os, sys, subprocess
from docker_helper import clone_repo, create_image, find_dockerfiles
from kubernetes_helper import create_deployment_object, create_deployment, delete_deployment, update_deployment, create_service
import logging

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "SUPER SECRET KEY"
bcrypt_pw = bcrypt.generate_password_hash(config.pw)
app.config["MONGO_URI"] = "mongodb+srv://{}:{}@launch-emlpr.gcp.mongodb.net/test?retryWrites=true&w=majority".format(config.username,bcrypt_pw)


mongo = PyMongo(app)
logging.basicConfig(filename="backend.log", format='%(levelname)s: %(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
try:
    logger.info("Docker username set by environment variables: {}".format(os.environ['DOCKERUSER']))
except:
    logger.warning("Docker username set by hard-coded value: {}".format('stolaunch'))

try:
    config_location = sys.argv[1]
except:
    config_location = None

@app.route('/')
def home():
    logger.debug("GET request to '/'")
    return ("<h1>Hello, World!</h1>")

@app.route('/api/<query>')
def api(query):
    logger.debug("GET request to '/api/{}".format(query))
    return("Placeholder")
# finds all objects in database, then makes jsonfile with all objects
@app.route('/api/getAll',methods=['GET'])
def getAllObj():
    logger.debug("GET request to '/api/getAll")
    json_data = mongo.db.users.find()
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
        logger.debug("User selected database: {}".format(db))
        images = []     
        if clone_repo(user, repo):
            dockerfiles = find_dockerfiles(user, repo)
            for path_to_dockerfile in dockerfiles:
                logger.info("calling create_image({}, {}, {})".format(repo, user, path_to_dockerfile))
                images.append(create_image(repo, user, path_to_dockerfile))
                logger.info("Added image {} to list".format(images[-1]))
            userdir = os.path.expanduser("~") + '/' + user
            if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
                subprocess.call(['rm', '-rf', userdir])
        else:
            logger.debug("clone_repo({}, {}) returned FALSE".format(user, repo))
            return("Something got messed up!")
        deployment_name = repo
        logger.debug("Contents of variable 'images': {}".format(images))
        logger.info("Length of images: {}".format(len(images)))
        try:
            logger.info("Using {} as frontend image open to the world.".format(images[0][0]))
        except:
            logger.info("Should be returning...")
            return "No Dockerfiles found, please try again"
        try:
            delete_deployment(deployment_name, config_location)
        except:
            logger.error("Tried to delete deployment, but threw an error")
            pass
        try:
            create_deployment(create_deployment_object(images, deployment_name, config_location=config_location), config_location=config_location)
        except: # This deployment likely already exists
            try:
                update_deployment(create_deployment_object(images, deployment_name, config_location=config_location), deployment_name, config_location=config_location)
            except:
                logger.error("Could not create or update a deployment object, check the status of the cluster.")
        try:
            port = -1
            for image in images:
                if "frontend" in image[0]:
                    port = int(image[1])
            if port == -1:
                port = int(images[0][1])
            node_port = create_service(deployment_name, port, config_location)
        except:
            node_port = -1
            logger.critical("Could not create a service for this application.")
        #MongoDB stuff
        try:
            if repo is not None and user is not None:
                user_param = mongo.db.users.find({'username': {"$in" :[user]}})
                if user_param:
                   mongo.db.users.update({'username':user},{"$push" :{'git-repo':{"$each" :[repo]}}})
                else:
                    user = {
                        'username': user,
                        'git-repo': [repo]
                    }
                # Attempt to connect to the db
                result = mongo.db.users.insert_one(user)
        except errors.ServerSelectionTimeoutError:
            print("MongoDB could not be found")
    return("Running on port {}".format(node_port))

@app.route("/delete/<deployment>", methods=["POST"])
def delete(deployment):
    try:
        delete_deployment(deployment, config_location)
        return("Deleted {}".format(deployment))
    except:
        return("Error trying to delete deployment {}. Does it exist?".format(deployment))
        
if __name__ == '__main__':
    app.debug = True
    app.run(use_reloader=True, debug=True, host='0.0.0.0', port=5001)