import logging
import keyring
import os
import yaml
import json

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

k8vault_path = os.path.join(os.path.expanduser('~'),'.k8vault')
kubeconfig_path = os.path.join(os.path.expanduser('~'),'.kube/config')


def create_config(kubeconfig, configname):
    """
    Create a keychain secret with kubeconfig and configname.
    Create/Edit ~/.k8vault file to keep track of existing kubeconfigs.
    """
    try:
        f = open(k8vault_path, 'r')
        try:
            k8vault_json = json.load(f)
            logger.debug("Loaded data in {}.".format(k8vault_path))
        except ValueError:
            logger.warn("No data or invalid json found in {}.".format(k8vault_path))
            f.close()
            k8vault_json = {}
    except IOError:
        logger.info("Creating {}.".format(k8vault_path))
        f = open(k8vault_path, 'w+')
        f.close()
        k8vault_json = {}
    with open(kubeconfig, "r") as f:
        data = f.read()
    yaml.safe_load(data)
    keyring.set_password("k8vault", configname, data)
    k8vault_json[configname] = 'inactive'
    with open(k8vault_path, "w") as f:
        json.dump(k8vault_json, f)
    logger.debug("Updated {}".format(k8vault_path))

def check_config(configname):
    """
    Check if the configname exists in the keychain.
    Returns true if config exists.
    """
    data = keyring.get_password("k8vault", configname)
    if data is None:
        return False
    else:
        return True
