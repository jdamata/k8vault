# k8vault
k8vault is a tool to securely store and access kubernetes configuration files.  
k8vault stores encoded kubeconfigs in your operating system's secure keystore and then outputs them into ~/.kube/config. This means only a single kubeconfig file needs to be present on your local filesystem.  

## Installing
Install k8vault
```bash
pip install k8vault
```

## Basic Usage
Add a kubeconfig to k8vault
```bash
k8vault add ~/.kube/docker-for-desktop
```

Switch to a kubeconfig
```bash
k8vault get docker-for-desktop
```

List stored kubeconfigs
```bash
k8vault list
```

Delete a kubeconfig
```bash
k8vault delete docker-for-desktop
```
