from kubernetes import client, config

def create_deployment_object(images, app_name, config_location):
    if config_location != None:
        config.load_kube_config(config_location)
    else:
        config.load_kube_config()
    v1 = client.AppsV1Api()
    containers = []
    # Create a container for each image
    for image in images:
        print("Adding container to deployment with image {}...".format(image[0]))
        containers.append(client.V1Container(
            name=image[0],
            image=image[0],
            ports=[client.V1ContainerPort(container_port=str(image[1]))]
        ))
    # Create metadata and spec
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app":app_name}),
        spec=client.V1PodSpec(containers=containers)
    )
    # Create the specification section
    spec = client.V1DeploymentSpec(
        replicas=1,
        template=template,
        selector={'matchLabels': {'app': app_name}}
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

def delete_deployment(deployment_name): #deployment_name is just <repo>-deployment
    config.load_kube_config()
    v1 = client.AppsV1Api()
    api_resp = v1.delete_namespaced_deployment(
        name=deployment_name,
        namespace='cir-anders-namespace',
        body=client.V1DeleteOptions(
            propogation_policy='Foreground',
            grace_period_seconds=5
        )
    )
    print("Deployment deleted. Status={}".format(str(api_resp.status)))
    return
