from kubernetes import client, config

def main():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    pod_list = v1.list_namespaced_pod('cir-anders-namespace')
    services_list = v1.list_namespaced_service('cir-anders-namespace')
    for pod in pod_list.items:
        print("%s\t%s\t%s" % (pod.metadata.name, 
                          pod.status.phase,
                          pod.status.pod_ip))
    for service in services_list.items:
        print("%s\t%s" % (service.metadata.name,
                          service.spec.ports[0].node_port))

if __name__ == '__main__':
    main()