# This is going to house kubernetes and docker commands

import subprocess
import sys
import docker
import os

def clone_repo(user, repo):
    homedir = os.path.expanduser("~")
    github_string = 'git@github.com:{}/{}.git'.format(user,repo)
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        subprocess.call(['mkdir', '-p', '{}/{}/{}'.format(homedir,user,repo)])
        subprocess.call(['git','init'])
        subprocess.call(['git', 'clone', github_string])
        return("cloning {}".format(github_string))
    else:
        return('Running in dev... \nRight now would be setting up ' + repo + ' from user: ' + user)

def create_image(user, repo, path_to_dockerfile):
    client = docker.from_env()
    image = client.images.build(path=path_to_dockerfile, rm=True, tag=repo)
    return image

# This returns a list of the dockerfiles found
def find_dockerfiles(homedir):
    result = []
    for root, dirs, files in os.walk(homedir):
        if 'Dockerfile' in files:
            result.append(os.path.join(root, 'Dockerfile'))
    return result