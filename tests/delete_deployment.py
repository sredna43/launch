from os import path
import sys
from kubernetes import client, config

def main():
    config.load_kube_config()
    v1 = client.AppsV1Api()
    if sys.argv[1]:
        name = sys.argv[1]
    else:
        name = 'cir-anders-openmp'
    resp = v1.delete_namespaced_deployment(name=name, namespace="cir-anders-namespace")
    print("Deployment {} deleted.".format(name))

if __name__ == '__main__':
    main()