import logging
import base64
import keyring

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def add_darwin_kubeconfig(kubeconfig):
    kubeconfig_b64 = base64.b64encode(kubeconfig.encode())
    configname = input("Give your kubeconfig a unique name: ")
    keyring.set_password("k8vault", configname, kubeconfig_b64)

def add_windows_kubeconfig(kubeconfig):
    kubeconfig_b64 = base64.b64encode(kubeconfig.encode())
    configname = input("Give your kubeconfig a unique name: ")
    keyring.set_password("k8vault", configname, kubeconfig_b64)

def add_linux_kubeconfig(kubeconfig):
    kubeconfig_b64 = base64.b64encode(kubeconfig.encode())
    configname = input("Give your kubeconfig a unique name: ")
    keyring.set_password("k8vault", configname, kubeconfig_b64)
