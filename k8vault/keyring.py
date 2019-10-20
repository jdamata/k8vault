import logging
import base64
import keyring
import os
import json

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

k8vault_path = os.path.join(os.path.expanduser('~'),'.k8vault')
kubeconfig_path = os.path.join(os.path.expanduser('~'),'.kube/config')

def add_kubeconfig(kubeconfig):
    # Prompt for a configname
    configname = input("Give your kubeconfig a unique name: ")

    # Create file if it does not exist and ensure that given kubeconfig name does not exist.
    try:
        f = open(k8vault_path, 'r')
        try:
            k8vault_json = json.load(f)
            if configname in k8vault_json.keys():
                logger.error("The kubeconfig name is already in use. Please use another name")
                raise SystemExit()
        except ValueError:
            f.close()
            k8vault_json = {}
    except IOError:
        f = open(k8vault_path, 'w+')
        f.close()
        k8vault_json = {}

    # Read kubeconfig and store in keychain
    with open(kubeconfig, "r") as f:
        data = f.read()
    keyring.set_password("k8vault", configname, data)

    # Update .k8vault file with kubeconfig name
    k8vault_json[configname] = 'inactive'
    with open(k8vault_path, "w") as f:
        json.dump(k8vault_json, f)
    logger.info("Stored kubeconfig in {}".format(configname))


def delete_kubeconfig(configname):
    # Delete kubeconfig from keychain
    keyring.delete_password("k8vault", configname)

    # Delete configname from .k8vault
    with open(k8vault_path, 'r') as f:
        k8vault_json = json.load(f)
        k8vault_json.pop(configname, None)
    with open(k8vault_path, 'w') as f:
        json.dump(k8vault_json, f)
    logger.info("Kubeconfig {} has been deleted".format(configname))


def get_kubeconfig(configname):
    # Get kubeconfig from keychain
    data = keyring.get_password("k8vault", configname)
    if data is not None:
        with open(kubeconfig_path, "w") as f:
            f.write(data)
        logger.info("Kubeconfig {} has been placed into {}".format(configname, kubeconfig_path))
    else:
        logger.info("Kubeconfig {} does not exist".format(configname))
        raise SystemExit()

    # Set kubeconfig to active in .k8vault
    with open(k8vault_path, 'r') as f:
        k8vault_json = json.load(f)
        k8vault_json = dict.fromkeys(k8vault_json, 'inactive')
        k8vault_json[configname] = 'active'
    with open(k8vault_path, 'w') as f:
        json.dump(k8vault_json, f)


def list_kubeconfig():
    # List .k8vault file with kubeconfig name
    try:
      with open(k8vault_path, "r") as f:
          k8vault_json = json.load(f)
          for key, value in k8vault_json.items():
              print('{}: {}'.format(key, value))
    except IOError:
        logger.error("K8vault file does not exist. Have you stored any kubeconfigs yet?")
