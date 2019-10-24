from os import path
import yaml
from kubernetes import client, config

def main():
    config.load_kube_config()
    v1 = client.AppsV1Api()
    resp = v1.delete_namespaced_deployment(name='cir-anders-openmp', namespace="cir-anders-namespace")
    print("Deployment {} deleted.".format('cir-anders-openmp'))

if __name__ == '__main__':
    main()