# k8s vault
K8s Vault is a tool to securely store and access kubernetes configuration files development environment.

K8s Vault stores base64 encoded kubeconfigs in your operating system's secure keystore and then outputs them into ~/.kube/config. This means only a single kubeconfig file will be present on your local filesystem.

Currently there is no programmatic way to supply a kubeconfig to kubectl.

## Installing

```bash
pip install k8s-vault
```

## Basic Usage
Add a kubeconfig to k8s-vault
```bash
k8s-vault add ~/.kube/docker-for-desktop
```


```bash
k8s-vault exec docker-for-desktop
```
