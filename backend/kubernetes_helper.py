# Functions used to create, update, and delete deploymenets

from kubernetes import client, config

def create_deployment_object(images, app_name, config_location):
    if config_location != None:
        config.load_kube_config(config_location)
    else:
        config.load_kube_config()
    containers = []
    # Create a container for each image
    for image in images:
        print("Adding container to deployment with image {}...".format(image[0]))
        containers.append(client.V1Container(
            name=image[0],
            image="stolaunch/{}:latest".format(image[0]),
            ports=[client.V1ContainerPort(container_port=int(image[1]))]
        ))
    print(containers)
    # Create metadata and spec
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={'app': app_name}),
        spec=client.V1PodSpec(containers=containers)
    )
    # Create the specification section
    spec = client.V1DeploymentSpec(
        replicas=1,
        selector={'matchLabels': {'app': app_name}},
        template=template
        
    )
    # Create and instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=app_name),
        spec=spec
    )
    # Return our deployment object
    return deployment

def create_deployment(deployment, config_location):
    print("Creating deployment")
    if config_location != None:
        config.load_kube_config(config_location)
    else:
        config.load_kube_config()
    v1 = client.AppsV1Api()
    api_resp = v1.create_namespaced_deployment(
        body=deployment,
        namespace='cir-anders-namespace'
    )
    print("Created deployment. Status={}".format(str(api_resp.status)))
    return

def update_deployment(deployment, deployment_name, config_location):
    if config_location != None:
        config.load_kube_config(config_location)
    else:
        config.load_kube_config()
        v1 = client.AppsV1Api()
    api_resp = v1.patch_namespaced_deployment(
        name=deployment_name,
        namespace='cir-anders-namespace',
        body=deployment
    )
    print("Deployment updated. Status={}".format(api_resp.status))
    return

def delete_deployment(deployment_name, config_location): # deployment_name is just <repo>-deployment
    if config_location != None:
        config.load_kube_config(config_location)
    else:
        config.load_kube_config()
    v1 = client.AppsV1Api()
    api_resp = v1.delete_namespaced_deployment(
        name=deployment_name,
        namespace='cir-anders-namespace'
    )
    print("Deployment deleted. Status={}".format(str(api_resp.status)))
    return