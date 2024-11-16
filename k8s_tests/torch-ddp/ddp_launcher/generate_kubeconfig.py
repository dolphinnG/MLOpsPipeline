import os
import base64
import yaml

def generate_kubeconfig():
    # Define the paths to the service account files
    sa_path = "/var/run/secrets/kubernetes.io/serviceaccount"
    token_path = os.path.join(sa_path, "token")
    ca_path = os.path.join(sa_path, "ca.crt")
    namespace_path = os.path.join(sa_path, "namespace")

    # Read the service account token, CA certificate, and namespace
    with open(token_path, 'r') as f:
        token = f.read().strip()
    with open(ca_path, 'rb') as f:  # Read as binary
        ca_cert = base64.b64encode(f.read()).decode('utf-8')  # Encode in base64
    with open(namespace_path, 'r') as f:
        namespace = f.read().strip()

    # Construct the kubeconfig dictionary
    kubeconfig = {
        'apiVersion': 'v1',
        'clusters': [{
            'cluster': {
                'server': 'https://kubernetes.default.svc',  # The default Kubernetes API server URL
                'certificate-authority-data': ca_cert
            },
            'name': 'kubernetes'
        }],
        'contexts': [{
            'context': {
                'cluster': 'kubernetes',
                'namespace': namespace,
                'user': 'default'
            },
            'name': 'default'
        }],
        'current-context': 'default',
        'kind': 'Config',
        'preferences': {},
        'users': [{
            'name': 'default',
            'user': {
                'token': token
            }
        }]
    }

    # Write the kubeconfig to a file
    kubeconfig_path = os.path.join(os.path.expanduser("~"), ".kube", "config")
    os.makedirs(os.path.dirname(kubeconfig_path), exist_ok=True)
    with open(kubeconfig_path, 'w') as f:
        yaml.dump(kubeconfig, f)

if __name__ == "__main__":
    generate_kubeconfig()