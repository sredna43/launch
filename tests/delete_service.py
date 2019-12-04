# Deletes a namespaced service
from kubernetes import client, config
from os import path
import sys

def main():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    serv = v1.delete_namespaced_service(
            name=sys.argv[1],
            namespace='cir-anders-namespace'
        )
    print("Delete service status: {}".format(str(serv.status)))

if __name__ == '__main__':
    main()
