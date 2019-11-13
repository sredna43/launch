# StoLaunch

Deploy custom web applications using a simple user interface that connects to Git

## Getting started:

- We assume for the duration of these instructions that you already have a Kubernetes cluster up and running, and have access to it using kubectl. If this is not the case, you should consult the official kubectl documentation [here](https://kubernetes.io/docs/tasks/tools/install-kubectl/). If you do not have a Kubernetes cluster set up, you can set one up following documentation [here](https://kubernetes.io/docs/tasks/tools/install-minikube/).

- Launch ships with its own `deployment.yaml` file that sets up the project to run in a kubernetes cluster. Because of this, all you need to do is populate the `DOCKERUSER` and `DOCKERPASS` fields with the username and password for your Image registry. 

(Note: if you do not have a docker registry set up, you can create a free Docker Hub account [here](https://hub.docker.com/).) 

- Once you have populated the username and password fields, open up a terminal, navigate to the folder containing the deployment.yaml file, and apply the deployment to your cluster using the command `kubectl apply -f deployment.yaml`.

- In order to check to make sure Launch is running properly, open up a terminal and run `kubectl get pods`. If Launch is running correctly, you should see an output that looks something like this: `launch-<hash string> 2/2 Running 0 <time>`. Make sure the Docker Daemon is connected the way it should be by running the command `docker image ls`. You should see a list of images that correspond to the kubernetes cluster (because there should not be any images stored within Launch itself).
  
- Now that the Launch deployment is running and has deployed a pod, we need to expose it to the world so that we can access it. We perform this task via what is called a service. In order to create a service that exposes Launch to the external world, run the command: `kubectl expose deployment launch --type=LoadBalancer --name=launch-expose`. This command will expose the two ports required by Launch in order to run properly. Wait about one minute, and then run the command: `kubectl get services launch-expose` and note the IP address under `<external IP>`. This is the address that you will have to type into your browser in order to access Launch. 

- Open up your browser, and navigate to the address: `http://<external IP>:5000` in order to see the UI for Launch. You should now be able to use Launch to its full capabilities.

## Contributing

If you would like to contribute, please refer to our contributing guidelines.

## Senior capstone project Fall 2019

Roger Becerra, Charlie Carlson, Hannah Dettmann, Anders Olson
