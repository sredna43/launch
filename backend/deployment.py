# This is going to house kubernetes and docker commands

import subprocess
import sys
import docker
import os

def homedir():
    return os.path.expanduser("~")

def clone_repo(user, repo):
    basedir = '{}/{}/{}'.format(homedir(), user, repo)
    userdir = '{}/{}'.format(homedir(), user)
    github_string = 'https://github.com/{}/{}.git'.format(user,repo)
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        subprocess.call(['mkdir', '-p', userdir])
        subprocess.call(['git', '-C', basedir, 'init'])
        subprocess.call(['git', '-C', userdir, 'clone', github_string])
        return True
    else:
        return False

def create_image(repo, path_to_dockerfile, is_frontend=False):
    client = docker.from_env()
    path_to_dockerfile = path_to_dockerfile.replace('Dockerfile', '')
    image = client.images.build(path=path_to_dockerfile, rm=True, tag=repo)
    return image

# This returns a list of the dockerfiles found, in the form of their file location
def find_dockerfiles(user, repo):
    basedir = '{}/{}/{}'.format(homedir(), user, repo)
    result = []
    for root, dirs, files in os.walk(basedir):
        if 'Dockerfile' in files:
            result.append(os.path.join(root, 'Dockerfile'))
    return result