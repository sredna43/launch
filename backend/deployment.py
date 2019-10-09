# This is going to house kubernetes and docker commands

import subprocess
import sys
import docker

def clone_repo(user, repo):
    github_string = 'git@github.com:{}/{}.git'.format(user,repo)
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        subprocess.call(['mkdir', '/home/{}/{}'.format(user,repo)])
        subprocess.call(['git','init'])
        subprocess.call(['git', 'clone', github_string])
        return("cloning {}".format(github_string))
    else:
        return('Running in dev... \nRight now would be setting up ' + repo + ' from user: ' + user)

def create_image(user, repo, path_to_dockerfile):
    client = docker.from_env()
    image = client.images.build(path=path_to_dockerfile, rm=True, tag=repo)
    return image