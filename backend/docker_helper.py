# Functions used to clone the github repository and create a container from a Dockerfile

import subprocess
import sys
import docker
import os
import re
import logging

logging.basicConfig(filename="backend.log", format='%(levelname)s: %(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def homedir():
    return os.path.expanduser("~")

def clone_repo(user, repo):
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        logger.info("Running on linux or mac")
        basedir = '{}/{}/{}'.format(homedir(), user, repo) # = '/home/<linux user>/<github user>/<repo>'
        userdir = '{}/{}'.format(homedir(), user) # = '/home/<linux user>/<github user>'
        github_string = 'https://github.com/{}/{}.git'.format(user,repo)
        subprocess.call(['rm', '-rf', basedir])
        subprocess.call(['mkdir', '-p', userdir])
        subprocess.call(['git', '-C', userdir, 'clone', github_string])
        logger.info("Repo successfully cloned to {}".format(userdir))
        return True
    else:
        logger.debug("Running on Windows, is this dev?")
        return False

# This returns a list of the dockerfiles found, in the form of their file location
def find_dockerfiles(user, repo):
    basedir = '{}/{}/{}'.format(homedir(), user, repo)
    logger.info("Searching for Dockerfiles in {} (which is the basedir)".format(basedir))
    result = []
    for root, dirs, files in os.walk(basedir, topdown=False):
        for name in files:
            if name == 'Dockerfile':
                logger.info("Found Dockerfile at: {} ".format(root))
                result.append(os.path.join(root, 'Dockerfile'))
    logger.debug("Result of Dockerfile search: ", result)
    return result

# Returns a string with the image tag (name of the image created)
def create_image(repo, user, path_to_dockerfile, is_frontend=False):
    try:
        username = os.environ['DOCKERUSER']
        password = os.environ['DOCKERPASS']
        logger.info("Logged into registry as {}".format(username))
    except: # Hard coded for now
        username = 'stolaunch'
        password = 'launchpass'
        return
    # Get the port from the Dockerfile
    try:
        with open(path_to_dockerfile, 'r') as file:
            contents = file.read()
            match = re.search('EXPOSE (\d+)',contents)
            try:
                container_port = match.group(1)
            except:
                container_port = 5000
            file.close()
    except FileNotFoundError:
        logger.critical("FileNotFoundError: Could not find Dockerfile in expected path: {}".format(path_to_dockerfile))
    except:
        logger.critical("Could not open Dockerfile")
    logger.debug("Creating image from: {}".format(path_to_dockerfile))
    client = docker.from_env()
    path_to_dockerfile = path_to_dockerfile.replace('Dockerfile', '')
    tag = username + "/" + path_to_dockerfile.replace(homedir(), '').replace(user, '').replace('/', '') + ":latest"
    client.images.build(path=path_to_dockerfile, rm=True, tag=tag, platform='amd64')
    logger.info("Image tag is: {}".format(tag))
    client.login(username=username, password=password)
    client.images.push(tag)
    logger.info("Pushed image to {}".format(tag))
    basedir = '{}/{}/{}'.format(homedir(), user, repo)
    return (tag, container_port)