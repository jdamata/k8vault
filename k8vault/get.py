import logging

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def get_darwin_kubeconfig(configname):
    kubeconfig_b64 = keyring.get_password("k8vault", configname)
    kubeconfig = base64.b64decode(kubeconfig_b64)
    with open('~/.kube/config', "w") as f:
        f.write(kubeconfig)

def get_windows_kubeconfig(configname):
    kubeconfig_b64 = keyring.get_password("k8vault", configname)
    kubeconfig = base64.b64decode(kubeconfig_b64)
    with open('~/.kube/config', "w") as f:
        f.write(kubeconfig)

def get_linux_kubeconfig(configname):
    kubeconfig_b64 = keyring.get_password("k8vault", configname)
    kubeconfig = base64.b64decode(kubeconfig_b64)
    with open('~/.kube/config', "w") as f:
        f.write(kubeconfig)
