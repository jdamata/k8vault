import logging
import keyring
import os
import yaml
import json

from .helper import check_config, create_config

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

k8vault_path = os.path.join(os.path.expanduser('~'),'.k8vault')
kubeconfig_path = os.path.join(os.path.expanduser('~'),'.kube/config')

def add_kubeconfig(kubeconfig):
    """
    Add a kubeconfig to the keychain
    """
    configname = input("Give your kubeconfig a unique name: ")
    if check_config(configname):
        raise SystemExit("Configname {} already exists".format(configname))
    create_config(kubeconfig, configname)
    logger.info("Stored kubeconfig in {}".format(configname))


def delete_kubeconfig(configname):
    """
    Delete a kubeconfig from the keychain
    """
    if not check_config(configname):
        raise SystemExit("Configname {} does not exist".format(configname))
    keyring.delete_password("k8vault", configname)
    logger.info("Kubeconfig {} has been deleted".format(configname))
    with open(k8vault_path, 'r') as f:
        k8vault_json = json.load(f)
        k8vault_json.pop(configname, None)
    with open(k8vault_path, 'w') as f:
        json.dump(k8vault_json, f)
    logger.debug("Updated {}".format(k8vault_path))


def get_kubeconfig(configname):
    """
    Retrieve a kubeconfig from the keychain to ~/.kube/config
    """
    if not check_config(configname):
        raise SystemExit("Configname {} does not exist".format(configname))
    data = keyring.get_password("k8vault", configname)
    with open(kubeconfig_path, "w") as f:
        f.write(data)
    logger.info("Kubeconfig {} has been placed into {}".format(configname, kubeconfig_path))
    with open(k8vault_path, 'r') as f:
        k8vault_json = json.load(f)
        k8vault_json = dict.fromkeys(k8vault_json, 'inactive')
        k8vault_json[configname] = 'active'
    with open(k8vault_path, 'w') as f:
        json.dump(k8vault_json, f)
    logger.debug("Updated {}".format(k8vault_path))


def list_kubeconfig():
    """
    List known kubeconfigs from ~/.k8vault
    """
    try:
      with open(k8vault_path, "r") as f:
          k8vault_json = json.load(f)
          for key, value in k8vault_json.items():
              print('{}: {}'.format(key, value))
    except IOError:
        logger.error("K8vault file does not exist. Have you stored any kubeconfigs yet?")


def update_kubeconfig(kubeconfig, configname):
    """
    Update an existing kubeconfig in the keychain.
    """
    if not check_config(configname):
        raise SystemExit("Configname {} does not exist".format(configname))
    create_config(kubeconfig, configname)
    logger.info("Updated kubeconfig in {}".format(configname))
