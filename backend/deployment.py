# This is going to house kubernetes and docker commands

import subprocess
import sys

def clone_repo(user, repo):
    github_string = 'git@github.com:{}/{}.git'.format(user,repo)
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        subprocess.call(['mkdir', '/home/{}/{}'.format(user,repo)])
        subprocess.call(['git','init'])
        subprocess.call(['git', 'clone', github_string])
        # create_image(user, repo)
        return("cloning {}".format(github_string))
    else:
        return('Running in dev... \nRight now would be setting up ' + repo + ' from user: ' + user)