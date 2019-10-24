from kubernetes import client, config

def main():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    pod_list = v1.list_namespaced_pod('cir-anders-namespace')
    for pod in pod_list.items:
        print("%s\t%s\t%s" % (pod.metadata.name, 
                          pod.status.phase,
                          pod.status.pod_ip))

if __name__ == '__main__':
    main()