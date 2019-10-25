# This is going to house kubernetes and docker commands

import subprocess
import sys
import docker
import os
import yaml
from kubernetes import client, config

def homedir():
    return os.path.expanduser("~")

def clone_repo(user, repo):
    basedir = '{}/{}/{}'.format(homedir(), user, repo) # = '/home/<linux user>/<github user>/<repo>'
    userdir = '{}/{}'.format(homedir(), user) # = '/home/<linux user>/<github user>'
    github_string = 'https://github.com/{}/{}.git'.format(user,repo)
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        subprocess.call(['rm', '-rf', basedir])
        subprocess.call(['mkdir', '-p', userdir])
        # subprocess.call(['git', '-C', userdir, 'init'])
        subprocess.call(['git', '-C', userdir, 'clone', github_string])
        print("Repo successfully cloned")
        return True
    else:
        print("Must be running on Windows")
        return False

def create_image(repo, user, path_to_dockerfile, is_frontend=False):
    print("Creating image: {}".format(path_to_dockerfile))
    client = docker.from_env()
    path_to_dockerfile = path_to_dockerfile.replace('Dockerfile', '')
    print("Dockerfile path: %s" % path_to_dockerfile)
    tag = path_to_dockerfile.replace(homedir(), '').replace(user, '').replace('/', '')
    if is_frontend:
        tag += "-frontend"
    else:
        tag += "-backend"
    print("Image tag is: {}".format(tag))
    image = client.images.build(path=path_to_dockerfile, rm=True, tag=tag)
    return image

# This returns a list of the dockerfiles found, in the form of their file location
def find_dockerfiles(user, repo):
    basedir = '{}/{}/{}'.format(homedir(), user, repo)
    print("Searching for Dockerfiles in {} (which is the basedir)".format(basedir))
    result = []
    for root, dirs, files in os.walk(basedir, topdown=False):
        for name in files:
            if name == 'Dockerfile':
                print("Found Dockerfile at: {} ".format(root))
                result.append(os.path.join(root, 'Dockerfile'))
    print("Result of Dockerfile search: ", result)
    return result

def create_deployment_object(user, repo, images=None):
    contents = [{}]
    yaml_file = '{}/{}/{}/deployment.yaml'.format(homedir(), user, repo)
    with open(yaml_file, 'w') as file:
        documents = yaml.dump(contents, file)
    #yaml stuff incoming