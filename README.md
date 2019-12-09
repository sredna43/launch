# StoLaunch

Deploy custom web applications using a simple user interface that connects to Git

## Installing Launch on Kubernetes:

- We assume for this section that you already have a Kubernetes cluster up and running, and have access to it using kubectl. If this is not the case, you should consult the official kubectl documentation [here](https://kubernetes.io/docs/tasks/tools/install-kubectl/). If you do not have a Kubernetes cluster set up, you can set up a local instance by following documentation [here](https://kubernetes.io/docs/tasks/tools/install-minikube/). It is also possible to run Launch on cloud-based Kubernetes solutions such as AWS or Google Cloud. Documentation for this type of installation can be found below.

- Launch ships with its own `deployment.yaml` file that sets up the project to run in a kubernetes cluster. Because of this, all you need to do is populate the `DOCKERUSER` and `DOCKERPASS` fields with the username and password for your DockerHub registry.

(Note: if you do not have a docker registry set up, you can create a free Docker Hub account [here](https://hub.docker.com/).)

- Once you have populated the username and password fields, open up a terminal, navigate to the folder containing the deployment.yaml file, and apply the deployment to your cluster using the command `kubectl apply -f deployment.yaml`. This will create the pods necessary, and defines some important information regarding system requirements.

- In order to check to make sure Launch is running properly, open up a terminal and run `kubectl get pods`. If Launch is running correctly, you should see an output that looks something like this: `launch-<hash string> 2/2 Running 0 <time>` where `launch-<hash string>` is the name of the pod currently running Launch. Make sure the Docker Daemon is connected the way it should be by running the command `kubectl exec <pod name> -c launch-backend docker image ls`. You should see a list of images that correspond to the kubernetes cluster (there should not be any images stored within Launch itself, instead, Launch uses the cluster's Docker Daemon).
  
- Now that the Launch deployment is running and has deployed a pod, we need to expose it to the world so that we can access it. We perform this task via what is called a service. In order to create a service that exposes Launch to the external world, run the command: `kubectl expose deployment launch --type=NodePort --name=launch-expose`. This command will expose the two ports required by Launch in order to run properly. Wait about one minute, and then run the command: `kubectl get services launch-expose`.

- Open up your browser, and navigate to the address: `http://<cluster node IP>:5000` in order to see the UI for Launch. You should now be able to use Launch to its full capabilities.

(Note: If your cluster is set up to forward all NodePort ports to a different specified range, then you should see something like `5000:31234/TCP` listed under `PORT(S)` when you run the `get services` command.)

- At this point, Launch is up and running! Go ahead and test to see if it is working correctly by entering the details of your first project! To see more about how to create a Launch-friendly application, see below.

## Make Your Application Launch-Friendly

- Because Launch relies upon Docker to function properly, your repository must also contain a Dockerfile. There are detailed instructions on how to create a Dockerfile [here](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/).

- For the time being, Launch is only capable of creating static web applications, this means that you must send any database requests to an outside service such as the MongoDB cloud, or other cloud database solutions.

- For most applications, you will likely be best served to simply use a NGINX solution to serve your application. Some documentation can be found [here](https://hub.docker.com/_/nginx), under the "hosting some simple static content" subsection of the "how to use this image" section of this webpage.

- As long as your project contains a Dockerfile, everything should run smoothly!

## Contributing

- If you would like to contribute some of your own changes, either for just yourself or the whole community, you can do so by following the guidelines and instructions found [here](/CONTRIBUTING.md). Happy coding!

## Senior capstone project Fall 2019

Roger Becerra, Charlie Carlson, Hannah Dettmann, Anders Olson
