from os import path
import yaml
from kubernetes import client, config

def main():
    config.load_kube_config()

    with open(path.join(path.dirname(__file__), "cir-anders-deployment.yaml")) as f:
        dep = yaml.safe_load(f)
        v1 = client.AppsV1Api()
        resp = v1.create_namespaced_deployment(body=dep, namespace="cir-anders-namespace")
        print("Deployment created. Status='%s'" % resp.metadata.name)

if __name__ == '__main__':
    main()