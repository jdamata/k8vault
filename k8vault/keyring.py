import logging
import keyring
import os
import yaml
import json

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

k8vault_path = os.path.join(os.path.expanduser('~'),'.k8vault')
kubeconfig_path = os.path.join(os.path.expanduser('~'),'.kube/config')

def add_kubeconfig(kubeconfig):
    # Prompt for a configname
    configname = input("Give your kubeconfig a unique name: ")

    # Check if configname already exists in keychain
    data = keyring.get_password("k8vault", configname)
    if data is not None:
        logger.error("Configname {} already exists in the keychain".format(configname))
        raise SystemExit()

    # Create file if it does not exist and ensure that given kubeconfig name does not exist.
    try:
        f = open(k8vault_path, 'r')
        try:
            k8vault_json = json.load(f)
        except ValueError:
            f.close()
            k8vault_json = {}
    except IOError:
        f = open(k8vault_path, 'w+')
        f.close()
        k8vault_json = {}

    # Read kubeconfig, ensure it is valid yaml and store in keychain
    with open(kubeconfig, "r") as f:
        data = f.read()
    yaml.safe_load(data)
    keyring.set_password("k8vault", configname, data)

    # Update .k8vault
    k8vault_json[configname] = 'inactive'
    with open(k8vault_path, "w") as f:
        json.dump(k8vault_json, f)
    logger.info("Stored kubeconfig in {}".format(configname))


def delete_kubeconfig(configname):
    # Check if configname is in keychain
    data = keyring.get_password("k8vault", configname)
    if data is None:
        logger.error("Configname {} does not exist in the keychain".format(configname))
        raise SystemExit()

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
        logger.info("Configname {} does not exist".format(configname))
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


def update_kubeconfig(configname, kubeconfig):
    # Check if configname exists in keychain
    data = keyring.get_password("k8vault", configname)
    if data is None:
        logger.warn("Configname {} does not exist".format(configname))
        raise SystemExit()

    # Store in keychain
    keyring.set_password("k8vault", configname, data)
    logger.info("Stored kubeconfig in {}".format(configname))
