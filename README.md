# k8vault
k8vault is a tool to securely store and access kubernetes configuration files. It stores kubeconfigs in your operating system's secure keystore and then writes them to ~/.kube/config. For this to work, you need the KUBECONFIG env var pointed at ~/.kube/config.

This has only been tested on macOS.

## Installing
Install k8vault
```bash
go get -u github.com/jdamata/k8vault
```

## Basic Usage
To use a custom keychain, specify --keychain

Add a kubeconfig to the keyring
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